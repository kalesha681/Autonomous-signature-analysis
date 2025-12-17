"""
Module: test_inference.py
Description: Tests for predictor logic
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference import predictor_core, signatures
from utils import config

class TestInference(unittest.TestCase):

    def test_diagnosis_logic(self):
        # Normal
        status = predictor_core.diagnose(config.VOLTAGE_RMS, 0.01)
        self.assertEqual(status, signatures.get_status_messages()["NORMAL"])
        
        # Sag only
        status = predictor_core.diagnose(config.VOLTAGE_RMS * 0.8, 0.01)
        self.assertIn("Sag", status)
        self.assertNotIn("Harmonic", status)
        
        # Harmonic only
        status = predictor_core.diagnose(config.VOLTAGE_RMS, 0.10)
        self.assertIn("Harmonic", status)
        self.assertNotIn("Sag", status)
        
        # Multi-Fault: Sag AND Harmonic
        status = predictor_core.diagnose(config.VOLTAGE_RMS * 0.8, 0.10)
        self.assertIn("Sag", status)
        self.assertIn("Harmonic", status)
        self.assertIn("|", status)
