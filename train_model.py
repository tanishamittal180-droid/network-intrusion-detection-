"""Train a Random Forest on the synthetic dataset and report real metrics."""
from pathlib import Path
import joblib,pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,classification_report
from ids.feature_extractor import dataframe_features
FEATURES=["packet_count","byte_count","duration_seconds","bytes_per_second","packets_per_second","average_packet_size","connection_count","failed_connection_count","failure_ratio","syn_count","rst_count","syn_ratio","connection_rate"]

def train():
    root=Path(__file__).resolve().parents[1]; df=pd.read_csv(root/'data/network_traffic.csv'); f=dataframe_features(df); X=f[FEATURES].fillna(0); y=(df.label=='SUSPICIOUS').astype(int)
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
    model=RandomForestClassifier(n_estimators=200,max_depth=16,class_weight='balanced',random_state=42,n_jobs=-1); model.fit(Xtr,ytr); p=model.predict(Xte)
    print(classification_report(yte,p,target_names=['NORMAL','SUSPICIOUS'])); print('Accuracy:',accuracy_score(yte,p)); print('Precision:',precision_score(yte,p)); print('Recall:',recall_score(yte,p)); print('F1:',f1_score(yte,p)); print('Confusion matrix:\n',confusion_matrix(yte,p))
    (root/'models').mkdir(exist_ok=True); joblib.dump({'model':model,'features':FEATURES},root/'models/ids_rf.joblib')
if __name__=='__main__': train()
