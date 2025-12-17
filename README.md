# Autonomous Edge-Based Signature Analysis

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-FF4B4B)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![CI/CD](https://img.shields.io/badge/build-passing-brightgreen)
![Status](https://img.shields.io/badge/status-Production-green)

An industrial IoT platform for **"Smart Meter with a Brain"**. This system differentiates itself by moving AI to the edge—performing real-time spectral analysis (FFT) and using an **Isolation Forest (Unsupervised Learning)** to detect unknown power quality anomalies, alongside traditional rule-based logic.

---

## 🌟 Key Features

- **Real-Time Edge Analytics**: Performed FFT analysis on 1000Hz sampled waveforms to extract harmonic signatures.
- **Hybrid AI Architecture**:
    - **Rule-Based**: Deterministic logic for known faults (Sag, Swell, Harmonics).
    - **Unsupervised Learning**: `IsolationForest` to detect *unknown* anomalies that deviate from the trained baseline.
- **Production-Ready**:
    - **Dockerized**: Fully containerized for cloud or edge deployment.
    - **CI/CD**: GitHub Actions pipeline for automated testing.
    - **Live Streaming**: Real-time oscilloscope visualization in the dashboard.

---

## 🏗 Architecture

The repository enforces strict separation of concerns for scalability:

- **`dashboard/`**: Streamlit-based HMI with "Live Mode" streaming.
- **`simulation/`**: Digital Twin engine for generating synthetic faulty waveforms.
- **`processing/`**: Signal processing math (FFT, RMS, THD).
- **`inference/`**:
    - `predictor_core.py`: Hybrid inference engine.
    - `anomaly_detector.py`: Scikit-learn anomaly detection model.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+ OR Docker

### Method 1: Docker (Recommended)

Build and run the container:
```bash
docker build -t smart-meter-app .
docker run -p 8501:8501 smart-meter-app
```
Access at `http://localhost:8501`.

### Method 2: Local Python

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Dashboard:
   ```bash
   run_app.bat
   # OR
   streamlit run dashboard/app_main.py
   ```

## 🧪 Testing

Run the automated CI suite locally:

```bash
python -m unittest discover tests
```

## 📂 Directory Structure

```text
├── .github/workflows/  # CI/CD Pipeline
├── dashboard/          # UI Components & Main App
├── data/               # Raw Data & Models (Gitignored)
├── inference/          # ML & Logic (Isolation Forest)
├── processing/         # FFT & Signal Math
├── simulation/         # Waveform Generator
├── tests/              # Unit Tests
├── utils/              # Configuration & Helpers
├── Dockerfile          # Container Config
└── requirements.txt    # Dependencies
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
