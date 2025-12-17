"""
Module: test_processing.py
Description: Tests for FFT and feature extraction
"""
import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation import waveform_generator, fault_injector
from processing import feature_extractor, fft_core
from utils import config

class TestProcessing(unittest.TestCase):

    def test_harmonics_thd(self):
        t, wave = waveform_generator.generate_sine_wave(frequency=50)
        # Inject huge harmonics
        harmonics = {3: 0.2} # 20% 3rd harmonic
        faulty_wave = fault_injector.inject_harmonics(t, wave, harmonics)
        
        thd = feature_extractor.calculate_thd(faulty_wave, fundamental_freq=50)
        self.assertGreater(thd, 0.15) # Should be around 0.2
        
    def test_fft_peak(self):
        t, wave = waveform_generator.generate_sine_wave(frequency=50)
        freqs, mags = fft_core.compute_fft(wave)
        
        peak_idx = np.argmax(mags)
        peak_freq = freqs[peak_idx]
        self.assertAlmostEqual(peak_freq, 50, delta=1.0)
