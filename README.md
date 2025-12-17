# Autonomous Edge-Based Signature Analysis.
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-FF4B4B)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![CI/CD](https://img.shields.io/badge/build-passing-brightgreen)


## Project Overview
This repository provides a research-grade, reproducible framework for simulating and benchmarking "Edge AI" algorithms on a Smart Meter.

It is designed for students, researchers, and engineers to understand how hybrid artificial intelligence can perform real-time power quality analysis on industrial IoT hardware. The simulation is powered by digital twin waveform generators, ensuring signal fidelity while remaining easy to run on any computer.

We implement and compare two fundamental inference architectures:

1.  **Rule-Based Logic**: The industry standard, deterministic and effective for known faults (ANSI C84.1 compliance).
2.  **Unsupervised Learning (Isolation Forest)**: A robust machine learning model that detects unknown anomalies deviating from the baseline.

## Directory Structure
Here is a guide to what you will find in this repository:

```text
Autonomous-Edge-Based-Signature-Analysis/
├── dashboard/                 # The main HMI package
│   ├── app_main.py            # The main entry point. Run this to start!
│   ├── components.py          # UI widgets and sidebar controls
│   └── visualizations.py      # Plotly-based oscilloscope and spectrum views
├── simulation/                # Digital Twin Engine
│   ├── waveform_generator.py  # AC sine wave synthesis (50Hz/60Hz)
│   └── fault_injector.py      # Physics-based fault algorithms (Sag, Swell, Harmonics)
├── processing/                # Signal Processing Core
│   ├── fft_core.py            # Fast Fourier Transform implementation
│   └── feature_extractor.py   # RMS, Peak, and THD calculators
├── inference/                 # The "Brain"
│   ├── predictor_core.py      # Hybrid decision logic
│   ├── anomaly_detector.py    # Isolation Forest (Scikit-Learn)
│   └── signatures.py          # Fault definitions and thresholds
├── data/                      # Data storage
│   └── models/                # Serialized ML models (.pkl)
├── tests/                     # Automated unit tests
├── .github/                   # CI/CD configuration for GitHub Actions
└── requirements.txt           # List of Python dependencies
```

## Getting Started

### Prerequisites
*   **Operating System**: Windows, Linux (Ubuntu), or macOS.
*   **Python**: Version 3.9 or higher.
*   **Docker**: Optional, for containerized execution.

### Installation

**1. Clone the Repository**
```bash
git clone https://github.com/kalesha681/autonomous-signature-analysis.git
cd autonomous-signature-analysis
```

**2. Create a Virtual Environment (Recommended)**
It's best practice to keep dependencies isolated.
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

## Theory & Mathematics

The system processes raw voltage signals $v(t)$ to extract meaningful power quality signatures.

### 1. Root Mean Square (RMS) Analysis
The RMS value is the fundamental metric for voltage stability. It represents the effective DC heating value of the AC waveform.
$$V_{rms} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} v[i]^2}$$

*   **Application**: Used to detect **Voltage Sags** ($V_{rms} < 0.9$ p.u.) and **Swells** ($V_{rms} > 1.1$ p.u.).

### 2. Spectral Analysis (FFT)
To detect harmonic distortion, we transform the time-domain signal into the frequency domain using the Discrete Fourier Transform (DFT):
$$X_k = \sum_{n=0}^{N-1} x_n \cdot e^{-i 2 \pi k n / N}$$

*   **Application**: We calculate Total Harmonic Distortion (THD) to identify non-linear load faults.
    $$THD = \frac{\sqrt{\sum_{n=2}^{\infty} V_n^2}}{V_{fundamental}}$$

### 3. Unsupervised Anomaly Detection
We employ an **Isolation Forest** (iForest) algorithm for non-deterministic fault detection.
*   **Concept**: Anomalies are "few and different".
*   **Logic**: The algorithm isolates observations by randomly selecting a feature and then randomly selecting a split value. Anomalies have shorter path lengths in the random trees.
*   **Why use it?**: It allows the meter to flag "Unknown" issues that were not explicitly programmed in the rule base.

## Usage

The entire system is controlled via the dashboard.

### 1. Visual Simulation (GUI)
Run the Streamlit dashboard to see the oscilloscope and spectrum analyzer in real-time.

```bash
# Windows
.\run_app.bat

# Linux/Mac
streamlit run dashboard/app_main.py
```

### 2. Docker Mode (Headless/Cloud)
Run the application as a containerized service.

```bash
docker build -t smart-meter-app .
docker run -p 8501:8501 smart-meter-app
```

## Results & Analysis

The framework provides immediate visual and textual feedback on standard power quality events.

### Diagnostic Performance

| Fault Type | Detection Method | Threshold / Logic | Characteristics |
| :--- | :--- | :--- | :--- |
| **Voltage Sag** | RMS Analysis | $< 0.9 \times V_{nom}$ | Instantaneous detection (< 20ms lag). |
| **Voltage Swell** | RMS Analysis | $> 1.1 \times V_{nom}$ | Robust against random noise. |
| **Harmonics** | FFT + THD | $> 5\%$ THD | Accurate spectral decomposition of 3rd, 5th, 7th orders. |
| **Unknown** | Isolation Forest | Path Length Outlier | Flags unexpected signal deviations (e.g., Gaussian noise attacks). |

### Visual Comparison
*   **Oscilloscope View**: Shows the raw $v(t)$ waveform. Sags appear as amplitude dips; Harmonics appear as distorted/jagged waves.
*   **Spectrum View**: Shows the $V(f)$ bar chart. Harmonic faults show distinct spikes at 150Hz, 250Hz, etc.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repo.
2.  Create a branch: `git checkout -b feature-new-algorithm`.
3.  Commit changes: `git commit -m "Add Wavelet Transform"`.
4.  Push to branch: `git push origin feature-new-algorithm`.
5.  Submit a Pull Request.

## Future Work

1.  **Hardware-in-the-Loop**: Porting the `inference/` logic to an ESP32 microcontroller.
2.  **Advanced Signal Processing**: Implementation of Wavelet Transform for transient detection.
3.  **Cloud Integration**: MQTT connectivity to AWS IoT Core.

## Citation

If you use this work in your research or studies, please cite:

**Shaik, Kalesha.** "Autonomous Edge-Based Signature Analysis Framework". 2025.

**Author**: [Kalesha Shaik](https://www.linkedin.com/in/kalesha-shaik/)

