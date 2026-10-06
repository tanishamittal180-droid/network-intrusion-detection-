from ids.feature_extractor import extract_network_features
from ids.rule_engine import analyze_flow
from ids.anomaly_detector import AnomalyDetector
from ids.risk_engine import calculate_risk_score,classify
from ids.alert_engine import generate_alert

class IDSService:
    def __init__(self): self.detector=AnomalyDetector()
    def fit(self, rows): self.detector.fit([extract_network_features(r) for r in rows])
    def analyze(self, flow):
        f=extract_network_features(flow); hits=analyze_flow(f); anomaly=self.detector.score(f); risk=calculate_risk_score(hits,anomaly,None,False); alert=generate_alert(flow,hits,risk,anomaly); return f,hits,anomaly,risk,classify(risk),alert
