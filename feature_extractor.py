"""Validation and network-flow feature engineering."""
import ipaddress
import math
import pandas as pd

NUMERIC = ["packet_count","byte_count","duration_seconds","bytes_per_second","packets_per_second","average_packet_size","connection_count","failed_connection_count","failure_ratio","syn_count","rst_count","syn_ratio","connection_rate"]


def _num(v, default=0.0):
    try:
        x=float(v); return x if math.isfinite(x) else default
    except (TypeError,ValueError): return default


def validate_flow(flow):
    for key in ("source_ip","destination_ip"):
        try: ipaddress.ip_address(str(flow.get(key,"")))
        except ValueError: raise ValueError(f"Invalid {key}")
    for key in ("source_port","destination_port"):
        p=int(flow.get(key,0))
        if not 0 <= p <= 65535: raise ValueError(f"Invalid {key}")
    if str(flow.get("protocol","")).upper() not in {"TCP","UDP","ICMP"}: raise ValueError("Unsupported protocol")


def extract_network_features(flow, context=None):
    validate_flow(flow)
    d=dict(flow)
    packets=max(_num(d.get("packet_count")),0); bytes_=max(_num(d.get("byte_count")),0)
    duration=max(_num(d.get("duration_seconds")),0.001); conns=max(_num(d.get("connection_count")),0)
    fails=max(_num(d.get("failed_connection_count")),0); syn=max(_num(d.get("syn_count")),0); rst=max(_num(d.get("rst_count")),0)
    f={**d, "packet_count":packets, "byte_count":bytes_, "duration_seconds":duration,
       "bytes_per_second":bytes_/duration, "packets_per_second":packets/duration,
       "average_packet_size":bytes_/max(packets,1), "failure_ratio":fails/max(conns,1),
       "syn_ratio":syn/max(packets,1), "connection_rate":conns/duration}
    if context:
        f["unique_destination_ports"]=context.get("unique_destination_ports",1)
        f["unique_destination_ips"]=context.get("unique_destination_ips",1)
    else:
        f["unique_destination_ports"]=1; f["unique_destination_ips"]=1
    return f


def dataframe_features(df):
    rows=[]
    for _,r in df.iterrows():
        rows.append(extract_network_features(r.to_dict()))
    return pd.DataFrame(rows)
