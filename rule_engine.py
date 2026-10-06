"""Explainable, configurable defensive signatures over flow records."""
DEFAULT_RULES={
 "IDS-001":{"name":"High Connection Rate","severity":"HIGH","threshold":30},
 "IDS-002":{"name":"Repeated Failed Connections","severity":"HIGH","threshold":0.35},
 "IDS-003":{"name":"Multi-Port Probing Pattern","severity":"MEDIUM","threshold":20},
 "IDS-004":{"name":"SYN-Heavy Pattern","severity":"HIGH","threshold":0.60},
 "IDS-005":{"name":"Unusual Service Port","severity":"MEDIUM","threshold":0},
 "IDS-006":{"name":"High Traffic Volume","severity":"HIGH","threshold":1000000},
}
UNUSUAL={31337,4444,8081,9001,12345}

def analyze_flow(f, rules=None):
    rules=rules or DEFAULT_RULES; hits=[]
    if f.get("connection_rate",0)>rules["IDS-001"]["threshold"]: hits.append(hit("IDS-001",rules["IDS-001"],"Connection rate exceeded baseline."))
    if f.get("failure_ratio",0)>=rules["IDS-002"]["threshold"] and f.get("failed_connection_count",0)>=3: hits.append(hit("IDS-002",rules["IDS-002"],"Failure ratio and failed connection count are elevated."))
    if f.get("unique_destination_ports",1)>=rules["IDS-003"]["threshold"]: hits.append(hit("IDS-003",rules["IDS-003"],"Source contacted many destination ports in the observation window."))
    if f.get("syn_ratio",0)>=rules["IDS-004"]["threshold"] and f.get("syn_count",0)>=20: hits.append(hit("IDS-004",rules["IDS-004"],"SYN share is unusually high relative to packets."))
    if int(f.get("destination_port",0)) in UNUSUAL: hits.append(hit("IDS-005",rules["IDS-005"],"Destination port is outside the project's common service-port set."))
    if f.get("byte_count",0)>=rules["IDS-006"]["threshold"]: hits.append(hit("IDS-006",rules["IDS-006"],"Observed byte volume is unusually high."))
    return hits

def hit(rule_id,rule,reason): return {"rule_id":rule_id,"name":rule["name"],"severity":rule["severity"],"description":reason}
