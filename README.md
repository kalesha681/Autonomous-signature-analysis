# Autonomous Edge-Based Signature Analysis

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-FF4B4B)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![CI/CD](https://img.shields.io/badge/build-passing-brightgreen)

## Project Description

This repository hosts a production-grade software prototype for a next-generation Smart Meter. Unlike traditional meters that simply log energy consumption, this system acts as a "Smart Meter with a Brain," capable of performing high-resolution power quality analysis directly at the edge.

The system utilizes a Hybrid AI architecture to diagnose electrical faults in real-time. It combines deterministic rule-based logic for identifying known issues (such as Voltage Sags, Swells, and Harmonic Distortion) with unsupervised machine learning (Isolation Forest) to detect anomalous behaviors that deviate from the established baseline. This approach addresses the "Data-Analysis Gap" in industrial IoT by converting raw high-frequency waveforms into actionable diagnostic insights before transmission.

## Reproducibility

This project is designed for ease of deployment and testing. There are two primary methods to run the application: using Docker (recommended for consistency) or a local Python environment.

### Prerequisites
*   Docker Desktop (Optional, for containerized run)
*   Python 3.9+ (For local execution)

### Method 1: Docker Deployment
To build and launch the application container:

```bash
docker build -t smart-meter-app .
docker run -p 8501:8501 smart-meter-app
```
The dashboard will be accessible at `http://localhost:8501`.

### Method 2: Local Python Execution
To run the application directly on the host machine:

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Launch Dashboard:**
    ```bash
    # Windows
    run_app.bat
    
    # Linux/Mac
    streamlit run dashboard/app_main.py
    ```

### Testing
Automated unit tests verified by the CI/CD pipeline can be executed locally to ensure system integrity:
```bash
python -m unittest discover tests
```

## System Outputs

The primary output of the system is an interactive real-time Dashboard that provides:

1.  **Time Domain Analysis:** A simulated Oscilloscope view rendering the voltage waveform in real-time.
2.  **Frequency Domain Analysis:** A live Spectrum Analyzer displaying the magnitude of frequency components (Harmonics) derived via FFT.
3.  **Real-Time Diagnostics:** The "Inference Engine" outputs diagnostic status messages such as:
    *   "Normal Operation"
    *   "WARNING: Voltage Sag Detected"
    *   "WARNING: Harmonic Fault Detected"
    *   "WARNING: Unknown Anomaly Detected (AI)"
4.  **Telemetry Metrics:** Live values for RMS Voltage, Peak Voltage, and Total Harmonic Distortion (THD).

## Mathematical Principles

The core signal processing relies on fundamental electrical engineering principles and statistical analysis.

### 1. Fast Fourier Transform (FFT)
The system converts the time-domain signal $v(t)$ into the frequency domain $V(f)$ to identify spectral content.
*   **Implementation:** `scipy.fft`
*   **Purpose:** To isolate the magnitude of individual harmonic orders (3rd, 5th, 7th).

### 2. Root Mean Square (RMS)
Voltage magnitude is calculated using the RMS formula to determine effective power:
$$V_{rms} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} v_i^2}$$
*   **Usage:** Detection of Voltage Sags ($< 0.9$ p.u.) and Swells ($> 1.1$ p.u.).

### 3. Total Harmonic Distortion (THD)
Power quality is assessed by the ratio of the sum of the powers of all harmonic components to the power of the fundamental frequency:
$$THD = \frac{\sqrt{\sum_{n=2}^{\infty} V_n^2}}{V_{fundamental}}$$
*   **Usage:** Detection of non-linear load faults and harmonic pollution.

### 4. Anomaly Detection (Isolation Forest)
For unknown faults, the system employs an Isolation Forest algorithm. It isolates observations by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature.
*   **Logic:** Anomalies are susceptible to isolation and will have shorter path lengths in the ensemble of random trees.

## Conclusion

This project demonstrates a scalable, modular architecture for Industrial IoT solutions. By rigorously separating concerns into Simulation, Processing, Inference, and Presentation layers, and by adhering to DevOps best practices (Docker, CI/CD), it provides a robust foundation for deploying intelligence to the industrial edge. The Hybrid AI approach ensures both reliability (via rules) and adaptability (via unsupervised learning), making it suitable for critical power monitoring applications.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
