"""
Module: test_simulation.py
Description: Tests for waveform generator and fault injector
"""
import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation import waveform_generator, fault_injector
from processing import feature_extractor
from utils import config

class TestSimulation(unittest.TestCase):

    def test_generator(self):
        t, wave = waveform_generator.generate_sine_wave(frequency=50, duration=0.1)
        self.assertEqual(len(t), len(wave))
        self.assertAlmostEqual(feature_extractor.calculate_rms(wave), config.VOLTAGE_RMS, delta=1.0) 

    def test_sag_injection(self):
        t, wave = waveform_generator.generate_sine_wave()
        sagged_wave = fault_injector.inject_sag(wave, depth=0.5, start_ratio=0.0, end_ratio=1.0)
        rms = feature_extractor.calculate_rms(sagged_wave)
        expected = config.VOLTAGE_RMS * 0.5
        self.assertAlmostEqual(rms, expected, delta=1.0)
        
    def test_swell_injection(self):
        t, wave = waveform_generator.generate_sine_wave()
        swelled_wave = fault_injector.inject_swell(wave, magnitude=1.5, start_ratio=0.0, end_ratio=1.0)
        rms = feature_extractor.calculate_rms(swelled_wave)
        expected = config.VOLTAGE_RMS * 1.5
        self.assertAlmostEqual(rms, expected, delta=1.0)
