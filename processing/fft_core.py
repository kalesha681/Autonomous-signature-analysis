"""
Module: fft_core.py
Description: Implementation for fft_core
"""

import numpy as np
from scipy.fft import fft, fftfreq
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import config

def compute_fft(waveform, sampling_rate=config.SAMPLING_RATE):
    """
    Performs FFT analysis.
    Returns: frequencies, magnitudes
    """
    N = len(waveform)
    yf = fft(waveform)
    xf = fftfreq(N, 1 / sampling_rate)
    
    # Return only positive frequencies
    positive_indices = xf >= 0
    magnitudes = 2.0/N * np.abs(yf[positive_indices])
    frequencies = xf[positive_indices]
    
    return frequencies, magnitudes
