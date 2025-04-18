#!/usr/bin/env python3
"""
Test Module for Viral Content Ideas Generator
"""

import os
import sys
import json
import unittest
import tempfile
import shutil
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_collection.instagram import get_profile_data, get_recent_videos, identify_viral_videos
from data_collection.youtube import get_channel_data, get_recent_shorts
from data_collection.tiktok import get_account_data, get_recent_videos as get_tiktok_videos
from data_collection.facebook import get_page_data, get_recent_reels
from data_collection.viral_identification import normalize_video_data, select_top_viral_videos
from data_collection.database import VideoDatabase

class TestDataCollection(unittest.TestCase):
    """Test data collection functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_instagram_data_collection(self):
        """Test Instagram data collection"""
        # Test profile data
        profile = get_profile_data("test_profile")
        self.assertIsNotNone(profile)
        self.assertEqual(profile["username"], "test_profile")
        
        # Test video collection
        videos = get_recent_videos("test_profile", days=1, count=5)
        self.assertIsNotNone(videos)
        self.assertLessEqual(len(videos), 5)
        
        # Test viral video identification
        viral_videos = identify_viral_videos(videos)
        self.assertIsNotNone(viral_videos)
    
    def test_youtube_data_collection(self):
        """Test YouTube data collection"""
        # Test channel data
        channel = get_channel_data("test_channel")
        self.assertIsNotNone(channel)
        self.assertEqual(channel["id"], "test_channel")
        
        # Test video collection
        videos = get_recent_shorts("test_channel", days=1, count=5)
        self.assertIsNotNone(videos)
        self.assertLessEqual(len(videos), 5)
    
    def test_tiktok_data_collection(self):
        """Test TikTok data collection"""
        # Test account data
        account = get_account_data("test_account")
        self.assertIsNotNone(account)
        self.assertEqual(account["username"], "test_account")
        
        # Test video collection
        videos = get_tiktok_videos("test_account", days=1, count=5)
        self.assertIsNotNone(videos)
        self.assertLessEqual(len(videos), 5)
    
    def test_facebook_data_collection(self):
        """Test Facebook data collection"""
        # Test page data
        page = get_page_data("test_page")
        self.assertIsNotNone(page)
        self.assertEqual(page["id"], "test_page")
        
        # Test video collection
        videos = get_recent_reels("test_page", days=1, count=5)
        self.assertIsNotNone(videos)
        self.assertLessEqual(len(videos), 5)

class TestViralIdentification(unittest.TestCase):
    """Test viral video identification functionality"""
    
    def test_normalize_video_data(self):
        """Test video data normalization"""
        # Create test videos from different platforms
        test_videos = [
            {
                "id": "123",
                "platform": "instagram",
                "profile": "test_profile",
                "title": "Test Instagram Video",
                "url": "https://instagram.com/p/123",
                "thumbnail": "https://example.com/thumb1.jpg",
                "views": 10000,
                "performance_ratio": 3.5,
                "post_date": "2025-04-10T12:00:00"
            },
            {
                "id": "456",
                "platform": "youtube",
                "channel_id": "test_channel",
                "title": "Test YouTube Video",
                "url": "https://youtube.com/shorts/456",
                "thumbnail": "https://example.com/thumb2.jpg",
                "views": 20000,
                "performance_ratio": 4.2,
                "post_date": "2025-04-11T12:00:00",
                "videoId": "456"
            }
        ]
        
        # Normalize videos
        normalized = normalize_video_data(test_videos)
        
        # Check normalization results
        self.assertEqual(len(normalized), 2)
        self.assertEqual(normalized[0]["platform"], "instagram")
        self.assertEqual(normalized[0]["creator"], "test_profile")
        self.assertEqual(normalized[1]["platform"], "youtube")
        self.assertEqual(normalized[1]["creator"], "test_channel")
        self.assertEqual(normalized[1]["videoId"], "456")
    
    def test_select_top_viral_videos(self):
        """Test top viral video selection"""
        # Create test videos with different performance ratios
        test_videos = [
            {"id": "1", "performance_ratio": 5.0},
            {"id": "2", "performance_ratio": 3.0},
            {"id": "3", "performance_ratio": 7.0},
            {"id": "4", "performance_ratio": 1.5},
            {"id": "5", "performance_ratio": 4.0}
        ]
        
        # Select top 3 videos with ratio >= 3.0
        top_videos = select_top_viral_videos(test_videos, count=3, min_ratio=3.0)
        
        # Check selection results
        self.assertEqual(len(top_videos), 3)
        self.assertEqual(top_videos[0]["id"], "3")  # Highest ratio (7.0)
        self.assertEqual(top_videos[1]["id"], "1")  # Second highest (5.0)
        self.assertEqual(top_videos[2]["id"], "5")  # Third highest (4.0)

class TestDatabase(unittest.TestCase):
    """Test database functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for test database
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test.db")
        self.db = VideoDatabase(self.db_path)
    
    def tearDown(self):
        """Clean up test environment"""
        # Close database connection
        self.db.close()
        
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_add_profile(self):
        """Test adding a profile to the database"""
        # Create test profile
        profile = {
            "id": "test_profile",
            "platform": "instagram",
            "name": "Test Profile",
            "follower_count": 10000,
            "last_updated": datetime.now().isoformat()
        }
        
        # Add profile to database
        self.db.add_profile(profile)
        
        # Check if profile was added
        self.db.cursor.execute("SELECT * FROM profiles WHERE id = ?", ("test_profile",))
        result = self.db.cursor.fetchone()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "test_profile")
        self.assertEqual(result[1], "instagram")
    
    def test_add_video(self):
        """Test adding a video to the database"""
        # Create test video
        video = {
            "id": "test_video",
            "platform": "youtube",
            "channel_id": "test_channel",
            "title": "Test Video",
            "url": "https://youtube.com/watch?v=test_video",
            "thumbnail": "https://example.com/thumb.jpg",
            "views": 10000,
            "performance_ratio": 3.5,
            "post_date": datetime.now().isoformat()
        }
        
        # Add video to database
        self.db.add_video(video)
        
        # Check if video was added
        self.db.cursor.execute("SELECT * FROM videos WHERE id = ?", ("test_video",))
        result = self.db.cursor.fetchone()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "test_video")
        self.assertEqual(result[1], "youtube")
        self.assertEqual(result[2], "test_channel")
    
    def test_add_daily_top_videos(self):
        """Test adding daily top videos to the database"""
        # Create test videos
        videos = [
            {
                "id": "video1",
                "platform": "instagram",
                "profile": "profile1",
                "title": "Video 1",
                "url": "https://instagram.com/p/video1",
                "views": 10000,
                "performance_ratio": 3.5,
                "post_date": datetime.now().isoformat()
            },
            {
                "id": "video2",
                "platform": "youtube",
                "channel_id": "channel1",
                "title": "Video 2",
                "url": "https://youtube.com/watch?v=video2",
                "views": 20000,
                "performance_ratio": 4.2,
                "post_date": datetime.now().isoformat()
            }
        ]
        
        # Add videos to database
        test_date = "2025-04-14"
        self.db.add_daily_top_videos(videos, test_date)
        
        # Check if daily top videos were added
        self.db.cursor.execute("SELECT * FROM daily_top_videos WHERE date = ?", (test_date,))
        results = self.db.cursor.fetchall()
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0], test_date)
        self.assertEqual(results[0][1], "video1")
        self.assertEqual(results[0][2], 1)  # Rank
        self.assertEqual(results[1][0], test_date)
        self.assertEqual(results[1][1], "video2")
        self.assertEqual(results[1][2], 2)  # Rank

if __name__ == "__main__":
    unittest.main()
