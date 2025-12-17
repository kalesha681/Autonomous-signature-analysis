"""
Module: feature_extractor.py
Description: Implementation for feature_extractor
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import config
from processing import fft_core

def calculate_rms(waveform):
    """Calculates Root Mean Square (RMS) voltage."""
    return np.sqrt(np.mean(waveform**2))

def calculate_peak(waveform):
    """Calculates Peak voltage."""
    return np.max(np.abs(waveform))

def calculate_thd(waveform, fundamental_freq=config.FREQUENCY, sampling_rate=config.SAMPLING_RATE):
    """
    Calculates Total Harmonic Distortion (THD).
    THD = sqrt(sum(V_n^2)) / V_fundamental
    """
    frequencies, magnitudes = fft_core.compute_fft(waveform, sampling_rate)
    
    # Find index of fundamental frequency
    idx = (np.abs(frequencies - fundamental_freq)).argmin()
    fundamental_amp = magnitudes[idx]
    
    if fundamental_amp == 0:
        return 0.0

    # Sum of squares of harmonic components (ignore DC and fundamental)
    # Using a small window around fundamental to exclude it
    window = 5 # indices
    harmonics_sq_sum = np.sum(magnitudes**2) - np.sum(magnitudes[max(0, idx-window):idx+window]**2)
    
    # Also remove DC component (near 0 Hz)
    dc_idx = (np.abs(frequencies - 0)).argmin()
    harmonics_sq_sum -= np.sum(magnitudes[max(0, dc_idx-window):dc_idx+window]**2)
    
    if harmonics_sq_sum < 0: harmonics_sq_sum = 0 # Numerical noise
    
    thd = np.sqrt(harmonics_sq_sum) / fundamental_amp
    return thd
