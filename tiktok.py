#!/usr/bin/env python3
"""
TikTok Data Collection Module for Viral Content Ideas Generator
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

# Sample TikTok accounts focused on self-improvement, inspirational stories, and books
TIKTOK_ACCOUNTS = [
    "motivation",
    "selfimprovement",
    "mindsetcoach",
    "bookclub",
    "inspirationdaily"
]

def get_account_data(username):
    """
    Get account data from TikTok
    
    Note: This is a simplified version for demonstration purposes.
    In a production environment, you would use proper TikTok API or scraping methods.
    """
    print(f"Fetching data for TikTok account: {username}")
    
    # In a real implementation, this would use TikTok's API or a proper scraping method
    # For demonstration, we'll generate mock data
    
    # Simulate API delay
    time.sleep(random.uniform(1, 2))
    
    # Generate mock account data
    account_data = {
        "username": username,
        "display_name": username.title(),
        "bio": f"Self-improvement and inspiration content creator | {random.randint(5, 20)} years experience",
        "follower_count": random.randint(50000, 2000000),
        "following_count": random.randint(100, 2000),
        "video_count": random.randint(50, 500),
        "like_count": random.randint(500000, 10000000),
        "verified": random.choice([True, False]),
        "last_updated": datetime.now().isoformat()
    }
    
    return account_data

def get_recent_videos(username, days=7, count=20):
    """
    Get recent videos from a TikTok account
    
    Args:
        username: TikTok username
        days: Number of days to look back
        count: Maximum number of videos to return
        
    Returns:
        List of video data dictionaries
    """
    print(f"Fetching recent videos for TikTok account: {username}")
    
    # In a real implementation, this would use TikTok's API or a proper scraping method
    # For demonstration, we'll generate mock data
    
    # Simulate API delay
    time.sleep(random.uniform(2, 4))
    
    videos = []
    
    # Generate mock video data
    for i in range(count):
        # Random date within the specified days range
        post_date = datetime.now() - timedelta(days=random.uniform(0, days))
        
        # Generate view count with some randomness to create "viral" videos
        base_views = random.randint(20000, 200000)
        # Make some videos viral (>2x average)
        is_viral = random.random() < 0.3
        view_multiplier = random.uniform(2.1, 20.0) if is_viral else random.uniform(0.5, 1.9)
        views = int(base_views * view_multiplier)
        
        # Generate a random video ID
        video_id = ''.join(random.choice('0123456789') for _ in range(19))
        
        video = {
            "id": video_id,
            "platform": "tiktok",
            "username": username,
            "title": f"{'Viral ' if is_viral else ''}Self-Improvement Tip #{i+1}",
            "description": f"#{username} #{random.choice(['motivation', 'selfimprovement', 'success', 'mindset', 'growth'])}",
            "url": f"https://www.tiktok.com/@{username}/video/{video_id}",
            "thumbnail": f"https://picsum.photos/seed/tiktok_{username}_{i}/500/500",
            "views": views,
            "likes": int(views * random.uniform(0.1, 0.3)),
            "comments": int(views * random.uniform(0.01, 0.05)),
            "shares": int(views * random.uniform(0.01, 0.1)),
            "post_date": post_date.isoformat(),
            "duration": random.randint(15, 60),
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

def collect_tiktok_data(output_dir="../data", accounts=None):
    """
    Main function to collect TikTok data
    
    Args:
        output_dir: Directory to save output files
        accounts: List of TikTok accounts to collect data from
    """
    if accounts is None:
        accounts = TIKTOK_ACCOUNTS
    
    os.makedirs(output_dir, exist_ok=True)
    
    all_videos = []
    account_data = {}
    
    # Collect data for each account
    for username in accounts:
        try:
            # Get account data
            account_info = get_account_data(username)
            account_data[username] = account_info
            
            # Get recent videos
            videos = get_recent_videos(username)
            all_videos.extend(videos)
            
            # Save account-specific data
            save_to_json(videos, f"{output_dir}/{username}_videos.json")
            
        except Exception as e:
            print(f"Error collecting data for {username}: {e}")
    
    # Identify viral videos across all accounts
    viral_videos = identify_viral_videos(all_videos)
    
    # Sort by performance ratio (descending)
    viral_videos.sort(key=lambda x: x["performance_ratio"], reverse=True)
    
    # Take top 10 viral videos
    top_viral_videos = viral_videos[:10]
    
    # Save combined data
    save_to_json(account_data, f"{output_dir}/tiktok_accounts.json")
    save_to_json(all_videos, f"{output_dir}/all_tiktok_videos.json")
    save_to_json(top_viral_videos, f"{output_dir}/top_tiktok_viral_videos.json")
    
    return top_viral_videos

if __name__ == "__main__":
    collect_tiktok_data()
