#!/usr/bin/env python3
"""
Automation Module for Viral Content Ideas Generator
"""

import os
import sys
import time
import logging
import schedule
import random
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_collection.instagram import collect_instagram_data
from data_collection.youtube import collect_youtube_data
from data_collection.tiktok import collect_tiktok_data
from data_collection.facebook import collect_facebook_data
from data_collection.viral_identification import identify_viral_videos
from data_collection.database import initialize_database

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/automation.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("automation")

# Constants
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

def collect_all_platform_data():
    """Collect data from all platforms with rate limiting and error handling"""
    logger.info("Starting data collection from all platforms")
    
    try:
        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Collect data from each platform with random delays to avoid rate limiting
        logger.info("Collecting Instagram data")
        instagram_videos = collect_instagram_data(DATA_DIR)
        time.sleep(random.uniform(5, 10))  # Random delay between platforms
        
        logger.info("Collecting YouTube data")
        youtube_videos = collect_youtube_data(DATA_DIR)
        time.sleep(random.uniform(5, 10))
        
        logger.info("Collecting TikTok data")
        tiktok_videos = collect_tiktok_data(DATA_DIR)
        time.sleep(random.uniform(5, 10))
        
        logger.info("Collecting Facebook data")
        facebook_videos = collect_facebook_data(DATA_DIR)
        
        # Identify viral videos across all platforms
        logger.info("Identifying viral videos across all platforms")
        top_viral_videos = identify_viral_videos(DATA_DIR, generate_samples=False)
        
        # Initialize database and import new data
        logger.info("Updating database with new data")
        db = initialize_database(DATA_DIR)
        
        logger.info(f"Data collection completed successfully. Found {len(top_viral_videos)} viral videos.")
        return True
    
    except Exception as e:
        logger.error(f"Error during data collection: {e}")
        return False

def run_daily_job():
    """Run the daily data collection job"""
    logger.info("Running daily data collection job")
    
    # Record start time
    start_time = time.time()
    
    # Run data collection
    success = collect_all_platform_data()
    
    # Record end time and calculate duration
    end_time = time.time()
    duration = end_time - start_time
    
    if success:
        logger.info(f"Daily job completed successfully in {duration:.2f} seconds")
    else:
        logger.error(f"Daily job failed after {duration:.2f} seconds")

def setup_schedule():
    """Set up the daily schedule"""
    # Schedule the job to run daily at midnight UTC
    schedule.every().day.at("00:00").do(run_daily_job)
    
    logger.info("Scheduled daily data collection job for 00:00 UTC")

def run_scheduler():
    """Run the scheduler loop"""
    setup_schedule()
    
    logger.info("Starting scheduler. Press Ctrl+C to exit.")
    
    try:
        # Run the job immediately on startup
        run_daily_job()
        
        # Then run the scheduler loop
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Scheduler error: {e}")

if __name__ == "__main__":
    run_scheduler()
