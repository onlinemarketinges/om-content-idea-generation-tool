# Viral Content Ideas Generator - User Documentation

## Overview

The Viral Content Ideas Generator is an internal tool designed to help identify and analyze viral content from major social media platforms. The tool focuses on self-improvement, inspirational stories, and book-related content to support organic marketing of a book summary app.

## Key Features

- **Multi-Platform Data Collection**: Automatically collects data from Instagram, YouTube Shorts, TikTok, and Facebook Reels
- **Viral Content Identification**: Identifies videos that perform at least 2X better than the average for each profile
- **Daily Updates**: Refreshes with new viral content every day at midnight UTC
- **Historical Browsing**: Allows you to view viral content from previous days
- **Platform Filtering**: Filter content by specific platforms
- **Performance Metrics**: Shows view counts and performance ratios for each video

## Getting Started

### Accessing the Tool

The Viral Content Ideas Generator is accessible at:
- Local access: http://localhost:8000
- For remote access, use the exposed URL provided by your system administrator

### System Requirements

- Modern web browser (Chrome, Firefox, Safari, or Edge)
- Internet connection to view embedded videos

## Using the Interface

### Main Dashboard

The main dashboard displays the top 10 viral videos for the current day. Each video card includes:

1. **Video Embed/Thumbnail**: Click to watch the video (YouTube videos are embedded directly)
2. **Platform Badge**: Indicates the source platform (Instagram, YouTube, TikTok, or Facebook)
3. **Title**: The title of the video
4. **View Count**: Number of views the video has received
5. **Performance Ratio**: How many times better this video performed compared to the profile's average (e.g., 5.1X)

### Navigation and Filtering

- **Date Navigation**: Use the "Previous Day" and "Next Day" buttons to browse historical data
- **Platform Filter**: Use the dropdown menu to filter videos by platform

## Administration

### Deployment

To deploy the tool on a new server:

1. Clone the repository to your server
2. Navigate to the project directory
3. Run the deployment script:
   ```
   python3 deployment/deploy.py
   ```

This will:
- Check dependencies
- Prepare the data directory
- Start the web server
- Set up daily automation

For advanced options:
```
python3 deployment/deploy.py --help
```

### Manual Data Collection

To manually trigger data collection:

```
python3 data_collection/automation.py
```

### Adding New Profiles

To add new profiles for monitoring:

1. Edit the appropriate platform file in the `data_collection` directory:
   - `instagram.py` for Instagram profiles
   - `youtube.py` for YouTube channels
   - `tiktok.py` for TikTok accounts
   - `facebook.py` for Facebook pages

2. Add the new profile ID to the list of profiles at the top of the file

3. Restart the automation process or run a manual data collection

## Technical Details

### Architecture

The Viral Content Ideas Generator consists of:

1. **Data Collection Modules**: Python scripts for collecting data from social media platforms
2. **Viral Identification Algorithm**: Identifies videos that perform significantly better than average
3. **SQLite Database**: Stores video data, profile information, and daily top videos
4. **Web Server**: Serves the web interface and API endpoints
5. **Frontend Interface**: HTML, CSS, and JavaScript for user interaction

### Database Schema

The database contains three main tables:
- `profiles`: Stores information about social media profiles
- `videos`: Stores information about individual videos
- `daily_top_videos`: Links videos to specific dates for historical browsing

### API Endpoints

The tool provides two main API endpoints:
- `/api/videos?day_offset=0&platform=all`: Get videos for a specific day and platform
- `/api/dates`: Get a list of available dates with data

## Troubleshooting

### Common Issues

1. **No videos displayed**: 
   - Check if the data collection process ran successfully
   - Verify that the database file exists in the data directory
   - Check server logs for errors

2. **Cannot access the tool**:
   - Verify the server is running with `ps aux | grep server.py`
   - Check if the correct port is being used (default: 8000)
   - Ensure firewall settings allow access to the port

3. **Videos not embedding properly**:
   - Ensure your browser allows embedded content
   - Check internet connection to the video platforms

### Logs

Log files are stored in the `data` directory:
- `automation.log`: Contains logs from the automated data collection process

## Support

For additional support or feature requests, please contact the development team.

---

© 2025 Viral Content Ideas Generator | Internal Tool
