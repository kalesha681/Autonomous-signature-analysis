"""
Module: app_main.py
Description: Main entry point for the Streamlit dashboard
"""
import streamlit as st
import time
import sys
import os
import numpy as np

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation import waveform_generator, fault_injector
from processing import feature_extractor, fft_core
from inference import predictor_core
from inference.anomaly_detector import AnomalyDetector
from dashboard import components, visualizations
from utils import config

# Config should be set first
st.set_page_config(page_title="Smart Meter with a Brain", page_icon="⚡", layout="wide")

st.title("⚡ Smart Meter 'Edge AI' Prototype")
st.markdown("Real-time Power Quality Analysis & Fault Classification")

# Render Sidebar
freq, noise_level, fault_type = components.render_sidebar()
sag_depth, swell_mag, harmonics = components.get_fault_params(fault_type)

st.sidebar.divider()
st.sidebar.subheader("Advanced AI")
if st.sidebar.button("Train Anomaly Model"):
    # Train on 100 random normal samples
    features = []
    for _ in range(100):
        t, w = waveform_generator.generate_sine_wave(frequency=50) # Normal
        w = fault_injector.inject_noise(w, noise_level=0.01)
        r = feature_extractor.calculate_rms(w)
        th = feature_extractor.calculate_thd(w, 50)
        features.append([r, th])
    
    ad = AnomalyDetector()
    ad.train(features)
    st.sidebar.success("Model Trained on Normal Data!")

# Live Mode Toggle
live_mode = st.sidebar.checkbox("Start Live Simulation", value=False)

def run_cycle():
    # 1. Generat
    t, waveform = waveform_generator.generate_sine_wave(frequency=freq)

    # 2. Inject Faults
    if fault_type == "Sag":
        waveform = fault_injector.inject_sag(waveform, depth=sag_depth)
    elif fault_type == "Swell":
        waveform = fault_injector.inject_swell(waveform, magnitude=swell_mag)
    elif fault_type == "Harmonics":
        waveform = fault_injector.inject_harmonics(t, waveform, harmonics)

    # Random jitter in live mode to make it look alive
    if live_mode:
        noise_jitter = np.random.uniform(0.8, 1.2)
        waveform = fault_injector.inject_noise(waveform, noise_level=noise_level * noise_jitter)
        # Shift phase slightly? No need, random noise is enough for visual jitter
    else:
        waveform = fault_injector.inject_noise(waveform, noise_level=noise_level)

    # 3. Process
    rms_val = feature_extractor.calculate_rms(waveform)
    thd_val = feature_extractor.calculate_thd(waveform, fundamental_freq=freq)
    fft_freqs, fft_mags = fft_core.compute_fft(waveform)

    # 4. Infer
    diagnosis = predictor_core.diagnose(rms_val, thd_val)

    return t, waveform, fft_freqs, fft_mags, rms_val, thd_val, diagnosis

# Main Loop Area
placeholder = st.empty()

if live_mode:
    # Run loop
    while True:
        t, wave, f_f, f_m, rms, thd, diag = run_cycle()
        
        with placeholder.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.plotly_chart(visualizations.plot_time_domain(t, wave), use_container_width=True, key=f"time_{time.time()}")
                st.plotly_chart(visualizations.plot_frequency_domain(f_f, f_m), use_container_width=True, key=f"freq_{time.time()}")
            with col2:
                components.render_metrics(rms, thd, diag, config)
        
        time.sleep(0.5) # Update every 0.5s
else:
    # Single run
    t, wave, f_f, f_m, rms, thd, diag = run_cycle()
    with placeholder.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.plotly_chart(visualizations.plot_time_domain(t, wave), use_container_width=True)
            st.plotly_chart(visualizations.plot_frequency_domain(f_f, f_m), use_container_width=True)
        with col2:
            components.render_metrics(rms, thd, diag, config)
