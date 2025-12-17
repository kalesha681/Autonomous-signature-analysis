"""
Module: predictor_core.py
Description: Implementation for predictor_core
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inference import signatures
# Lazy import/init of anomaly detector
from inference.anomaly_detector import AnomalyDetector

# Singleton instance
detector = AnomalyDetector()

def diagnose(rms, thd):
    """
    Classifies the signal state based on extracted features.
    Returns a status string. Can return multiple faults joined by ' | '.
    """
    msgs = signatures.get_status_messages()
    issues = []
    
    # 1. Check Rule-Based (Deterministic knowledge)
    if rms < signatures.SAG_THRESHOLD:
        issues.append(msgs["SAG"])
    elif rms > signatures.SWELL_THRESHOLD:
        issues.append(msgs["SWELL"])
    
    if thd > signatures.THD_THRESHOLD:
        issues.append(msgs["HARMONIC"])
    
    # 2. Check Anomaly Detector (Unsupervised / Unknown Faults)
    is_normal = detector.predict([rms, thd])
    if is_normal == -1:
        issues.append("WARNING: Unknown Anomaly Detected (AI)")
    
    # Return Logic
    if not issues:
        return msgs["NORMAL"]
        
    return " | ".join(issues)
