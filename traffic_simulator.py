"""Continuous synthetic flow producer. It writes JSONL only; it never sends packets."""
import argparse,json,random,time
from datetime import datetime,timezone
from pathlib import Path
from simulator.generate_dataset import normal_flow,suspicious_flow

def main():
    p=argparse.ArgumentParser(); p.add_argument('--mode',choices=['normal','mixed'],default='mixed'); p.add_argument('--speed',choices=['slow','fast'],default='slow'); p.add_argument('--count',type=int,default=0); p.add_argument('--output',default='data/live_flows.jsonl'); a=p.parse_args()
    Path(a.output).parent.mkdir(parents=True,exist_ok=True); delay=1.0 if a.speed=='slow' else .2; i=0
    with open(a.output,'a',encoding='utf-8') as out:
        while not a.count or i<a.count:
            row=suspicious_flow(datetime.now(timezone.utc)) if a.mode=='mixed' and random.random()<.3 else normal_flow(datetime.now(timezone.utc))
            out.write(json.dumps(row)+'\n'); out.flush(); print(row); i+=1; time.sleep(delay)
if __name__=='__main__': main()
