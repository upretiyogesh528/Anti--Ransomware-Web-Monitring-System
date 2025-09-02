import os
import random
import time

def create_test_directory(base_path=None):
    """Create a test directory to monitor."""
    # If no path specified, create it in the project directory
    if not base_path:
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_monitor")
    
    # Create the directory if it doesn't exist
    os.makedirs(base_path, exist_ok=True)
    print(f"Created test directory: {base_path}")
    
    return base_path

def create_normal_files(directory, num_files=5):
    """Create normal files that shouldn't trigger alerts."""
    for i in range(num_files):
        # Create files with different extensions
        extensions = ['.txt', '.log', '.ini', '.cfg', '.md', '.json', '.csv']
        ext = random.choice(extensions)
        filename = f"normal_file_{i}{ext}"
        filepath = os.path.join(directory, filename)
        
        # Create file with random content
        with open(filepath, "w") as f:
            f.write(f"This is a normal test file {i}\n")
            f.write("It contains regular text content.\n")
            f.write("Line 3 of the file.\n")
            f.write(f"Created at {time.ctime()}\n")
        
        print(f"Created normal file: {filename}")

def main():
    print("Setting up test environment for ransomware detection system...")
    
    # Create test directory
    test_dir = create_test_directory()
    
    # Create normal files
    create_normal_files(test_dir)
    
    print("\nTest environment setup complete!")
    print(f"\nTo start monitoring, run:")
    print(f"python main.py --dashboard --path \"{test_dir}\"")
    print("\nYou can then create suspicious files in this directory to trigger alerts.")

if __name__ == "__main__":
    main()
