"""Baseline anomaly scoring using robust z-score/IQR style deviations."""
import numpy as np
FEATURES=["packets_per_second","bytes_per_second","connection_rate","failure_ratio","unique_destination_ports"]

class AnomalyDetector:
    def __init__(self): self.stats={}
    def fit(self, rows):
        for col in FEATURES:
            vals=np.array([float(r.get(col,0)) for r in rows],dtype=float)
            q1,q3=np.percentile(vals,[25,75]); med=float(np.median(vals)); std=float(np.std(vals))
            self.stats[col]={"median":med,"iqr":max(q3-q1,1e-9),"std":max(std,1e-9)}
        return self
    def score(self,row):
        if not self.stats: return 0.0
        deviations=[]
        for col,s in self.stats.items():
            x=float(row.get(col,0)); z=abs(x-s["median"])/(1.4826*s["iqr"]+1e-9)
            deviations.append(min(z,10)/10)
        return round(float(np.mean(deviations)*100),2)
