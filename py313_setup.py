"""
Setup script for the Ransomware Detection project with Python 3.13 compatibility.
This script creates the necessary directory structure and files.
"""
import os
import sys
import subprocess
import platform

def create_directory(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def create_file(path, content=""):
    """Create a file with given content."""
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def create_project_structure():
    """Create the basic project structure."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create main directories
    dirs = [
        os.path.join(base_dir, "utils"),
        os.path.join(base_dir, "detectors"),
        os.path.join(base_dir, "dashboard"),
        os.path.join(base_dir, "dashboard", "templates"),
        os.path.join(base_dir, "dashboard", "static"),
        os.path.join(base_dir, "logs"),
        os.path.join(base_dir, "data"),
    ]
    
    for d in dirs:
        create_directory(d)
    
    # Create __init__.py files
    for package in ["utils", "detectors", "dashboard"]:
        init_file = os.path.join(base_dir, package, "__init__.py")
        if not os.path.exists(init_file):
            create_file(init_file, "# Package initialization\n")
    
    # Create config.py if it doesn't exist
    config_path = os.path.join(base_dir, "config.py")
    if not os.path.exists(config_path):
        config_content = """
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory to monitor (default is the user's home directory)
MONITOR_PATH = os.path.expanduser("~")

# Logs directory
LOGS_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOGS_DIR, "ransomware_detector.log")

# Data directory
DATA_DIR = os.path.join(BASE_DIR, "data")
SIGNATURES_FILE = os.path.join(DATA_DIR, "signatures.json")

# Dashboard settings
DASHBOARD_HOST = "127.0.0.1"
DASHBOARD_PORT = 5000

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
"""
        create_file(config_path, config_content)
    
    # Create basic logger module
    logger_path = os.path.join(base_dir, "utils", "logger.py")
    if not os.path.exists(logger_path):
        logger_content = """
import logging
import os
import colorlog
import config

def setup_logger():
    \"\"\"Configure and return a logger for the application.\"\"\"
    # Create logs directory if it doesn't exist
    os.makedirs(config.LOGS_DIR, exist_ok=True)
    
    logger = logging.getLogger("ransomware_detector")
    logger.setLevel(logging.DEBUG)
    
    # Stop propagation to the root logger
    logger.propagate = False
    
    # File handler for all logs
    file_handler = logging.FileHandler(config.LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler with colors for info and above
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(console_formatter)
    
    # Remove existing handlers if any
    if logger.handlers:
        logger.handlers = []
        
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger():
    \"\"\"Get the configured logger.\"\"\"
    return logging.getLogger("ransomware_detector")
"""
        create_file(logger_path, logger_content)
    
    print("\nProject structure created successfully!")
    print("Next steps:")
    print("1. Run the dependency checker: python check_dependencies.py")
    print("2. Install required packages: pip install -r requirements-py313.txt")

def install_single_packages():
    """Install packages one by one to avoid dependency issues."""
    print("\nInstalling core packages one by one...")
    packages = [
        "flask==2.3.3",
        "watchdog==3.0.0",
        "colorlog==6.8.0",
        "psutil==5.9.6",
    ]
    
    # These are the packages that might need special handling
    scientific_packages = [
        "numpy==2.2.5",
        "scipy==1.13.1",
        "pandas==2.2.1",
        "matplotlib==3.9.0",
        "scikit-learn==1.5.0",
    ]
    
    # Platform specific
    if platform.system() == "Windows":
        packages.append("python-magic-bin==0.4.14")
        packages.append("pywin32==306")
    else:
        packages.append("python-magic==0.4.27")
    
    # Install the core packages first
    for pkg in packages:
        try:
            print(f"Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        except subprocess.CalledProcessError:
            print(f"Failed to install {pkg}")
    
    # Then attempt to install scientific packages
    print("\nInstalling scientific packages...")
    for pkg in scientific_packages:
        try:
            print(f"Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        except subprocess.CalledProcessError:
            print(f"Failed to install {pkg}, trying without version constraint...")
            pkg_name = pkg.split("==")[0]
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])
            except subprocess.CalledProcessError:
                print(f"Failed to install {pkg_name}")

def install_dependencies():
    """Install required dependencies."""
    print("\nInstalling dependencies...")
    
    # First try directly with requirements file
    requirements_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        "requirements-py313.txt"
    )
    
    if os.path.exists(requirements_file):
        try:
            print("Trying to install all dependencies at once...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", requirements_file
            ])
            print("Dependencies installed successfully!")
            return
        except subprocess.CalledProcessError as e:
            print(f"Error installing all dependencies at once: {e}")
            print("Will try installing packages one by one.")
            install_single_packages()
    else:
        print(f"Requirements file not found: {requirements_file}")
        print("Installing packages one by one...")
        install_single_packages()

if __name__ == "__main__":
    print("Setting up Ransomware Detection project for Python 3.13...")
    create_project_structure()
    choice = input("\nWould you like to install dependencies now? (y/n): ")
    if choice.lower() == 'y':
        install_dependencies()
