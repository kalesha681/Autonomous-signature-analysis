"""
Module: waveform_generator.py
Description: Implementation for waveform_generator
"""

import numpy as np
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import config

def generate_sine_wave(frequency=config.FREQUENCY, sampling_rate=config.SAMPLING_RATE, duration=config.DURATION, amplitude=None):
    """
    Generates a pure sine wave.
    """
    if amplitude is None:
        amplitude = config.VOLTAGE_RMS * np.sqrt(2) # Peak voltage
    
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    waveform = amplitude * np.sin(2 * np.pi * frequency * t)
    return t, waveform
