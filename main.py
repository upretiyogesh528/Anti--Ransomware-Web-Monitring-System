import os
import time
import argparse
import sys
from utils.logger import setup_logger
from detectors.file_monitor import FileSystemMonitor
from detectors.behavior_detector import BehaviorDetector
from dashboard.app import start_dashboard
import config

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Ransomware Detection System")
    parser.add_argument("--path", type=str, default=config.MONITOR_PATH,
                      help="Path to monitor for ransomware activity")
    parser.add_argument("--dashboard", action="store_true",
                      help="Start the web dashboard")
    parser.add_argument("--debug", action="store_true",
                      help="Enable debug logging")
    parser.add_argument("--port", type=int, default=config.DASHBOARD_PORT,
                      help="Port to use for the dashboard")
    args = parser.parse_args()
    
    # Set the current monitoring path in config for the dashboard to access
    config.CURRENT_MONITORING_PATH = args.path
    
    # Set up logging
    log_level = "DEBUG" if args.debug else "INFO"
    logger = setup_logger(console_level=getattr(logging, log_level))
    logger.info("Starting Ransomware Detection System")
    
    # Create directory for logs if it doesn't exist
    os.makedirs(config.LOGS_DIR, exist_ok=True)
    
    try:
        # Initialize the behavior detector
        behavior_detector = BehaviorDetector()
        
        # Initialize the file system monitor
        file_monitor = FileSystemMonitor(
            path=args.path,
            behavior_detector=behavior_detector
        )
        
        # Start the dashboard if requested
        if args.dashboard:
            try:
                logger.info("Starting dashboard interface")
                # Pass the port from args directly to ensure consistency
                start_dashboard(behavior_detector, port=args.port)
                # Use 'localhost' for display purposes instead of the binding address
                display_host = "localhost" if config.DASHBOARD_HOST == "0.0.0.0" else config.DASHBOARD_HOST
                logger.info(f"Dashboard available at http://{display_host}:{args.port}")
                print(f"Dashboard available at http://{display_host}:{args.port}")
            except Exception as e:
                logger.error(f"Failed to start dashboard: {e}")
        
        # Start the file system monitor in a background thread
        file_monitor.start_async()
        logger.info(f"Monitoring files in {args.path}")
        
        # Keep the main thread running
        try:
            print(f"Ransomware Detection System running. Press Ctrl+C to stop.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down Ransomware Detection System")
            file_monitor.stop()
            sys.exit(0)
    
    except Exception as e:
        logger.error(f"Error in main program: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    import logging  # Add import here to avoid circular imports
    main()
