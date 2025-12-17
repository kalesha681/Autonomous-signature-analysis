"""
Module: fault_injector.py
Description: Implementation for fault_injector
"""

import numpy as np
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import config

def inject_sag(waveform, depth=0.5, start_ratio=0.3, end_ratio=0.7):
    """
    Simulates a voltage sag (dip).
    depth: Remaining voltage percentage (e.g., 0.5 means 50% drop)
    """
    n_samples = len(waveform)
    start_idx = int(n_samples * start_ratio)
    end_idx = int(n_samples * end_ratio)
    
    faulty_wave = waveform.copy()
    faulty_wave[start_idx:end_idx] *= depth
    return faulty_wave

def inject_swell(waveform, magnitude=1.5, start_ratio=0.3, end_ratio=0.7):
    """
    Simulates a voltage swell.
    magnitude: Multiplier (e.g., 1.5 means 150% voltage)
    """
    n_samples = len(waveform)
    start_idx = int(n_samples * start_ratio)
    end_idx = int(n_samples * end_ratio)
    
    faulty_wave = waveform.copy()
    faulty_wave[start_idx:end_idx] *= magnitude
    return faulty_wave

def inject_harmonics(t, waveform, harmonics_dict):
    """
    Injects harmonics.
    harmonics_dict: {order: magnitude_ratio}
    e.g. {3: 0.1, 5: 0.05} means 10% 3rd harmonic, 5% 5th harmonic relative to fundamental
    """
    fundamental_amp = config.VOLTAGE_RMS * np.sqrt(2)
    faulty_wave = waveform.copy()
    
    for order, ratio in harmonics_dict.items():
        harmonic_freq = config.FREQUENCY * order
        harmonic_wave = (fundamental_amp * ratio) * np.sin(2 * np.pi * harmonic_freq * t)
        faulty_wave += harmonic_wave
        
    return faulty_wave

def inject_noise(waveform, noise_level=0.01):
    """
    Adds Gaussian noise.
    """
    peak = config.VOLTAGE_RMS * np.sqrt(2)
    noise = np.random.normal(0, peak * noise_level, len(waveform))
    return waveform + noise
