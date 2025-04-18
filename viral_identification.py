#!/usr/bin/env python3
"""
Cross-Platform Viral Video Identification Module for Viral Content Ideas Generator
"""

import os
import json
import time
from datetime import datetime, timedelta
import random  # Only for sample data generation

def load_json_data(filename):
    """Load data from a JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filename}: {e}")
        return []

def save_to_json(data, filename):
    """Save data to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")

def combine_platform_videos(data_dir="../data"):
    """
    Combine viral videos from all platforms
    
    Args:
        data_dir: Directory containing platform-specific data files
        
    Returns:
        List of all viral videos across platforms
    """
    all_viral_videos = []
    
    # Load viral videos from each platform
    platforms = ["instagram", "youtube", "tiktok", "facebook"]
    
    for platform in platforms:
        try:
            filename = f"{data_dir}/top_{platform}_viral_videos.json"
            videos = load_json_data(filename)
            if videos:
                all_viral_videos.extend(videos)
                print(f"Loaded {len(videos)} viral videos from {platform}")
        except Exception as e:
            print(f"Error loading {platform} viral videos: {e}")
    
    return all_viral_videos

def normalize_video_data(videos):
    """
    Normalize video data across platforms to ensure consistent format
    
    Args:
        videos: List of video data dictionaries from different platforms
        
    Returns:
        List of normalized video data dictionaries
    """
    normalized_videos = []
    
    for video in videos:
        # Ensure all required fields exist
        normalized_video = {
            "id": video.get("id", ""),
            "platform": video.get("platform", "unknown"),
            "title": video.get("title", "Untitled Video"),
            "url": video.get("url", ""),
            "thumbnail": video.get("thumbnail", ""),
            "views": video.get("views", 0),
            "performance_ratio": video.get("performance_ratio", 1.0),
            "post_date": video.get("post_date", datetime.now().isoformat()),
        }
        
        # Add platform-specific fields
        if video.get("platform") == "youtube":
            normalized_video["videoId"] = video.get("videoId", video.get("id", ""))
        
        # Add profile/channel/account information
        if "profile" in video:
            normalized_video["creator"] = video["profile"]
        elif "channel_id" in video:
            normalized_video["creator"] = video["channel_id"]
        elif "username" in video:
            normalized_video["creator"] = video["username"]
        elif "page_id" in video:
            normalized_video["creator"] = video["page_id"]
        else:
            normalized_video["creator"] = "Unknown Creator"
        
        normalized_videos.append(normalized_video)
    
    return normalized_videos

def select_top_viral_videos(videos, count=10, min_ratio=2.0):
    """
    Select top viral videos across all platforms
    
    Args:
        videos: List of normalized video data dictionaries
        count: Number of top videos to select
        min_ratio: Minimum performance ratio to be considered viral
        
    Returns:
        List of top viral video data dictionaries
    """
    # Filter videos by minimum performance ratio
    viral_videos = [v for v in videos if v.get("performance_ratio", 0) >= min_ratio]
    
    # Sort by performance ratio (descending)
    viral_videos.sort(key=lambda x: x.get("performance_ratio", 0), reverse=True)
    
    # Take top N videos
    top_videos = viral_videos[:count]
    
    return top_videos

def generate_daily_data(top_videos, data_dir="../data", day_offset=0):
    """
    Generate daily data file for the frontend
    
    Args:
        top_videos: List of top viral video data dictionaries
        data_dir: Directory to save output files
        day_offset: Day offset (0 for today, 1 for yesterday, etc.)
    """
    # Save to daily file
    filename = f"{data_dir}/videos-{day_offset}.json"
    save_to_json(top_videos, filename)
    
    # Also save as sample data if it's today's data
    if day_offset == 0:
        save_to_json(top_videos, f"{data_dir}/sample-videos.json")
    
    return filename

def generate_sample_data(data_dir="../data", count=10):
    """
    Generate sample data for testing
    
    Args:
        data_dir: Directory to save output files
        count: Number of sample videos to generate
        
    Returns:
        List of sample video data dictionaries
    """
    os.makedirs(data_dir, exist_ok=True)
    
    platforms = ["instagram", "youtube", "tiktok", "facebook"]
    sample_videos = []
    
    for i in range(count):
        platform = random.choice(platforms)
        
        # Generate view count with viral performance
        base_views = random.randint(10000, 200000)
        performance_ratio = round(random.uniform(2.1, 15.0), 1)
        views = int(base_views * performance_ratio)
        
        # Generate video ID based on platform
        if platform == "youtube":
            video_id = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-') for _ in range(11))
        elif platform == "tiktok":
            video_id = ''.join(random.choice('0123456789') for _ in range(19))
        elif platform == "facebook":
            video_id = ''.join(random.choice('0123456789') for _ in range(15))
        else:  # instagram
            video_id = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for _ in range(11))
        
        # Create sample video data
        video = {
            "id": video_id,
            "platform": platform,
            "title": f"Viral Self-Improvement Video #{i+1}",
            "url": f"https://www.{platform}.com/{'' if platform == 'facebook' else '@'}{'reel/' if platform == 'facebook' else ''}{'shorts/' if platform == 'youtube' else ''}{video_id}",
            "thumbnail": f"https://picsum.photos/seed/{platform}_{i}/500/500",
            "views": views,
            "performance_ratio": performance_ratio,
            "post_date": (datetime.now() - timedelta(days=random.uniform(0, 7))).isoformat(),
            "creator": f"{platform.title()}Creator{i}"
        }
        
        # Add platform-specific fields
        if platform == "youtube":
            video["videoId"] = video_id
        
        sample_videos.append(video)
    
    # Sort by performance ratio (descending)
    sample_videos.sort(key=lambda x: x["performance_ratio"], reverse=True)
    
    # Save sample data
    save_to_json(sample_videos, f"{data_dir}/sample-videos.json")
    save_to_json(sample_videos, f"{data_dir}/videos-0.json")
    
    return sample_videos

def identify_viral_videos(data_dir="../data", generate_samples=True):
    """
    Main function to identify viral videos across platforms
    
    Args:
        data_dir: Directory containing platform-specific data files
        generate_samples: Whether to generate sample data if real data is not available
        
    Returns:
        List of top viral video data dictionaries
    """
    os.makedirs(data_dir, exist_ok=True)
    
    # Try to combine real data from all platforms
    all_videos = combine_platform_videos(data_dir)
    
    # If no real data is available and samples are requested, generate sample data
    if not all_videos and generate_samples:
        print("No real data available. Generating sample data...")
        return generate_sample_data(data_dir)
    
    # Normalize video data
    normalized_videos = normalize_video_data(all_videos)
    
    # Select top viral videos
    top_videos = select_top_viral_videos(normalized_videos)
    
    # Generate daily data file
    generate_daily_data(top_videos, data_dir)
    
    return top_videos

if __name__ == "__main__":
    # Run the viral video identification process
    top_viral_videos = identify_viral_videos()
    print(f"Identified {len(top_viral_videos)} top viral videos across all platforms")
