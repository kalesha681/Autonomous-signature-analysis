"""
Module: visualizations.py
Description: Plotting logic for the dashboard
"""
import plotly.graph_objects as go

def plot_time_domain(t, waveform, samples=200):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t[:samples], y=waveform[:samples], mode='lines', name='Voltage'))
    fig.update_layout(
        title="Time Domain (Oscilloscope)", 
        xaxis_title="Time (s)", 
        yaxis_title="Voltage (V)", 
        height=350,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def plot_frequency_domain(frequencies, magnitudes, limit=100):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=frequencies[:limit], y=magnitudes[:limit], name='Spectrum'))
    fig.update_layout(
        title="Frequency Domain (Spectrum)", 
        xaxis_title="Frequency (Hz)", 
        yaxis_title="Magnitude (V)", 
        height=350,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig
