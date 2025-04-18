#!/usr/bin/env python3
"""
Instagram Data Collection Module for Viral Content Ideas Generator
"""

import os
import json
import time
import random
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Constants
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Starting profiles from requirements
INSTAGRAM_PROFILES = [
    "sei.come.sei",
    "founderspodcast",
    "matthgray",
    "hormozi",
    "onlinemarketinges.co"
]

def get_profile_data(username):
    """
    Scrape basic profile data from Instagram
    
    Note: This is a simplified version for demonstration purposes.
    In a production environment, you would need to handle authentication,
    rate limiting, and use official APIs where available.
    """
    print(f"Fetching data for Instagram profile: {username}")
    
    # In a real implementation, this would use Instagram's API or a proper scraping method
    # For demonstration, we'll generate mock data
    
    # Simulate API delay
    time.sleep(random.uniform(1, 3))
    
    # Generate mock profile data
    profile_data = {
        "username": username,
        "full_name": f"{username.replace('.', ' ').title()}",
        "follower_count": random.randint(10000, 1000000),
        "following_count": random.randint(100, 5000),
        "post_count": random.randint(50, 500),
        "is_verified": random.choice([True, False]),
        "last_updated": datetime.now().isoformat()
    }
    
    return profile_data

def get_recent_videos(username, days=7, count=20):
    """
    Get recent videos from an Instagram profile
    
    Args:
        username: Instagram username
        days: Number of days to look back
        count: Maximum number of videos to return
        
    Returns:
        List of video data dictionaries
    """
    print(f"Fetching recent videos for Instagram profile: {username}")
    
    # In a real implementation, this would use Instagram's API or a proper scraping method
    # For demonstration, we'll generate mock data
    
    # Simulate API delay
    time.sleep(random.uniform(2, 5))
    
    videos = []
    
    # Generate mock video data
    for i in range(count):
        # Random date within the specified days range
        post_date = datetime.now() - timedelta(days=random.uniform(0, days))
        
        # Generate view count with some randomness to create "viral" videos
        base_views = random.randint(5000, 50000)
        # Make some videos viral (>2x average)
        is_viral = random.random() < 0.3
        view_multiplier = random.uniform(2.1, 10.0) if is_viral else random.uniform(0.5, 1.9)
        views = int(base_views * view_multiplier)
        
        video = {
            "id": f"{username}_{int(time.time())}_{i}",
            "platform": "instagram",
            "profile": username,
            "title": f"{'Viral ' if is_viral else ''}Content from {username}",
            "description": f"This is a {'viral' if is_viral else 'regular'} video about self-improvement and inspiration.",
            "url": f"https://www.instagram.com/{username}/p/{generate_random_id(11)}/",
            "thumbnail": f"https://picsum.photos/seed/{username}_{i}/500/500",
            "views": views,
            "likes": int(views * random.uniform(0.05, 0.2)),
            "comments": int(views * random.uniform(0.01, 0.05)),
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

def generate_random_id(length=11):
    """Generate a random ID string (similar to Instagram post IDs)"""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
    return ''.join(random.choice(chars) for _ in range(length))

def save_to_json(data, filename):
    """Save data to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")

def collect_instagram_data(output_dir="../data", profiles=None):
    """
    Main function to collect Instagram data
    
    Args:
        output_dir: Directory to save output files
        profiles: List of Instagram profiles to collect data from
    """
    if profiles is None:
        profiles = INSTAGRAM_PROFILES
    
    os.makedirs(output_dir, exist_ok=True)
    
    all_videos = []
    profile_data = {}
    
    # Collect data for each profile
    for username in profiles:
        try:
            # Get profile data
            profile_info = get_profile_data(username)
            profile_data[username] = profile_info
            
            # Get recent videos
            videos = get_recent_videos(username)
            all_videos.extend(videos)
            
            # Save profile-specific data
            save_to_json(videos, f"{output_dir}/{username}_videos.json")
            
        except Exception as e:
            print(f"Error collecting data for {username}: {e}")
    
    # Identify viral videos across all profiles
    viral_videos = identify_viral_videos(all_videos)
    
    # Sort by performance ratio (descending)
    viral_videos.sort(key=lambda x: x["performance_ratio"], reverse=True)
    
    # Take top 10 viral videos
    top_viral_videos = viral_videos[:10]
    
    # Save combined data
    save_to_json(profile_data, f"{output_dir}/instagram_profiles.json")
    save_to_json(all_videos, f"{output_dir}/all_instagram_videos.json")
    save_to_json(top_viral_videos, f"{output_dir}/top_instagram_viral_videos.json")
    
    # Save as sample data for the frontend
    save_to_json(top_viral_videos, f"{output_dir}/sample-videos.json")
    
    return top_viral_videos

if __name__ == "__main__":
    collect_instagram_data()
