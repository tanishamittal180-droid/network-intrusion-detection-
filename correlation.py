from datetime import datetime

def correlate_alerts(alerts, window_seconds=60):
    groups={}
    for a in alerts:
        key=(a.get("source_ip"),a.get("alert_type")); groups.setdefault(key,[]).append(a)
    out=[]
    for key,items in groups.items():
        items=sorted(items,key=lambda x:x["timestamp"]); bucket=[]
        for a in items:
            t=datetime.fromisoformat(a["timestamp"].replace("Z","+00:00"))
            if not bucket or (t-datetime.fromisoformat(bucket[-1]["timestamp"].replace("Z","+00:00"))).total_seconds()<=window_seconds: bucket.append(a)
            else: out.append({"source_ip":key[0],"alert_type":key[1],"count":len(bucket),"alert_ids":[x["alert_id"] for x in bucket]}); bucket=[a]
        if bucket: out.append({"source_ip":key[0],"alert_type":key[1],"count":len(bucket),"alert_ids":[x["alert_id"] for x in bucket]})
    return out
