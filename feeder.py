"""Safe local feeder: reads synthetic JSONL and POSTs records to localhost API."""
import argparse,json,time
from pathlib import Path
import requests

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',default='data/live_flows.jsonl');p.add_argument('--url',default='http://127.0.0.1:8000/api/flows');p.add_argument('--delay',type=float,default=.5);p.add_argument('--count',type=int,default=100);a=p.parse_args()
    rows=Path(a.input).read_text(encoding='utf-8').splitlines()[-a.count:]
    for line in rows:
        r=requests.post(a.url,json=json.loads(line),timeout=5);print(r.status_code,r.json());time.sleep(a.delay)
if __name__=='__main__':main()
