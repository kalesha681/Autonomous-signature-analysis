"""
Module: components.py
Description: Reusable UI components
"""
import streamlit as st
from simulation import waveform_generator, fault_injector

def render_sidebar():
    st.sidebar.header("Simulation Settings")

    # 1. Base Waveform
    st.sidebar.subheader("Generator")
    freq = st.sidebar.slider("Frequency (Hz)", 40, 70, 50)
    noise_level = st.sidebar.slider("Noise Level", 0.0, 0.1, 0.01)

    # 2. Fault Injection
    st.sidebar.subheader("Fault Injection")
    fault_type = st.sidebar.selectbox("Inject Fault", ["None", "Sag", "Swell", "Harmonics"])
    
    return freq, noise_level, fault_type

def get_fault_params(fault_type):
    sag_depth = 0.5
    swell_mag = 1.5
    harmonics = {}

    if fault_type == "Sag":
        sag_depth = st.sidebar.slider("Sag Depth (Remaining %)", 0.1, 0.9, 0.5)
    elif fault_type == "Swell":
        swell_mag = st.sidebar.slider("Swell Magnitude (x)", 1.1, 2.0, 1.5)
    elif fault_type == "Harmonics":
        h3 = st.sidebar.slider("3rd Harmonic (150Hz)", 0.0, 0.5, 0.1)
        h5 = st.sidebar.slider("5th Harmonic (250Hz)", 0.0, 0.5, 0.05)
        h7 = st.sidebar.slider("7th Harmonic (350Hz)", 0.0, 0.5, 0.02)
        harmonics = {3: h3, 5: h5, 7: h7}
        
    return sag_depth, swell_mag, harmonics

def render_metrics(rms_val, thd_val, diagnosis, config):
    st.subheader("Diagnostics")
    
    # Status Alert
    if diagnosis == "Normal Operation":
        st.success(diagnosis)
    else:
        st.error(diagnosis)
        
    st.divider()
    
    # Metrics
    st.metric("RMS Voltage", f"{rms_val:.2f} V", delta=f"{rms_val - config.VOLTAGE_RMS:.1f} V")
    st.metric("THD", f"{thd_val*100:.2f} %", delta=f"{(thd_val - config.THD_THRESHOLD)*100:.2f} %" if thd_val > config.THD_THRESHOLD else None)
    
    st.markdown("### Thresholds")
    st.caption(f"Sag: < {config.SAG_THRESHOLD} V")
    st.caption(f"Swell: > {config.SWELL_THRESHOLD} V")
    st.caption(f"THD: > {config.THD_THRESHOLD*100} %")
