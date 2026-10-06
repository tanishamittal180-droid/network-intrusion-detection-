from pathlib import Path
import joblib,pandas as pd
from ids.feature_extractor import extract_network_features

def predict(flow):
    root=Path(__file__).resolve().parents[1]; bundle=joblib.load(root/'models/ids_rf.joblib'); f=extract_network_features(flow); X=pd.DataFrame([f])[bundle['features']].fillna(0); return float(bundle['model'].predict_proba(X)[0,1])
