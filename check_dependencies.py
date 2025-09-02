"""
Dependency checker script to ensure all required libraries are installed
and diagnose common issues with the ransomware detection tool.
"""
import sys
import os
import subprocess
import importlib
import platform

def check_import(module_name):
    """Check if a module can be imported."""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def print_system_info():
    """Print information about the system."""
    print("\n=== System Information ===")
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python executable: {sys.executable}")
    print("=" * 30)

def check_setuptools():
    """Check if setuptools is properly installed and working."""
    try:
        import setuptools
        print(f"Setuptools version: {setuptools.__version__}")
        return True
    except ImportError:
        print("❌ Setuptools is not installed properly")
        return False
    except Exception as e:
        print(f"❌ Error with setuptools: {e}")
        return False

def install_package(package_name):
    """Install a single package."""
    print(f"Installing {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--upgrade"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {e}")
        return False

def is_python_version_compatible():
    """Check if the current Python version is compatible."""
    major, minor, *_ = sys.version_info
    if major == 3 and minor >= 13:
        print(f"Python {major}.{minor} detected - using compatible package versions.")
        return True  # We're now supporting 3.13, so return True
    return True

def check_and_create_init_files():
    """Create missing __init__.py files in package directories."""
    packages = ["utils", "detectors", "dashboard"]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for pkg in packages:
        pkg_path = os.path.join(base_dir, pkg)
        init_file = os.path.join(pkg_path, "__init__.py")
        
        # Create directory if it doesn't exist
        if not os.path.exists(pkg_path):
            os.makedirs(pkg_path)
            print(f"Created directory: {pkg_path}")
        
        # Create __init__.py if it doesn't exist
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# Package initialization\n")
            print(f"Created: {init_file}")

def main():
    print("Ransomware Detection Tool - Dependency Checker (Python 3.13 Compatible)")
    print_system_info()
    
    # First check setuptools and pip
    print("\nChecking base packaging tools...")
    check_setuptools()
    
    try:
        import pip
        print(f"Pip version: {pip.__version__}")
    except ImportError:
        print("❌ Pip not found in the current environment")
    
    # Python 3.13 compatible dependencies with versions
    dependencies_with_versions = [
        ("flask", "2.3.3"),
        ("watchdog", "3.0.0"),
        ("numpy", "2.2.5"),  # Updated for Python 3.13
        ("scipy", "1.13.1"),  # Updated for Python 3.13
        ("scikit-learn", "1.5.0"),  # Updated for Python 3.13
        ("pandas", "2.2.1"),  # Updated for Python 3.13
        ("matplotlib", "3.9.0"),  # Updated for Python 3.13
        ("psutil", "5.9.6"),
        ("colorlog", "6.8.0")
    ]
    
    # Extract just the names for checking
    dependencies = [item[0] for item in dependencies_with_versions]
    
    # Optional dependencies based on platform
    if platform.system() == "Windows":
        dependencies.append("pywin32")
        dependencies.append("python-magic-bin")
        dependencies_with_versions.append(("pywin32", "306"))
        dependencies_with_versions.append(("python-magic-bin", "0.4.14"))
    else:
        dependencies.append("python-magic")
        dependencies_with_versions.append(("python-magic", "0.4.27"))
    
    # Check each dependency
    print("\nChecking dependencies...")
    missing = []
    for dep in dependencies:
        sys.stdout.write(f"Checking for {dep}... ")
        if check_import(dep):
            print("✓")
        else:
            print("❌")
            missing.append(dep)
    
    # Results
    if missing:
        print("\n⚠️ Missing dependencies detected!")
        print("Please install the following packages:")
        for dep in missing:
            print(f"  - {dep}")
        
        # Installation options
        print("\nInstallation options:")
        print("1. Install all dependencies at once:")
        print("   pip install -r requirements-py313.txt")
        print("2. Install dependencies one by one:")
        for dep, ver in dependencies_with_versions:
            if dep in missing:
                print(f"   pip install {dep}=={ver}")
        
        # Offer to install
        choice = input("\nWould you like to attempt installation now? (y/n): ")
        if choice.lower() == 'y':
            # Try to install all at once first
            requirements_file = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                "requirements-py313.txt"
            )
            if os.path.exists(requirements_file):
                print(f"\nInstalling dependencies from {requirements_file}...")
                try:
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", "-r", requirements_file
                    ])
                except subprocess.CalledProcessError:
                    print("Failed to install all dependencies at once, trying one by one...")
                    for dep, ver in dependencies_with_versions:
                        if dep in missing:
                            install_package(f"{dep}=={ver}")
            else:
                print("requirements-py313.txt not found, installing one by one...")
                for dep, ver in dependencies_with_versions:
                    if dep in missing:
                        install_package(f"{dep}=={ver}")
                
            print("\nPlease run this checker again to verify installations.")
    else:
        print("\n✅ All dependencies are installed correctly!")
    
    # Check and create package directories and __init__.py files
    check_and_create_init_files()
    
    # Check for project modules
    print("\nChecking project structure...")
    project_modules = ["config", "utils.logger", "detectors.file_monitor", "dashboard.app"]
    project_issues = []
    
    for module in project_modules:
        sys.stdout.write(f"Checking for {module}... ")
        try:
            importlib.import_module(module)
            print("✓")
        except ImportError as e:
            print("❌")
            project_issues.append(f"{module}: {str(e)}")
    
    if project_issues:
        print("\n⚠️ Issues with project structure detected:")
        for issue in project_issues:
            print(f"  - {issue}")
        print("\nMake sure you're running this script from the project root directory")
        print("and that all project files are correctly created.")
        
        # Recommend running the setup script
        print("\nTry running the setup script to create the necessary project structure:")
        print("python py313_setup.py")
    else:
        print("\n✅ Project structure looks good!")
    
    print("\nCheck completed.")

if __name__ == "__main__":
    main()
