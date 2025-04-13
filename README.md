# AI-Powered Log Analysis

Automated log analysis using Isolation Forest algorithm to detect anomalies in system logs.

## Features
- Real-time log monitoring
- Anomaly detection using Isolation Forest
- Detailed anomaly reporting
- Support for multiple service logs

## Setup
1. Install requirements:
```pip install scikit-learn numpy```

2. Generate sample logs:
```python src/generate_logs.py```

3. Run the analyzer:
```python src/main.py```

## Project Structure
- src/
  - main.py: Main analysis script
  - log_analyzer.py: Isolation Forest implementation
  - generate_logs.py: Sample log generator