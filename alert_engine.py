from datetime import datetime, timezone
import uuid

def generate_alert(flow, hits, risk, anomaly, ml_probability=None):
    if not hits and risk<=20:return None
    return {"alert_id":"ALT-"+uuid.uuid4().hex[:8].upper(),"timestamp":datetime.now(timezone.utc).isoformat(),"flow_id":flow["flow_id"],"source_ip":flow["source_ip"],"destination_ip":flow["destination_ip"],"protocol":flow["protocol"],"source_port":flow["source_port"],"destination_port":flow["destination_port"],"rule_id":hits[0]["rule_id"] if hits else "ANOM-001","alert_type":hits[0]["name"] if hits else "Behavioral Anomaly","severity":__import__('ids.risk_engine',fromlist=['severity']).severity(risk,hits),"risk_score":risk,"anomaly_score":anomaly,"ml_probability":ml_probability,"description":"; ".join(h["description"] for h in hits) or "Flow deviated from the normal baseline.","status":"NEW"}
