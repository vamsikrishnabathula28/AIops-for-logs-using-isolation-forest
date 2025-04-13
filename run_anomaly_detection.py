#!/usr/bin/env python3
"""
Run anomaly detection on log files
"""

from src.process_logs import main as process_logs_main
import sys

if __name__ == "__main__":
    # Default to sample_logs.txt if no arguments provided
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        log_file = "sample_logs.txt"
    
    # Set up arguments for process_logs.py
    sys.argv = ["process_logs.py", log_file, "--output", "anomaly_results.txt"]
    
    # Run the process_logs.py script
    process_logs_main() 