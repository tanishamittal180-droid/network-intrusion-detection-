"""Hybrid rule + anomaly + optional ML risk scoring."""
def calculate_risk_score(rule_hits, anomaly_score, ml_probability=None, ml_enabled=True, weights=None):
    rule_score=min(100,len(rule_hits)*35)
    if ml_enabled and ml_probability is not None:
        w=weights or {"rules":.4,"anomaly":.3,"ml":.3}
        score=rule_score*w["rules"]+float(anomaly_score)*w["anomaly"]+float(ml_probability)*100*w["ml"]
    else:
        w=weights or {"rules":.6,"anomaly":.4}
        score=rule_score*w["rules"]+float(anomaly_score)*w["anomaly"]
    return round(max(0,min(100,score)),2)

def classify(score):
    if score<=20:return "NORMAL"
    if score<=40:return "LOW RISK"
    if score<=60:return "SUSPICIOUS"
    if score<=80:return "HIGH RISK"
    return "CRITICAL INVESTIGATION"

def severity(score, hits):
    if any(h["severity"]=="HIGH" for h in hits) or score>80:return "HIGH" if score<=80 else "CRITICAL"
    if score>60:return "HIGH"
    if score>40:return "MEDIUM"
    if score>20:return "LOW"
    return "INFO"
