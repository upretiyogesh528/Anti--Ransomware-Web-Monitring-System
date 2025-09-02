import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory to monitor (default is the user's home directory)
MONITOR_PATH = os.path.expanduser("~")

# This will be updated at runtime with the actual path being monitored
CURRENT_MONITORING_PATH = None

# Logs directory
LOGS_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOGS_DIR, "ransomware_detector.log")

# Data directory
DATA_DIR = os.path.join(BASE_DIR, "data")
SIGNATURES_FILE = os.path.join(DATA_DIR, "signatures.json")

# Dashboard settings
DASHBOARD_HOST = "0.0.0.0"  # Allow connections from any IP
DASHBOARD_PORT = 5001

# Detection settings
ENTROPY_THRESHOLD = 7.0  # Higher values indicate potential encryption
MAX_FILES_CHANGED_THRESHOLD = 10  # Number of file changes in a short period to trigger alert
SUSPICIOUS_EXTENSIONS = [
    ".crypted", ".locked", ".encrypted", ".crypto", ".crypt",
    ".vault", ".enc", ".pay", ".locked", ".cerber", ".zepto",
    ".locky", ".osiris", ".odin", ".sage", ".cryptolocker", ".cryptowall"
]

# Time window for detecting burst of file changes (in seconds)
TIME_WINDOW = 60
