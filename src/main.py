from log_analyzer import LogAnalyzer
import json
from datetime import datetime
import time

def analyze_logs():
    analyzer = LogAnalyzer(contamination=0.05)
    
    with open('logs.json', 'r') as f:
        logs = json.load(f)
    
    analyzer.fit(logs)
    results = analyzer.detect_anomalies(logs)
    anomalies = [r for r in results if r['is_anomaly']]
    
    print(f"\nTotal logs analyzed: {len(logs)}")
    print(f"Anomalies detected: {len(anomalies)}")
    
    if anomalies:
        print("\nTop 5 Most Critical Anomalies:")
        sorted_anomalies = sorted(anomalies, key=lambda x: x['anomaly_score'])[:5]
        
        for anomaly in sorted_anomalies:
            print(f"\nTimestamp: {anomaly['log_entry']['timestamp']}")
            print(f"Service: {anomaly['log_entry']['service']}")
            print(f"Level: {anomaly['log_entry']['level']}")
            print(f"Message: {anomaly['log_entry']['message']}")
            print(f"Anomaly Score: {anomaly['anomaly_score']:.3f}")

if __name__ == "__main__":
    analyze_logs()