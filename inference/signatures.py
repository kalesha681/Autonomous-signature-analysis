"""
Module: signatures.py
Description: Definitions of fault signatures and operating thresholds
"""
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import config

# Thresholds can be derived from config or defined explicitly here if they are rule constants
SAG_THRESHOLD = config.SAG_THRESHOLD
SWELL_THRESHOLD = config.SWELL_THRESHOLD
THD_THRESHOLD = config.THD_THRESHOLD

def get_status_messages():
    return {
        "SAG": "WARNING: Voltage Sag Detected",
        "SWELL": "WARNING: Voltage Swell Detected",
        "HARMONIC": "WARNING: Harmonic Fault Detected",
        "NORMAL": "Normal Operation"
    }
