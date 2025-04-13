from log_anomaly_detector import LogAnomalyDetector
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_logs(n_samples=1000):
    """Generate sample log data for demonstration"""
    np.random.seed(42)
    
    # Generate timestamps
    start_date = datetime.now() - timedelta(days=7)
    timestamps = [start_date + timedelta(minutes=i) for i in range(n_samples)]
    
    # Generate log levels
    levels = np.random.choice(['INFO', 'WARNING', 'ERROR', 'DEBUG'], 
                            size=n_samples, 
                            p=[0.7, 0.15, 0.1, 0.05])
    
    # Generate messages
    normal_length = np.random.normal(50, 10, n_samples)
    # Add some anomalies
    anomaly_indices = np.random.choice(n_samples, size=int(n_samples * 0.1), replace=False)
    normal_length[anomaly_indices] = np.random.normal(200, 50, len(anomaly_indices))
    
    messages = [f"Log message with length {int(abs(length))}" * (int(abs(length))//20 + 1) 
               for length in normal_length]
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'level': levels,
        'message': messages
    })

def main():
    # Generate sample log data
    print("Generating sample log data...")
    log_data = generate_sample_logs()
    
    # Initialize and train the anomaly detector
    print("Training anomaly detector...")
    detector = LogAnomalyDetector(contamination=0.1)
    detector.fit(log_data)
    
    # Predict anomalies
    print("Detecting anomalies...")
    predictions = detector.predict(log_data)
    anomaly_scores = detector.predict_score(log_data)
    
    # Add predictions to the dataframe
    log_data['is_anomaly'] = predictions == -1
    log_data['anomaly_score'] = anomaly_scores
    
    # Print summary
    print("\nAnalysis Summary:")
    print(f"Total log entries: {len(log_data)}")
    print(f"Detected anomalies: {sum(log_data['is_anomaly'])} ({sum(log_data['is_anomaly'])/len(log_data)*100:.2f}%)")
    
    # Display some example anomalies
    print("\nExample anomalies:")
    anomalies = log_data[log_data['is_anomaly']].head()
    print(anomalies[['timestamp', 'level', 'message', 'anomaly_score']])
    
    # Visualize the results
    print("\nGenerating visualization...")
    detector.visualize_anomalies(log_data, predictions)

if __name__ == "__main__":
    main() 