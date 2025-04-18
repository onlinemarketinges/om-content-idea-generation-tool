#!/usr/bin/env python3
"""
Server Module for Viral Content Ideas Generator
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
import urllib.parse
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_collection.database import VideoDatabase

# Constants
PORT = 8000
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
PUBLIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")

class ViralContentHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler for Viral Content Ideas Generator"""
    
    def __init__(self, *args, **kwargs):
        self.db = VideoDatabase(os.path.join(DATA_DIR, "viral_videos.db"))
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        # Parse URL and query parameters
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # API endpoints
        if path.startswith('/api/'):
            self.handle_api_request(path, query_params)
            return
        
        # Serve static files from public directory
        if path == '/':
            self.path = '/index.html'
        
        # Adjust path to point to public directory
        self.path = os.path.join(PUBLIC_DIR, self.path.lstrip('/'))
        
        # Use default handler for static files
        try:
            super().do_GET()
        except FileNotFoundError:
            self.send_error(404, "File not found")
    
    def handle_api_request(self, path, query_params):
        """Handle API requests"""
        # Get videos for a specific date
        if path == '/api/videos':
            day_offset = int(query_params.get('day_offset', ['0'])[0])
            platform = query_params.get('platform', ['all'])[0]
            
            date = (datetime.now() - timedelta(days=day_offset)).date().isoformat()
            videos = self.db.get_top_videos_by_date(date)
            
            # Filter by platform if needed
            if platform != 'all':
                videos = [v for v in videos if v.get('platform') == platform]
            
            self.send_json_response(videos)
        
        # Get available dates with data
        elif path == '/api/dates':
            dates = self.db.get_dates_with_data()
            self.send_json_response(dates)
        
        # Unknown API endpoint
        else:
            self.send_error(404, "API endpoint not found")
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def run_server(port=PORT):
    """Run the HTTP server"""
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Initialize database with sample data if needed
    if not os.path.exists(os.path.join(DATA_DIR, "viral_videos.db")):
        from data_collection.viral_identification import generate_sample_data
        generate_sample_data(DATA_DIR)
        
        from data_collection.database import initialize_database
        initialize_database(DATA_DIR)
    
    # Set up HTTP server
    handler = lambda *args, **kwargs: ViralContentHandler(*args, **kwargs)
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Server running at http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
