"""Generate safe synthetic network-flow records. No packets are transmitted."""
from pathlib import Path
import random
from datetime import datetime, timedelta, timezone
import ipaddress
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "data" / "network_traffic.csv"
R = random.Random(42)
SRC_NET = ipaddress.ip_network("192.0.2.0/24")
DST_NETS = [ipaddress.ip_network("198.51.100.0/24"), ipaddress.ip_network("203.0.113.0/24")]

SCENARIOS = [
    "NORMAL_WEB", "NORMAL_DNS", "NORMAL_SSH", "NORMAL_EMAIL", "NORMAL_DATABASE",
    "HIGH_CONNECTION_RATE", "REPEATED_FAILED_CONNECTIONS", "MULTI_PORT_PROBING_PATTERN",
    "SYN_HEAVY_PATTERN", "UNUSUAL_PORT_ACTIVITY", "HIGH_TRAFFIC_VOLUME"
]


def ip_from(net):
    hosts = list(net.hosts())
    return str(R.choice(hosts))


def normal_flow(ts):
    scenario = R.choice(SCENARIOS[:5])
    proto = "UDP" if scenario == "NORMAL_DNS" else "TCP"
    dport = {"NORMAL_WEB":443,"NORMAL_DNS":53,"NORMAL_SSH":22,"NORMAL_EMAIL":587,"NORMAL_DATABASE":5432}[scenario]
    packets = R.randint(5, 80)
    duration = round(R.uniform(0.2, 12), 3)
    avg = R.randint(300, 1400)
    return make(ts, scenario, "NORMAL", proto, dport, packets, packets*avg, duration, R.randint(1,4), 0, R.randint(0,4), 0)


def suspicious_flow(ts):
    scenario = R.choice(SCENARIOS[5:])
    if scenario == "HIGH_CONNECTION_RATE":
        return make(ts, scenario, "SUSPICIOUS", "TCP", R.choice([80,443]), R.randint(100,500), R.randint(50000,250000), R.uniform(0.2,2), R.randint(80,250), R.randint(0,10), R.randint(50,180), R.randint(0,3))
    if scenario == "REPEATED_FAILED_CONNECTIONS":
        return make(ts, scenario, "SUSPICIOUS", "TCP", R.choice([22,25,3389]), R.randint(20,100), R.randint(5000,40000), R.uniform(1,8), R.randint(20,90), R.randint(12,80), R.randint(10,50), R.randint(5,35))
    if scenario == "MULTI_PORT_PROBING_PATTERN":
        return make(ts, scenario, "SUSPICIOUS", "TCP", R.randint(1,65535), R.randint(20,120), R.randint(3000,70000), R.uniform(1,8), R.randint(20,100), R.randint(0,10), R.randint(30,100), R.randint(1,20))
    if scenario == "SYN_HEAVY_PATTERN":
        return make(ts, scenario, "SUSPICIOUS", "TCP", R.choice([80,443]), R.randint(80,300), R.randint(5000,50000), R.uniform(0.2,3), R.randint(50,220), R.randint(0,5), R.randint(60,280), R.randint(20,100))
    if scenario == "UNUSUAL_PORT_ACTIVITY":
        return make(ts, scenario, R.choice(["SUSPICIOUS","NORMAL"]), "TCP", R.choice([31337,4444,8081,9001]), R.randint(10,60), R.randint(3000,50000), R.uniform(0.5,10), R.randint(5,30), R.randint(0,8), R.randint(2,25), R.randint(0,8))
    return make(ts, scenario, "SUSPICIOUS", R.choice(["TCP","UDP"]), R.choice([443,8080,9000]), R.randint(500,5000), R.randint(1000000,10000000), R.uniform(1,10), R.randint(100,800), R.randint(0,30), R.randint(100,1500), R.randint(0,100))


def make(ts, scenario, label, proto, dport, packets, bytes_, duration, conns, fails, syns, rsts):
    src = ip_from(SRC_NET); dst = ip_from(R.choice(DST_NETS))
    return {
        "flow_id": f"FLW-{int(ts.timestamp()*1000)}-{R.randint(1000,9999)}",
        "timestamp": ts.isoformat(), "source_ip": src, "destination_ip": dst,
        "source_port": R.randint(1024,65535), "destination_port": int(dport), "protocol": proto,
        "packet_count": int(packets), "byte_count": int(bytes_), "duration_seconds": round(float(duration),3),
        "connection_count": int(conns), "failed_connection_count": int(fails), "syn_count": int(syns),
        "rst_count": int(rsts), "average_packet_size": round(bytes_/max(packets,1),2),
        "label": label, "scenario_type": scenario
    }


def generate(n=5000):
    now = datetime.now(timezone.utc) - timedelta(hours=24)
    rows=[]
    for i in range(n):
        ts = now + timedelta(seconds=i*17 + R.uniform(0,10))
        rows.append(suspicious_flow(ts) if R.random() < 0.30 else normal_flow(ts))
    df=pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True); df.to_csv(OUT,index=False)
    print(f"Generated {len(df)} records -> {OUT}")
    print(df["scenario_type"].value_counts().to_string())
    return df

if __name__ == "__main__": generate()
