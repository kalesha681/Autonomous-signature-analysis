"""
Module: test_anomaly.py
Description: Tests for Anomaly Detection module
"""
import unittest
import numpy as np
import sys
import os
import shutil

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.anomaly_detector import AnomalyDetector

class TestAnomalyDetector(unittest.TestCase):

    def setUp(self):
        # Create dummy data
        self.normal_data = np.random.normal(loc=0.0, scale=1.0, size=(100, 2))
        self.detector = AnomalyDetector()
        
    def test_train_and_predict(self):
        # Train
        self.detector.train(self.normal_data)
        self.assertTrue(self.detector.is_trained)
        self.assertTrue(os.path.exists("data/models/isolation_forest.pkl"))
        
        # Predict Normal
        normal_sample = [0.1, 0.1]
        pred = self.detector.predict(normal_sample)
        self.assertEqual(pred, 1) # 1 is normal
        
        # Predict Anomaly (Huge outlier)
        anomaly_sample = [100.0, 100.0]
        pred = self.detector.predict(anomaly_sample)
        self.assertEqual(pred, -1) # -1 is anomaly

    def tearDown(self):
        # Cleanup model file
        pass 
