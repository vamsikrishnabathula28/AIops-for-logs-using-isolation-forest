from sklearn.ensemble import IsolationForest
import numpy as np

class LogAnalyzer:
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        
    def extract_features(self, log_entry):
        features = [
            log_entry['response_time'],
            int(str(log_entry['status_code'])[0]),
            1 if log_entry['level'] == 'ERROR' else 0,
            1 if log_entry['level'] == 'WARNING' else 0
        ]
        return features
    
    def fit(self, logs):
        features = np.array([self.extract_features(log) for log in logs])
        self.model.fit(features)
        
    def detect_anomalies(self, logs):
        features = np.array([self.extract_features(log) for log in logs])
        predictions = self.model.predict(features)
        scores = self.model.score_samples(features)
        
        results = []
        for i, log in enumerate(logs):
            results.append({
                'log_entry': log,
                'is_anomaly': predictions[i] == -1,
                'anomaly_score': scores[i]
            })
        return results