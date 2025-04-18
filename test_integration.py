#!/usr/bin/env python3
"""
Integration Test Script for Viral Content Ideas Generator
"""

import os
import sys
import time
import logging
import subprocess
import requests
import signal
import atexit

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("integration_test")

# Constants
SERVER_PORT = 8000
SERVER_URL = f"http://localhost:{SERVER_PORT}"
SERVER_PROCESS = None

def start_server():
    """Start the web server"""
    global SERVER_PROCESS
    
    logger.info("Starting web server...")
    
    # Change to project root directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Start server process
    SERVER_PROCESS = subprocess.Popen(
        ["python3", "server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Register cleanup function
    atexit.register(stop_server)
    
    # Wait for server to start
    time.sleep(3)
    
    logger.info(f"Server started at {SERVER_URL}")

def stop_server():
    """Stop the web server"""
    global SERVER_PROCESS
    
    if SERVER_PROCESS:
        logger.info("Stopping web server...")
        
        # Send SIGTERM to server process
        SERVER_PROCESS.terminate()
        
        # Wait for process to terminate
        SERVER_PROCESS.wait(timeout=5)
        
        logger.info("Server stopped")

def test_server_running():
    """Test if server is running"""
    try:
        response = requests.get(SERVER_URL)
        assert response.status_code == 200
        logger.info("Server is running and responding to requests")
        return True
    except (requests.RequestException, AssertionError) as e:
        logger.error(f"Server is not running or not responding: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    # Test videos endpoint
    try:
        response = requests.get(f"{SERVER_URL}/api/videos?day_offset=0&platform=all")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        logger.info(f"Videos API endpoint working, returned {len(data)} videos")
    except (requests.RequestException, AssertionError) as e:
        logger.error(f"Videos API endpoint test failed: {e}")
        return False
    
    # Test dates endpoint
    try:
        response = requests.get(f"{SERVER_URL}/api/dates")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        logger.info(f"Dates API endpoint working, returned {len(data)} dates")
    except (requests.RequestException, AssertionError) as e:
        logger.error(f"Dates API endpoint test failed: {e}")
        return False
    
    return True

def test_platform_filtering():
    """Test platform filtering functionality"""
    platforms = ["all", "instagram", "youtube", "tiktok", "facebook"]
    
    for platform in platforms:
        try:
            response = requests.get(f"{SERVER_URL}/api/videos?day_offset=0&platform={platform}")
            assert response.status_code == 200
            data = response.json()
            
            if platform != "all" and data:
                # Check that all videos are from the specified platform
                for video in data:
                    assert video["platform"] == platform
            
            logger.info(f"Platform filtering for '{platform}' working, returned {len(data)} videos")
        except (requests.RequestException, AssertionError) as e:
            logger.error(f"Platform filtering test for '{platform}' failed: {e}")
            return False
    
    return True

def test_historical_browsing():
    """Test historical browsing functionality"""
    # Test with different day offsets
    for day_offset in range(3):
        try:
            response = requests.get(f"{SERVER_URL}/api/videos?day_offset={day_offset}&platform=all")
            assert response.status_code == 200
            data = response.json()
            
            logger.info(f"Historical browsing for day_offset={day_offset} working, returned {len(data)} videos")
        except (requests.RequestException, AssertionError) as e:
            logger.error(f"Historical browsing test for day_offset={day_offset} failed: {e}")
            return False
    
    return True

def run_integration_tests():
    """Run all integration tests"""
    logger.info("Starting integration tests...")
    
    # Start server
    start_server()
    
    # Run tests
    tests = [
        ("Server Running", test_server_running),
        ("API Endpoints", test_api_endpoints),
        ("Platform Filtering", test_platform_filtering),
        ("Historical Browsing", test_historical_browsing)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        logger.info(f"Running test: {test_name}")
        
        if test_func():
            logger.info(f"✅ Test passed: {test_name}")
        else:
            logger.error(f"❌ Test failed: {test_name}")
            all_passed = False
    
    # Stop server
    stop_server()
    
    # Print summary
    if all_passed:
        logger.info("🎉 All integration tests passed!")
    else:
        logger.error("❌ Some integration tests failed")
    
    return all_passed

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
