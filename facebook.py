#!/usr/bin/env python3
"""
Facebook Reels Data Collection Module for Viral Content Ideas Generator
"""

import os
import json
import time
import random
import requests
from datetime import datetime, timedelta

# Constants
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Sample Facebook pages focused on self-improvement, inspirational stories, and books
FACEBOOK_PAGES = [
    "mindsetmentor",
    "selfimprovementdaily",
    "motivationmafia",
    "bookloversclub",
    "successmindset"
]

def get_page_data(page_id):
    """
    Get page data from Facebook
    
    Note: This is a simplified version for demonstration purposes.
    In a production environment, you would use the Facebook Graph API.
    """
    print(f"Fetching data for Facebook page: {page_id}")
    
    # In a real implementation, this would use Facebook's Graph API
    # For demonstration, we'll generate mock data
    
    # Simulate API delay
    time.sleep(random.uniform(1, 2))
    
    # Generate mock page data
    page_data = {
        "id": page_id,
        "name": page_id.replace("_", " ").title(),
        "category": random.choice(["Education", "Personal Blog", "Book", "Public Figure"]),
        "description": f"A page dedicated to self-improvement and inspiration",
        "fan_count": random.randint(50000, 3000000),
        "talking_about_count": random.randint(1000, 50000),
        "verified": random.choice([True, False]),
        "last_updated": datetime.now().isoformat()
    }
    
    return page_data

def get_recent_reels(page_id, days=7, count=20):
    """
    Get recent Facebook Reels from a page
    
    Args:
        page_id: Facebook page ID
        days: Number of days to look back
        count: Maximum number of videos to return
        
    Returns:
        List of video data dictionaries
    """
    print(f"Fetching recent reels for Facebook page: {page_id}")
    
    # In a real implementation, this would use Facebook's Graph API
    # For demonstration, we'll generate mock data
    
    # Simulate API delay
    time.sleep(random.uniform(2, 4))
    
    videos = []
    
    # Generate mock video data
    for i in range(count):
        # Random date within the specified days range
        post_date = datetime.now() - timedelta(days=random.uniform(0, days))
        
        # Generate view count with some randomness to create "viral" videos
        base_views = random.randint(15000, 150000)
        # Make some videos viral (>2x average)
        is_viral = random.random() < 0.3
        view_multiplier = random.uniform(2.1, 12.0) if is_viral else random.uniform(0.5, 1.9)
        views = int(base_views * view_multiplier)
        
        # Generate a random video ID
        video_id = ''.join(random.choice('0123456789') for _ in range(15))
        
        video = {
            "id": video_id,
            "platform": "facebook",
            "page_id": page_id,
            "title": f"{'Viral ' if is_viral else ''}Self-Improvement Reel #{i+1}",
            "description": f"This is a {'viral' if is_viral else 'regular'} Facebook Reel about self-improvement and inspiration.",
            "url": f"https://www.facebook.com/reel/{video_id}",
            "thumbnail": f"https://picsum.photos/seed/facebook_{page_id}_{i}/500/500",
            "views": views,
            "likes": int(views * random.uniform(0.05, 0.2)),
            "comments": int(views * random.uniform(0.01, 0.05)),
            "shares": int(views * random.uniform(0.01, 0.1)),
            "post_date": post_date.isoformat(),
            "duration": random.randint(15, 60),
            "is_reel": True,
            "performance_ratio": round(view_multiplier, 1)
        }
        
        videos.append(video)
    
    # Sort by views (descending)
    videos.sort(key=lambda x: x["views"], reverse=True)
    
    return videos

def calculate_average_views(videos):
    """Calculate the average view count for a list of videos"""
    if not videos:
        return 0
    
    total_views = sum(video["views"] for video in videos)
    return total_views / len(videos)

def identify_viral_videos(videos, min_ratio=2.0):
    """
    Identify viral videos based on view count compared to average
    
    Args:
        videos: List of video data dictionaries
        min_ratio: Minimum ratio of views to average to be considered viral
        
    Returns:
        List of viral video data dictionaries
    """
    if not videos:
        return []
    
    avg_views = calculate_average_views(videos)
    
    viral_videos = []
    for video in videos:
        ratio = video["views"] / avg_views if avg_views > 0 else 0
        
        if ratio >= min_ratio:
            # Add performance ratio to video data
            video["performance_ratio"] = round(ratio, 1)
            viral_videos.append(video)
    
    return viral_videos

def save_to_json(data, filename):
    """Save data to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")

def collect_facebook_data(output_dir="../data", pages=None):
    """
    Main function to collect Facebook data
    
    Args:
        output_dir: Directory to save output files
        pages: List of Facebook page IDs to collect data from
    """
    if pages is None:
        pages = FACEBOOK_PAGES
    
    os.makedirs(output_dir, exist_ok=True)
    
    all_videos = []
    page_data = {}
    
    # Collect data for each page
    for page_id in pages:
        try:
            # Get page data
            page_info = get_page_data(page_id)
            page_data[page_id] = page_info
            
            # Get recent reels
            videos = get_recent_reels(page_id)
            all_videos.extend(videos)
            
            # Save page-specific data
            save_to_json(videos, f"{output_dir}/{page_id}_videos.json")
            
        except Exception as e:
            print(f"Error collecting data for {page_id}: {e}")
    
    # Identify viral videos across all pages
    viral_videos = identify_viral_videos(all_videos)
    
    # Sort by performance ratio (descending)
    viral_videos.sort(key=lambda x: x["performance_ratio"], reverse=True)
    
    # Take top 10 viral videos
    top_viral_videos = viral_videos[:10]
    
    # Save combined data
    save_to_json(page_data, f"{output_dir}/facebook_pages.json")
    save_to_json(all_videos, f"{output_dir}/all_facebook_videos.json")
    save_to_json(top_viral_videos, f"{output_dir}/top_facebook_viral_videos.json")
    
    return top_viral_videos

if __name__ == "__main__":
    collect_facebook_data()
