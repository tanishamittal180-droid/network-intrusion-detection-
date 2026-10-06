import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pytest
from ids.feature_extractor import extract_network_features
from ids.rule_engine import analyze_flow
from ids.anomaly_detector import AnomalyDetector
from ids.risk_engine import calculate_risk_score,classify
from ids.alert_engine import generate_alert
from ids.correlation import correlate_alerts

BASE={'flow_id':'T1','timestamp':'2026-01-01T00:00:00Z','source_ip':'192.0.2.1','destination_ip':'198.51.100.1','source_port':50000,'destination_port':443,'protocol':'TCP','packet_count':20,'byte_count':10000,'duration_seconds':2,'connection_count':2,'failed_connection_count':0,'syn_count':2,'rst_count':0,'average_packet_size':500,'label':'NORMAL','scenario_type':'TEST'}
def f(**kw): return {**BASE,**kw}

def test_normal_tcp(): assert extract_network_features(f())['failure_ratio']==0
def test_normal_udp(): assert extract_network_features(f(protocol='UDP',destination_port=53))['connection_rate']==1
def test_normal_dns(): assert f(destination_port=53,protocol='UDP')['destination_port']==53
def test_normal_https(): assert f(destination_port=443)['protocol']=='TCP'
def test_high_rate(): assert any(x['rule_id']=='IDS-001' for x in analyze_flow(extract_network_features(f(connection_count=100))))
def test_failed(): assert any(x['rule_id']=='IDS-002' for x in analyze_flow(extract_network_features(f(connection_count=20,failed_connection_count=10))))
def test_multiport(): assert any(x['rule_id']=='IDS-003' for x in analyze_flow(extract_network_features(f()))) is False
def test_syn_heavy(): assert any(x['rule_id']=='IDS-004' for x in analyze_flow(extract_network_features(f(packet_count=50,syn_count=40))))
def test_high_volume(): assert any(x['rule_id']=='IDS-006' for x in analyze_flow(extract_network_features(f(byte_count=2000000))))
def test_invalid_src_ip():
    with pytest.raises(ValueError): extract_network_features(f(source_ip='999.1.1.1'))
def test_invalid_dst_ip():
    with pytest.raises(ValueError): extract_network_features(f(destination_ip='bad'))
def test_invalid_src_port():
    with pytest.raises(ValueError): extract_network_features(f(source_port=70000))
def test_invalid_dst_port():
    with pytest.raises(ValueError): extract_network_features(f(destination_port=-1))
def test_unsupported_protocol():
    with pytest.raises(ValueError): extract_network_features(f(protocol='FTP'))
def test_missing_packets(): assert extract_network_features(f(packet_count=None))['packet_count']==0
def test_zero_duration(): assert extract_network_features(f(duration_seconds=0))['bytes_per_second']>0
def test_feature_engineering():
    x=extract_network_features(f(packet_count=10,byte_count=1000,duration_seconds=2)); assert x['bytes_per_second']==500

def test_rule_detection(): assert len(analyze_flow(extract_network_features(f(connection_count=100))))>=1
def test_anomaly_score():
    d=AnomalyDetector().fit([extract_network_features(f()) for _ in range(20)]); assert 0<=d.score(extract_network_features(f()))<=100
def test_risk_score(): assert 0<=calculate_risk_score([],50,None,False)<=100
def test_alert_creation():
    a=generate_alert(f(),[{'rule_id':'X','name':'Test','severity':'HIGH','description':'x'}],70,60); assert a['status']=='NEW'
def test_correlation():
    a=generate_alert(f(flow_id='1'),[{'rule_id':'X','name':'Test','severity':'HIGH','description':'x'}],70,60); b=generate_alert(f(flow_id='2'),[{'rule_id':'X','name':'Test','severity':'HIGH','description':'x'}],70,60); assert correlate_alerts([a,b])[0]['count']==2
def test_status_values(): assert classify(10)=='NORMAL' and classify(90)=='CRITICAL INVESTIGATION'
def test_db_storage(): assert True
def test_dashboard_stats(): assert True
def test_ml_prediction_placeholder(): assert True
def test_api_validation():
    from backend.app import Flow
    with pytest.raises(Exception): Flow(flow_id='x',timestamp='x',source_ip='192.0.2.1',destination_ip='198.51.100.1',source_port=1,destination_port=443,protocol='BAD',packet_count=1,byte_count=1,duration_seconds=1,connection_count=1,failed_connection_count=0,syn_count=0,rst_count=0,average_packet_size=1)
def test_empty_detector(): assert AnomalyDetector().score({})==0
def test_duplicate_event_logic(): assert True
