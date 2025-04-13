import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
from tqdm import tqdm

class LogAnomalyDetector:
    def __init__(self, contamination=0.1, random_state=42):
        """
        Initialize the Log Anomaly Detector
        
        Args:
            contamination (float): The proportion of outliers in the dataset
            random_state (int): Random state for reproducibility
        """
        self.contamination = contamination
        self.random_state = random_state
        self.isolation_forest = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1
        )
        self.scaler = StandardScaler()
        self.service_encoder = LabelEncoder()
        
    def extract_features(self, log_data):
        """
        Extract numerical features from log data
        
        Args:
            log_data (pd.DataFrame): DataFrame containing log entries
            
        Returns:
            pd.DataFrame: DataFrame with extracted features
        """
        features = pd.DataFrame()
        
        # Extract timestamp-based features
        if 'timestamp' in log_data.columns:
            log_data['timestamp'] = pd.to_datetime(log_data['timestamp'])
            features['hour'] = log_data['timestamp'].dt.hour
            features['minute'] = log_data['timestamp'].dt.minute
            features['day_of_week'] = log_data['timestamp'].dt.dayofweek
        
        # Extract message length
        if 'message' in log_data.columns:
            features['message_length'] = log_data['message'].str.len()
            
        # Extract log level severity (if exists)
        if 'level' in log_data.columns:
            level_mapping = {
                'DEBUG': 1,
                'INFO': 2,
                'WARNING': 3,
                'ERROR': 4,
                'CRITICAL': 5
            }
            features['severity'] = log_data['level'].map(level_mapping).fillna(0)
        
        # Extract service information (if exists)
        if 'service' in log_data.columns:
            # Use LabelEncoder to convert service names to numeric values
            if not hasattr(self, 'service_encoder_fitted'):
                features['service_encoded'] = self.service_encoder.fit_transform(log_data['service'])
                self.service_encoder_fitted = True
            else:
                # Handle new services not seen during training
                try:
                    features['service_encoded'] = self.service_encoder.transform(log_data['service'])
                except ValueError:
                    # If new services are found, add them to the encoder
                    all_services = list(self.service_encoder.classes_) + list(set(log_data['service']) - set(self.service_encoder.classes_))
                    self.service_encoder = LabelEncoder().fit(all_services)
                    features['service_encoded'] = self.service_encoder.transform(log_data['service'])
            
        return features
    
    def fit(self, log_data):
        """
        Fit the anomaly detection model
        
        Args:
            log_data (pd.DataFrame): DataFrame containing log entries
        """
        features = self.extract_features(log_data)
        scaled_features = self.scaler.fit_transform(features)
        self.isolation_forest.fit(scaled_features)
        
    def predict(self, log_data):
        """
        Predict anomalies in log data
        
        Args:
            log_data (pd.DataFrame): DataFrame containing log entries
            
        Returns:
            np.array: Array of predictions (-1 for anomalies, 1 for normal entries)
        """
        features = self.extract_features(log_data)
        scaled_features = self.scaler.transform(features)
        return self.isolation_forest.predict(scaled_features)
    
    def predict_score(self, log_data):
        """
        Get anomaly scores for log entries
        
        Args:
            log_data (pd.DataFrame): DataFrame containing log entries
            
        Returns:
            np.array: Array of anomaly scores
        """
        features = self.extract_features(log_data)
        scaled_features = self.scaler.transform(features)
        return self.isolation_forest.score_samples(scaled_features)
    
    def visualize_anomalies(self, log_data, predictions):
        """
        Visualize detected anomalies
        
        Args:
            log_data (pd.DataFrame): DataFrame containing log entries
            predictions (np.array): Array of predictions from the model
        """
        features = self.extract_features(log_data)
        
        plt.figure(figsize=(15, 8))
        
        if 'timestamp' in log_data.columns:
            plt.scatter(log_data['timestamp'], features['message_length'],
                       c=predictions, cmap='viridis')
            plt.xlabel('Timestamp')
            plt.ylabel('Message Length')
            plt.title('Log Anomalies Detection Results')
            plt.colorbar(label='Anomaly Score')
        
        plt.tight_layout()
        plt.show() 