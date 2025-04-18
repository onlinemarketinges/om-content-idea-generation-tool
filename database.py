#!/usr/bin/env python3
"""
Database Module for Viral Content Ideas Generator
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta

class VideoDatabase:
    """Database class for storing and retrieving viral videos"""
    
    def __init__(self, db_path="../data/viral_videos.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.initialize_db()
    
    def initialize_db(self):
        """Initialize database and create tables if they don't exist"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Connect to database
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            name TEXT NOT NULL,
            url TEXT,
            follower_count INTEGER,
            last_updated TEXT
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            profile_id TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            thumbnail TEXT,
            views INTEGER NOT NULL,
            performance_ratio REAL NOT NULL,
            post_date TEXT NOT NULL,
            collection_date TEXT NOT NULL,
            FOREIGN KEY (profile_id) REFERENCES profiles (id)
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_top_videos (
            date TEXT NOT NULL,
            video_id TEXT NOT NULL,
            rank INTEGER NOT NULL,
            PRIMARY KEY (date, video_id),
            FOREIGN KEY (video_id) REFERENCES videos (id)
        )
        ''')
        
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def add_profile(self, profile_data):
        """
        Add or update a profile in the database
        
        Args:
            profile_data: Dictionary containing profile information
        """
        profile_id = profile_data.get('id') or profile_data.get('username')
        platform = profile_data.get('platform', 'unknown')
        name = profile_data.get('name') or profile_data.get('display_name') or profile_data.get('full_name') or profile_id
        url = profile_data.get('url', f"https://www.{platform}.com/{profile_id}")
        follower_count = profile_data.get('follower_count', 0)
        last_updated = profile_data.get('last_updated', datetime.now().isoformat())
        
        self.cursor.execute('''
        INSERT OR REPLACE INTO profiles (id, platform, name, url, follower_count, last_updated)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (profile_id, platform, name, url, follower_count, last_updated))
        
        self.conn.commit()
    
    def add_video(self, video_data):
        """
        Add a video to the database
        
        Args:
            video_data: Dictionary containing video information
        """
        video_id = video_data.get('id')
        platform = video_data.get('platform', 'unknown')
        
        # Determine profile_id based on platform
        if platform == 'instagram':
            profile_id = video_data.get('profile')
        elif platform == 'youtube':
            profile_id = video_data.get('channel_id')
        elif platform == 'tiktok':
            profile_id = video_data.get('username')
        elif platform == 'facebook':
            profile_id = video_data.get('page_id')
        else:
            profile_id = video_data.get('creator', 'unknown')
        
        title = video_data.get('title', 'Untitled Video')
        url = video_data.get('url', '')
        thumbnail = video_data.get('thumbnail', '')
        views = video_data.get('views', 0)
        performance_ratio = video_data.get('performance_ratio', 1.0)
        post_date = video_data.get('post_date', datetime.now().isoformat())
        collection_date = datetime.now().isoformat()
        
        self.cursor.execute('''
        INSERT OR REPLACE INTO videos 
        (id, platform, profile_id, title, url, thumbnail, views, performance_ratio, post_date, collection_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (video_id, platform, profile_id, title, url, thumbnail, views, performance_ratio, post_date, collection_date))
        
        self.conn.commit()
    
    def add_daily_top_videos(self, videos, date=None):
        """
        Add top videos for a specific date
        
        Args:
            videos: List of video dictionaries
            date: Date string (ISO format), defaults to today
        """
        if date is None:
            date = datetime.now().date().isoformat()
        
        # First, add all videos to the videos table
        for video in videos:
            self.add_video(video)
        
        # Then, add entries to daily_top_videos
        for rank, video in enumerate(videos, 1):
            video_id = video.get('id')
            
            self.cursor.execute('''
            INSERT OR REPLACE INTO daily_top_videos (date, video_id, rank)
            VALUES (?, ?, ?)
            ''', (date, video_id, rank))
        
        self.conn.commit()
    
    def get_top_videos_by_date(self, date=None, limit=10):
        """
        Get top videos for a specific date
        
        Args:
            date: Date string (ISO format), defaults to today
            limit: Maximum number of videos to return
            
        Returns:
            List of video dictionaries
        """
        if date is None:
            date = datetime.now().date().isoformat()
        
        self.cursor.execute('''
        SELECT v.* FROM videos v
        JOIN daily_top_videos d ON v.id = d.video_id
        WHERE d.date = ?
        ORDER BY d.rank
        LIMIT ?
        ''', (date, limit))
        
        columns = [column[0] for column in self.cursor.description]
        videos = []
        
        for row in self.cursor.fetchall():
            video = dict(zip(columns, row))
            videos.append(video)
        
        return videos
    
    def get_dates_with_data(self, limit=30):
        """
        Get dates that have top videos data
        
        Args:
            limit: Maximum number of dates to return
            
        Returns:
            List of date strings (ISO format)
        """
        self.cursor.execute('''
        SELECT DISTINCT date FROM daily_top_videos
        ORDER BY date DESC
        LIMIT ?
        ''', (limit,))
        
        dates = [row[0] for row in self.cursor.fetchall()]
        return dates
    
    def import_from_json(self, json_file):
        """
        Import videos from a JSON file
        
        Args:
            json_file: Path to JSON file containing video data
            
        Returns:
            Number of videos imported
        """
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                videos = json.load(f)
            
            if not isinstance(videos, list):
                print(f"Error: {json_file} does not contain a list of videos")
                return 0
            
            # Extract date from filename if possible
            filename = os.path.basename(json_file)
            date = None
            
            if filename.startswith('videos-'):
                try:
                    day_offset = int(filename.split('-')[1].split('.')[0])
                    date = (datetime.now() - timedelta(days=day_offset)).date().isoformat()
                except (ValueError, IndexError):
                    date = None
            
            # Add videos to database
            self.add_daily_top_videos(videos, date)
            
            return len(videos)
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error importing from {json_file}: {e}")
            return 0
    
    def export_to_json(self, output_file, date=None):
        """
        Export top videos for a date to a JSON file
        
        Args:
            output_file: Path to output JSON file
            date: Date string (ISO format), defaults to today
            
        Returns:
            Number of videos exported
        """
        videos = self.get_top_videos_by_date(date)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(videos, f, indent=2)
            
            return len(videos)
            
        except Exception as e:
            print(f"Error exporting to {output_file}: {e}")
            return 0

def initialize_database(data_dir="../data"):
    """
    Initialize database and import existing JSON data
    
    Args:
        data_dir: Directory containing JSON data files
        
    Returns:
        VideoDatabase instance
    """
    db = VideoDatabase(f"{data_dir}/viral_videos.db")
    
    # Import sample data if it exists
    sample_file = f"{data_dir}/sample-videos.json"
    if os.path.exists(sample_file):
        print(f"Importing sample data from {sample_file}")
        db.import_from_json(sample_file)
    
    # Import any daily data files
    for filename in os.listdir(data_dir):
        if filename.startswith('videos-') and filename.endswith('.json'):
            file_path = os.path.join(data_dir, filename)
            print(f"Importing data from {file_path}")
            db.import_from_json(file_path)
    
    return db

if __name__ == "__main__":
    # Initialize database and import existing data
    db = initialize_database()
    
    # Print some stats
    dates = db.get_dates_with_data()
    print(f"Database contains data for {len(dates)} dates")
    
    for date in dates:
        videos = db.get_top_videos_by_date(date)
        print(f"{date}: {len(videos)} videos")
    
    db.close()
