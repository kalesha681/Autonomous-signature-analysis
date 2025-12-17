"""
Module: anomaly_detector.py
Description: Unsupervised Anomaly Detection using Isolation Forest
"""
import numpy as np
from sklearn.ensemble import IsolationForest
import pickle
import os

MODEL_PATH = "data/models/isolation_forest.pkl"

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False
        
    def train(self, X):
        """
        Train the model on normal data.
        X: Feature matrix (n_samples, n_features)
        """
        self.model.fit(X)
        self.is_trained = True
        self.save_model()
        
    def predict(self, features):
        """
        Predict if a sample is anomalous.
        features: [rms, thd, peak, etc.]
        Returns: -1 for anomaly, 1 for normal
        """
        if not self.is_trained:
            self.load_model()
            
        if not self.is_trained:
            return 1 # Default to normal if no model
            
        # Reshape for single prediction
        X = np.array(features).reshape(1, -1)
        return self.model.predict(X)[0]
    
    def save_model(self):
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(self.model, f)
            
    def load_model(self):
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
            self.is_trained = True
