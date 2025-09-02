import os
import random
import time
import config

def ensure_test_dir():
    """Ensure the test directory exists."""
    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_monitor")
    os.makedirs(test_dir, exist_ok=True)
    print(f"Test directory: {os.path.abspath(test_dir)}")
    print(f"IMPORTANT: Make sure you're monitoring this exact path in the detection system!")
    print(f"Run with: python main.py --dashboard --path \"{os.path.abspath(test_dir)}\"")
    return test_dir

def create_suspicious_extension_file(test_dir):
    """Create a file with a suspicious extension."""
    # Use multiple known extensions to increase chances of detection
    for ext in [".crypted", ".encrypted", ".crypto", ".locky"]:
        filename = f"ENCRYPTED_FILES{ext}"
        filepath = os.path.join(test_dir, filename)
        
        print(f"Creating suspicious extension file: {filename}")
        with open(filepath, 'w') as f:
            f.write("YOUR FILES HAVE BEEN ENCRYPTED!\n")
            f.write("This is a test file that should trigger the ransomware detection system.\n")
    
    return filepath

def create_ransom_note(test_dir):
    """Create a file that looks like a ransom note."""
    ransom_filenames = [
        "README_TO_DECRYPT.txt",
        "HOW_TO_RECOVER_FILES.txt",
        "YOUR_FILES_ENCRYPTED.txt",
        "DECRYPT_INSTRUCTION.html",
        "BITCOIN_PAYMENT.txt"
    ]
    
    filename = random.choice(ransom_filenames)
    filepath = os.path.join(test_dir, filename)
    
    print(f"Creating ransom note: {filename}")
    with open(filepath, 'w') as f:
        f.write("YOUR FILES HAVE BEEN ENCRYPTED!\n\n")
        f.write("All your documents, photos, databases, and other files have been encrypted with a strong algorithm.\n")
        f.write("To recover your files, you must pay using cryptocurrency.\n\n")
        f.write("This is a TEST ransom note to demonstrate the detection system.\n")
    
    return filepath

def create_high_entropy_file(test_dir):
    """Create a file with high entropy that looks encrypted."""
    filename = "encrypted_data.crypted"
    filepath = os.path.join(test_dir, filename)
    
    print(f"Creating high-entropy file: {filename}")
    with open(filepath, 'wb') as f:
        # Generate 100KB of random bytes for very high entropy
        random_bytes = os.urandom(102400)  # Using os.urandom for true randomness
        f.write(random_bytes)
    
    print(f"Created high-entropy file at: {filepath}")
    return filepath

def create_activity_burst(test_dir):
    """Create many files in quick succession to trigger activity burst detection."""
    print("Creating activity burst (multiple files in quick succession)...")
    files_created = []
    
    for i in range(config.MAX_FILES_CHANGED_THRESHOLD + 5):  # Create more than the threshold
        filename = f"burst_file_{i}.txt"
        filepath = os.path.join(test_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(f"File {i} created during activity burst test\n")
        
        files_created.append(filepath)
        time.sleep(0.1)  # Small delay between files
    
    return files_created

def verify_monitoring_setup():
    """Check if the monitoring system is likely set up correctly."""
    print("\nVERIFYING SETUP:")
    print("1. Is the detection system running? It should show logs in another console.")
    print("2. Are you monitoring the correct directory?")
    print("3. Did you start with the --dashboard flag to see results?")
    print("\nIf alerts aren't showing in the dashboard, check these issues first.")

if __name__ == "__main__":
    test_dir = ensure_test_dir()
    verify_monitoring_setup()
    
    print("\nCreating test files in:", test_dir)
    
    # Create multiple alert-triggering files without waiting for input
    print("\nCreating suspicious extension files...")
    suspicious_file = create_suspicious_extension_file(test_dir)
    
    print("\nCreating ransom note...")
    ransom_note = create_ransom_note(test_dir)
    
    print("\nCreating high-entropy encrypted file...")
    entropy_file = create_high_entropy_file(test_dir)
    
    print("\nCreating activity burst...")
    burst_files = create_activity_burst(test_dir)
    
    print("\nAll test files created successfully!")
    print("\nVERIFICATION STEPS:")
    print("1. Check console output for any alerts")
    print("2. Open dashboard at http://localhost:5001 to see alerts")
    print("3. If no alerts appear, verify you're monitoring:", os.path.abspath(test_dir))
