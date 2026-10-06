import os,sqlite3
DB=os.getenv('IDS_DB_PATH','ids.db')

def connect():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init_db():
    c=connect(); c.executescript('''CREATE TABLE IF NOT EXISTS network_flows(flow_id TEXT PRIMARY KEY,timestamp TEXT,source_ip TEXT,destination_ip TEXT,source_port INTEGER,destination_port INTEGER,protocol TEXT,packet_count INTEGER,byte_count INTEGER,duration REAL,risk_score REAL,classification TEXT); CREATE TABLE IF NOT EXISTS alerts(alert_id TEXT PRIMARY KEY,flow_id TEXT,rule_id TEXT,severity TEXT,alert_type TEXT,description TEXT,risk_score REAL,status TEXT,created_at TEXT,source_ip TEXT,destination_ip TEXT,protocol TEXT,source_port INTEGER,destination_port INTEGER,anomaly_score REAL,ml_probability REAL); CREATE TABLE IF NOT EXISTS rules(rule_id TEXT PRIMARY KEY,rule_name TEXT,description TEXT,severity TEXT,threshold REAL,enabled INTEGER); CREATE TABLE IF NOT EXISTS incident_notes(note_id INTEGER PRIMARY KEY AUTOINCREMENT,alert_id TEXT,note TEXT,created_at TEXT); CREATE INDEX IF NOT EXISTS idx_alerts_created ON alerts(created_at); CREATE INDEX IF NOT EXISTS idx_alerts_source ON alerts(source_ip);'''); c.commit(); c.close()
