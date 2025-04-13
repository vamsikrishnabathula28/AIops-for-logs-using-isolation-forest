import pandas as pd
import argparse
import re
from datetime import datetime
import os
from log_anomaly_detector import LogAnomalyDetector

def parse_log_line(line):
    """
    Parse a log line into timestamp, service, level, and message components.
    This function assumes a log format like:
    Timestamp: 2025-04-13T23:41:37.368054
    Service: web
    Level: ERROR
    Message: Authentication failed
    """
    # Initialize variables
    timestamp = None
    service = None
    level = None
    message = None
    
    # Split the line by colon
    parts = line.strip().split(':', 1)
    if len(parts) != 2:
        return None, None, None, None
    
    key, value = parts
    key = key.strip()
    value = value.strip()
    
    if key == "Timestamp":
        try:
            timestamp = datetime.fromisoformat(value)
        except ValueError:
            return None, None, None, None
    elif key == "Service":
        service = value
    elif key == "Level":
        level = value
    elif key == "Message":
        message = value
    
    return timestamp, service, level, message

def load_log_file(file_path):
    """
    Load a log file and convert it to a pandas DataFrame with the required columns.
    """
    log_entries = []
    current_entry = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:  # Empty line indicates end of a log entry
                if current_entry and all(k in current_entry for k in ['timestamp', 'service', 'level', 'message']):
                    log_entries.append(current_entry)
                current_entry = {}
                continue
                
            timestamp, service, level, message = parse_log_line(line)
            
            if timestamp:
                current_entry['timestamp'] = timestamp
            if service:
                current_entry['service'] = service
            if level:
                current_entry['level'] = level
            if message:
                current_entry['message'] = message
    
    # Add the last entry if it exists
    if current_entry and all(k in current_entry for k in ['timestamp', 'service', 'level', 'message']):
        log_entries.append(current_entry)
    
    return pd.DataFrame(log_entries)

def format_output(log_data):
    """
    Format the output according to the user's requirements.
    """
    output = []
    for _, row in log_data.iterrows():
        entry = (
            f"Timestamp: {row['timestamp'].isoformat()}\n"
            f"Service: {row['service']}\n"
            f"Level: {row['level']}\n"
            f"Message: {row['message']}\n"
            f"Anomaly Score: {row['anomaly_score']:.3f}\n"
        )
        output.append(entry)
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description='Process log files for anomaly detection')
    parser.add_argument('log_file', help='Path to the log file to analyze')
    parser.add_argument('--contamination', type=float, default=0.1, 
                        help='Expected proportion of outliers (default: 0.1)')
    parser.add_argument('--output', help='Path to save the results (CSV format)')
    args = parser.parse_args()
    
    print(f"Loading log file: {args.log_file}")
    log_data = load_log_file(args.log_file)
    
    if log_data.empty:
        print("No valid log entries found. Please check your log format.")
        return
    
    print(f"Loaded {len(log_data)} log entries")
    print(f"Log levels found: {log_data['level'].unique()}")
    
    # Initialize and train the anomaly detector
    print("Training anomaly detector...")
    detector = LogAnomalyDetector(contamination=args.contamination)
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
    
    # Display results in the desired format
    print("\nAnomaly Detection Results:")
    print(format_output(log_data[log_data['is_anomaly']].head()))
    
    # Save results if output path is provided
    if args.output:
        if args.output.endswith('.csv'):
            log_data.to_csv(args.output, index=False)
            print(f"\nResults saved to: {args.output}")
        else:
            with open(args.output, 'w') as f:
                f.write(format_output(log_data))
            print(f"\nResults saved to: {args.output}")
    
    # Visualize the results
    print("\nGenerating visualization...")
    detector.visualize_anomalies(log_data, predictions)

if __name__ == "__main__":
    main() 