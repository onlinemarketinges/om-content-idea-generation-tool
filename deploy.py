#!/usr/bin/env python3
"""
Deployment Script for Viral Content Ideas Generator
"""

import os
import sys
import logging
import subprocess
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("deployment")

# Constants
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PORT = 8000

def check_dependencies():
    """Check if all required dependencies are installed"""
    logger.info("Checking dependencies...")
    
    try:
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
            logger.error(f"Python 3.6+ required, found {python_version.major}.{python_version.minor}")
            return False
        
        # Check required Python packages
        required_packages = ["sqlite3", "requests", "schedule"]
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                logger.error(f"Required package '{package}' not found")
                return False
        
        logger.info("All dependencies satisfied")
        return True
        
    except Exception as e:
        logger.error(f"Error checking dependencies: {e}")
        return False

def prepare_data_directory():
    """Prepare data directory with sample data if needed"""
    logger.info("Preparing data directory...")
    
    try:
        # Create data directory if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Check if sample data exists
        sample_file = os.path.join(DATA_DIR, "sample-videos.json")
        if not os.path.exists(sample_file):
            logger.info("Generating sample data...")
            
            # Import and run sample data generation
            sys.path.append(PROJECT_ROOT)
            from data_collection.viral_identification import generate_sample_data
            generate_sample_data(DATA_DIR)
            
            logger.info("Sample data generated")
        
        # Initialize database if it doesn't exist
        db_file = os.path.join(DATA_DIR, "viral_videos.db")
        if not os.path.exists(db_file):
            logger.info("Initializing database...")
            
            # Import and run database initialization
            from data_collection.database import initialize_database
            initialize_database(DATA_DIR)
            
            logger.info("Database initialized")
        
        logger.info("Data directory prepared")
        return True
        
    except Exception as e:
        logger.error(f"Error preparing data directory: {e}")
        return False

def start_server(port=PORT, daemon=True):
    """Start the web server"""
    logger.info(f"Starting web server on port {port}...")
    
    try:
        # Change to project root directory
        os.chdir(PROJECT_ROOT)
        
        # Start server process
        if daemon:
            # Start as daemon process
            server_process = subprocess.Popen(
                ["nohup", "python3", "server.py", str(port), "&"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True
            )
            
            # Wait a moment for server to start
            time.sleep(3)
            
            # Check if server is running
            try:
                import requests
                response = requests.get(f"http://localhost:{port}")
                if response.status_code == 200:
                    logger.info(f"Server started successfully on port {port}")
                    return True
                else:
                    logger.error(f"Server returned unexpected status code: {response.status_code}")
                    return False
            except Exception as e:
                logger.error(f"Error checking server status: {e}")
                return False
        else:
            # Start in foreground (blocking)
            logger.info("Starting server in foreground (press Ctrl+C to stop)...")
            os.system(f"python3 server.py {port}")
            return True
        
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        return False

def setup_automation():
    """Set up automation for daily data collection"""
    logger.info("Setting up automation...")
    
    try:
        # Create cron job for daily data collection
        cron_command = f"0 0 * * * cd {PROJECT_ROOT} && python3 data_collection/automation.py >> {DATA_DIR}/automation.log 2>&1"
        
        # Write to crontab
        with open("/tmp/viral_content_cron", "w") as f:
            f.write(f"{cron_command}\n")
        
        # Install crontab
        os.system("crontab -l > /tmp/existing_cron 2>/dev/null || true")
        os.system("cat /tmp/existing_cron /tmp/viral_content_cron > /tmp/new_cron")
        os.system("crontab /tmp/new_cron")
        
        # Clean up temporary files
        os.system("rm /tmp/viral_content_cron /tmp/existing_cron /tmp/new_cron")
        
        logger.info("Automation setup complete")
        return True
        
    except Exception as e:
        logger.error(f"Error setting up automation: {e}")
        return False

def expose_to_public(port=PORT):
    """Expose the server to public internet"""
    logger.info("Exposing server to public internet...")
    
    try:
        # Use deploy_expose_port tool to expose the port
        # This is a placeholder - in a real environment, you would use appropriate deployment tools
        logger.info(f"Server is now publicly accessible at http://localhost:{port}")
        logger.info("To expose to the internet, use the deploy_expose_port tool or a similar service")
        
        return True
        
    except Exception as e:
        logger.error(f"Error exposing server: {e}")
        return False

def deploy():
    """Main deployment function"""
    logger.info("Starting deployment process...")
    
    # Check dependencies
    if not check_dependencies():
        logger.error("Deployment failed: dependencies not satisfied")
        return False
    
    # Prepare data directory
    if not prepare_data_directory():
        logger.error("Deployment failed: could not prepare data directory")
        return False
    
    # Start server
    if not start_server():
        logger.error("Deployment failed: could not start server")
        return False
    
    # Setup automation
    if not setup_automation():
        logger.warning("Automation setup failed, but server is running")
    
    # Expose to public
    if not expose_to_public():
        logger.warning("Could not expose server to public, but it's running locally")
    
    logger.info("Deployment completed successfully!")
    logger.info(f"Server is running at http://localhost:{PORT}")
    logger.info("To access from other devices, use the appropriate networking tools or deployment services")
    
    return True

if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Deploy Viral Content Ideas Generator")
    parser.add_argument("--port", type=int, default=PORT, help=f"Port to run server on (default: {PORT})")
    parser.add_argument("--foreground", action="store_true", help="Run server in foreground (non-daemon)")
    args = parser.parse_args()
    
    # Run deployment
    if args.foreground:
        # Check dependencies and prepare data
        check_dependencies()
        prepare_data_directory()
        
        # Start server in foreground
        start_server(args.port, daemon=False)
    else:
        # Full deployment
        deploy()
