#!/usr/bin/env python3
"""
YouTube Shorts Data Collection Module for Viral Content Ideas Generator
"""

import os
import json
import time
import random
import requests
from datetime import datetime, timedelta

# Constants
API_KEY = "MOCK_API_KEY"  # In a real implementation, this would be a valid YouTube API key
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Sample YouTube channels focused on self-improvement, inspirational stories, and books
YOUTUBE_CHANNELS = [
    "UCfzlCWGWYyIQ0aLC5w48gBQ",  # Valuetainment
    "UCnYMOamNKLGVlJgRUbamveA",  # Matt D'Avella
    "UCJ24N4O0bP7LGLBDvye7oCA",  # Ali Abdaal
    "UCfbLDMh6uGOZePAfqqjVZ-g",  # Thomas Frank
    "UCG-vvPTyh24D9ScKdxvOvxg"   # The Better Ideas
]

def get_channel_data(channel_id):
    """
    Get channel data from YouTube API
    
    Note: This is a simplified version for demonstration purposes.
    In a production environment, you would use the actual YouTube API.
    """
    print(f"Fetching data for YouTube channel: {channel_id}")
    
    # In a real implementation, this would use YouTube's API
    # For demonstration, we'll generate mock data
    
    # Simulate API delay
    time.sleep(random.uniform(1, 2))
    
    # Generate mock channel data
    channel_data = {
        "id": channel_id,
        "title": f"Channel {channel_id[-5:]}",
        "description": "A channel about self-improvement and inspiration",
        "subscriber_count": random.randint(100000, 5000000),
        "video_count": random.randint(100, 1000),
        "view_count": random.randint(10000000, 500000000),
        "last_updated": datetime.now().isoformat()
    }
    
    return channel_data

def get_recent_shorts(channel_id, days=7, count=20):
    """
    Get recent YouTube Shorts from a channel
    
    Args:
        channel_id: YouTube channel ID
        days: Number of days to look back
        count: Maximum number of videos to return
        
    Returns:
        List of video data dictionaries
    """
    print(f"Fetching recent shorts for YouTube channel: {channel_id}")
    
    # In a real implementation, this would use YouTube's API
    # For demonstration, we'll generate mock data
    
    # Simulate API delay
    time.sleep(random.uniform(2, 4))
    
    videos = []
    
    # Generate mock video data
    for i in range(count):
        # Random date within the specified days range
        post_date = datetime.now() - timedelta(days=random.uniform(0, days))
        
        # Generate view count with some randomness to create "viral" videos
        base_views = random.randint(10000, 100000)
        # Make some videos viral (>2x average)
        is_viral = random.random() < 0.3
        view_multiplier = random.uniform(2.1, 15.0) if is_viral else random.uniform(0.5, 1.9)
        views = int(base_views * view_multiplier)
        
        # Generate a random video ID (11 characters)
        video_id = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-') for _ in range(11))
        
        video = {
            "id": video_id,
            "platform": "youtube",
            "channel_id": channel_id,
            "title": f"{'Viral ' if is_viral else ''}Short about Self-Improvement #{i+1}",
            "description": f"This is a {'viral' if is_viral else 'regular'} YouTube Short about self-improvement and inspiration.",
            "url": f"https://www.youtube.com/shorts/{video_id}",
            "thumbnail": f"https://picsum.photos/seed/{video_id}/500/500",
            "views": views,
            "likes": int(views * random.uniform(0.05, 0.2)),
            "comments": int(views * random.uniform(0.01, 0.05)),
            "post_date": post_date.isoformat(),
            "duration": random.randint(15, 60),
            "is_short": True,
            "performance_ratio": round(view_multiplier, 1),
            "videoId": video_id  # For embedding
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

def collect_youtube_data(output_dir="../data", channels=None):
    """
    Main function to collect YouTube data
    
    Args:
        output_dir: Directory to save output files
        channels: List of YouTube channel IDs to collect data from
    """
    if channels is None:
        channels = YOUTUBE_CHANNELS
    
    os.makedirs(output_dir, exist_ok=True)
    
    all_videos = []
    channel_data = {}
    
    # Collect data for each channel
    for channel_id in channels:
        try:
            # Get channel data
            channel_info = get_channel_data(channel_id)
            channel_data[channel_id] = channel_info
            
            # Get recent shorts
            videos = get_recent_shorts(channel_id)
            all_videos.extend(videos)
            
            # Save channel-specific data
            save_to_json(videos, f"{output_dir}/{channel_id}_videos.json")
            
        except Exception as e:
            print(f"Error collecting data for {channel_id}: {e}")
    
    # Identify viral videos across all channels
    viral_videos = identify_viral_videos(all_videos)
    
    # Sort by performance ratio (descending)
    viral_videos.sort(key=lambda x: x["performance_ratio"], reverse=True)
    
    # Take top 10 viral videos
    top_viral_videos = viral_videos[:10]
    
    # Save combined data
    save_to_json(channel_data, f"{output_dir}/youtube_channels.json")
    save_to_json(all_videos, f"{output_dir}/all_youtube_videos.json")
    save_to_json(top_viral_videos, f"{output_dir}/top_youtube_viral_videos.json")
    
    return top_viral_videos

if __name__ == "__main__":
    collect_youtube_data()
