# Viral Content Ideas Generator - Requirements Analysis

## Project Overview
The project requires building an internal tool that helps generate viral content ideas from short videos on social media platforms. The tool will focus on self-improvement, inspirational stories, and books for organic marketing of a book summary app.

## Key Requirements

### Data Collection
- **Platforms**: Instagram, TikTok, YouTube Shorts, and Facebook Reels
- **Starting Profiles**:
  - SEI Come SEI (Instagram)
  - Founders Podcast (Instagram)
  - Matt Gray (Instagram)
  - Alex Hormozi (Instagram)
  - Online Marketing ES (Instagram)
- **Expansion**: Need to include functionality to add more profiles in the target niches
- **Collection Methods**:
  - Instagram: Scraping tools (Instaloader, Apify's Instagram Scrapers)
  - YouTube Shorts: YouTube Data API
  - TikTok: Available APIs or scraping tools
  - Facebook Reels: Suitable scraping methods or APIs

### Viral Video Identification
- Collect videos posted in the last 7 days from each profile
- Calculate average view count for each profile based on last 20 videos
- Identify videos with view counts at least 2X the average
- Select top 10 viral videos daily based on view count and relevance to niches

### Database Requirements
- Store selected videos with timestamps
- Database options: SQLite (simpler) or PostgreSQL (more robust)
- Need to store: video links, view counts, performance ratios, timestamps, platform source

### Website Interface
- Display daily top 10 viral videos
- Include embedded videos where possible
- Show view counts and performance ratios (e.g., 5.1X average views)
- Allow historical browsing (scroll back to previous days)
- Simple, functional design for internal use

### Automation
- Daily scheduled runs
- Handle API rate limits and authentication
- Respect platform policies to avoid blocks
- Implement delays between requests

## Technical Considerations
- Need to handle different embedding methods for different platforms
- Authentication requirements vary by platform
- Rate limiting considerations for each API
- Error handling for API failures or changes
- Cross-platform data normalization

## Development Approach
Based on the requirements, a Next.js application with a built-in database would be most appropriate, as it provides:
- Server-side rendering for better performance
- API routes for data collection scripts
- Built-in scheduling capabilities
- Integrated database functionality
- Component-based UI for the video displays
