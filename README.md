# Ransomware Detection System

A file system monitoring tool to detect potential ransomware activity on your system.

## Features

- Real-time file system monitoring
- Detection of suspicious file operations
- Entropy analysis to identify potential encryption
- Behavior patterns detection for known ransomware
- Web dashboard for visualization and alerts
- Logging and alerting system

## Installation

1. Install Python 3.7+ if not already installed
2. Clone this repository
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Start the basic monitoring:

```bash
python main.py
```

Start with dashboard:

```bash
python main.py --dashboard
```

Specify a custom directory to monitor:

```bash
python main.py --path "C:\Path\To\Monitor" --dashboard
```

## How it works

The system works by:

1. Monitoring the file system for changes
2. Analyzing file changes for suspicious patterns
3. Calculating entropy of modified files to detect encryption
4. Tracking the rate of file changes to detect bursts of activity
5. Looking for known ransomware patterns like ransom notes

## Dashboard

When started with the `--dashboard` flag, a web interface will be available at:
http://127.0.0.1:5000

## Warning Signs

The system looks for multiple indicators of ransomware activity:

- High entropy in files (indicating encryption)
- Burst of file modifications in a short time
- Known ransomware file extensions
- Creation of ransom note files
- Suspicious processes

## Disclaimer

This tool is for educational and defensive purposes only. It may not detect all forms of ransomware, especially newer variants. Always maintain proper backups and security practices.

## License

MIT
