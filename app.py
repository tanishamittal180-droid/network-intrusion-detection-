import sys,os,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
import pandas as pd
from fastapi import FastAPI,HTTPException,Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field,field_validator
from backend.database import connect,init_db
from backend.services.ids_service import IDSService
from ids.rule_engine import DEFAULT_RULES

app=FastAPI(title='Network IDS Simulation API',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])
service=IDSService(); init_db()
try:
    df=pd.read_csv(ROOT/'data/network_traffic.csv'); service.fit(df.to_dict('records'))
except Exception: df=pd.DataFrame()

class Flow(BaseModel):
    flow_id:str; timestamp:str; source_ip:str; destination_ip:str; source_port:int=Field(ge=0,le=65535); destination_port:int=Field(ge=0,le=65535); protocol:str; packet_count:int=Field(ge=0); byte_count:int=Field(ge=0); duration_seconds:float=Field(ge=0); connection_count:int=Field(ge=0); failed_connection_count:int=Field(ge=0); syn_count:int=Field(ge=0); rst_count:int=Field(ge=0); average_packet_size:float=Field(ge=0); label:str='NORMAL'; scenario_type:str='LIVE'
    @field_validator('protocol')
    @classmethod
    def protocol_ok(cls,v):
        if v.upper() not in {'TCP','UDP','ICMP'}: raise ValueError('protocol must be TCP, UDP, or ICMP')
        return v.upper()

class Note(BaseModel): note:str=Field(min_length=1,max_length=2000)
class Status(BaseModel): status:str

@app.get('/api/health')
def health(): return {'status':'ok','synthetic_only':True}

@app.post('/api/flows')
def create_flow(flow:Flow):
    d=flow.model_dump(); f,h,a,r,c,alert=service.analyze(d); con=connect(); con.execute('INSERT OR REPLACE INTO network_flows VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(d['flow_id'],d['timestamp'],d['source_ip'],d['destination_ip'],d['source_port'],d['destination_port'],d['protocol'],d['packet_count'],d['byte_count'],d['duration_seconds'],r,c))
    if alert:
        con.execute('INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(alert['alert_id'],d['flow_id'],alert['rule_id'],alert['severity'],alert['alert_type'],alert['description'],r,'NEW',alert['timestamp'],d['source_ip'],d['destination_ip'],d['protocol'],d['source_port'],d['destination_port'],a,None))
    con.commit(); con.close(); return {'flow':f,'classification':c,'risk_score':r,'matched_rules':h,'anomaly_score':a,'alert':alert}

@app.get('/api/flows')
def flows(limit:int=Query(100,ge=1,le=1000)):
    c=connect(); rows=[dict(x) for x in c.execute('SELECT * FROM network_flows ORDER BY timestamp DESC LIMIT ?', (limit,))]; c.close(); return rows
@app.get('/api/flows/{flow_id}')
def flow(flow_id:str):
    c=connect(); r=c.execute('SELECT * FROM network_flows WHERE flow_id=?',(flow_id,)).fetchone(); c.close();
    if not r: raise HTTPException(404,'Flow not found')
    return dict(r)
@app.get('/api/alerts')
def alerts(limit:int=Query(100,ge=1,le=1000),severity:str|None=None,status:str|None=None):
    q='SELECT * FROM alerts WHERE 1=1'; p=[]
    if severity:q+=' AND severity=?';p.append(severity)
    if status:q+=' AND status=?';p.append(status)
    q+=' ORDER BY created_at DESC LIMIT ?';p.append(limit); c=connect(); out=[dict(x) for x in c.execute(q,p)]; c.close(); return out
@app.get('/api/alerts/{alert_id}')
def get_alert(alert_id:str):
    c=connect(); a=c.execute('SELECT * FROM alerts WHERE alert_id=?',(alert_id,)).fetchone(); notes=[dict(x) for x in c.execute('SELECT * FROM incident_notes WHERE alert_id=? ORDER BY created_at',(alert_id,))]; c.close();
    if not a: raise HTTPException(404,'Alert not found')
    return {'alert':dict(a),'notes':notes}
@app.put('/api/alerts/{alert_id}/status')
def update_status(alert_id:str,s:Status):
    if s.status not in {'NEW','INVESTIGATING','RESOLVED','FALSE_POSITIVE'}: raise HTTPException(400,'Invalid status')
    c=connect(); cur=c.execute('UPDATE alerts SET status=? WHERE alert_id=?',(s.status,alert_id)); c.commit(); c.close();
    if cur.rowcount==0: raise HTTPException(404,'Alert not found')
    return {'status':s.status}
@app.post('/api/alerts/{alert_id}/notes')
def add_note(alert_id:str,n:Note):
    from datetime import datetime,timezone
    c=connect();
    if not c.execute('SELECT 1 FROM alerts WHERE alert_id=?',(alert_id,)).fetchone(): c.close(); raise HTTPException(404,'Alert not found')
    c.execute('INSERT INTO incident_notes(alert_id,note,created_at) VALUES(?,?,?)',(alert_id,n.note,datetime.now(timezone.utc).isoformat())); c.commit(); c.close(); return {'saved':True}
@app.get('/api/dashboard/stats')
def stats():
    c=connect(); total=c.execute('SELECT COUNT(*) FROM network_flows').fetchone()[0]; suspicious=c.execute("SELECT COUNT(*) FROM network_flows WHERE classification!='NORMAL'").fetchone()[0]; opena=c.execute("SELECT COUNT(*) FROM alerts WHERE status IN ('NEW','INVESTIGATING')").fetchone()[0]; critical=c.execute("SELECT COUNT(*) FROM alerts WHERE severity='CRITICAL' AND status!='RESOLVED'").fetchone()[0]; avg=c.execute('SELECT AVG(risk_score) FROM network_flows').fetchone()[0] or 0; c.close(); return {'total_flows':total,'suspicious_flows':suspicious,'open_alerts':opena,'critical_alerts':critical,'average_risk':round(avg,2)}
@app.get('/api/dashboard/traffic')
def traffic():
    c=connect(); rows=[dict(x) for x in c.execute("SELECT substr(timestamp,1,16) bucket, COUNT(*) count, SUM(CASE WHEN classification='NORMAL' THEN 1 ELSE 0 END) normal, SUM(CASE WHEN classification!='NORMAL' THEN 1 ELSE 0 END) suspicious FROM network_flows GROUP BY bucket ORDER BY bucket DESC LIMIT 60")]; c.close(); return list(reversed(rows))
@app.get('/api/dashboard/alerts')
def alert_stats():
    c=connect(); sev=[dict(x) for x in c.execute('SELECT severity,COUNT(*) count FROM alerts GROUP BY severity')]; typ=[dict(x) for x in c.execute('SELECT alert_type,COUNT(*) count FROM alerts GROUP BY alert_type ORDER BY count DESC')]; proto=[dict(x) for x in c.execute('SELECT protocol,COUNT(*) count FROM network_flows GROUP BY protocol')]; c.close(); return {'severity':sev,'types':typ,'protocols':proto}
@app.get('/api/rules')
def rules(): return [{'rule_id':k,**v,'enabled':True} for k,v in DEFAULT_RULES.items()]
