// Updated application JavaScript to connect with backend API
document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const videosContainer = document.getElementById('videos-container');
    const currentDateElement = document.getElementById('current-date');
    const prevDayButton = document.getElementById('prev-day');
    const nextDayButton = document.getElementById('next-day');
    const platformFilter = document.getElementById('platform-filter');
    
    // Application state
    let currentOffset = 0;
    let currentPlatformFilter = 'all';
    let videoData = [];
    
    // Initialize the application
    init();
    
    function init() {
        // Set current date display
        updateDateDisplay();
        
        // Load initial data
        loadVideoData(currentOffset, currentPlatformFilter);
        
        // Event listeners
        prevDayButton.addEventListener('click', goToPreviousDay);
        nextDayButton.addEventListener('click', goToNextDay);
        platformFilter.addEventListener('change', filterByPlatform);
    }
    
    function updateDateDisplay() {
        const date = new Date();
        date.setDate(date.getDate() - currentOffset);
        
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        currentDateElement.textContent = date.toLocaleDateString('en-US', options);
        
        // Disable next day button if we're at today
        nextDayButton.disabled = currentOffset === 0;
    }
    
    function goToPreviousDay() {
        currentOffset++;
        updateDateDisplay();
        loadVideoData(currentOffset, currentPlatformFilter);
    }
    
    function goToNextDay() {
        if (currentOffset > 0) {
            currentOffset--;
            updateDateDisplay();
            loadVideoData(currentOffset, currentPlatformFilter);
        }
    }
    
    function filterByPlatform(event) {
        currentPlatformFilter = event.target.value;
        loadVideoData(currentOffset, currentPlatformFilter);
    }
    
    function loadVideoData(dayOffset, platform) {
        // Show loading state
        videosContainer.innerHTML = '<div class="loading">Loading viral videos...</div>';
        
        // Fetch data from API
        fetch(`/api/videos?day_offset=${dayOffset}&platform=${platform}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                videoData = data;
                
                // Render videos
                renderVideos(videoData);
            })
            .catch(error => {
                console.error('Error loading video data:', error);
                
                // Try to load sample data if API fails
                fetch(`../data/videos-${dayOffset}.json`)
                    .then(response => {
                        if (!response.ok && dayOffset > 0) {
                            return fetch('../data/sample-videos.json');
                        }
                        return response.json();
                    })
                    .then(data => {
                        videoData = data;
                        
                        // Filter by platform if needed
                        if (platform !== 'all') {
                            videoData = videoData.filter(video => video.platform === platform);
                        }
                        
                        // Render videos
                        renderVideos(videoData);
                    })
                    .catch(fallbackError => {
                        console.error('Error loading fallback data:', fallbackError);
                        videosContainer.innerHTML = `
                            <div class="loading">
                                Error loading videos. Please try again later.
                            </div>
                        `;
                    });
            });
    }
    
    function renderVideos(videos) {
        if (videos.length === 0) {
            videosContainer.innerHTML = `
                <div class="loading">
                    No videos found for the selected filters.
                </div>
            `;
            return;
        }
        
        // Clear container
        videosContainer.innerHTML = '';
        
        // Add each video card
        videos.forEach(video => {
            const videoCard = document.createElement('div');
            videoCard.className = 'video-card';
            
            // Create embed based on platform
            let embedHTML = '';
            if (video.platform === 'youtube') {
                embedHTML = `
                    <div class="video-embed">
                        <iframe 
                            src="https://www.youtube.com/embed/${video.videoId || video.id}" 
                            frameborder="0" 
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                            allowfullscreen>
                        </iframe>
                    </div>
                `;
            } else {
                // For other platforms, show thumbnail with link
                embedHTML = `
                    <div class="video-embed">
                        <a href="${video.url}" target="_blank">
                            <img src="${video.thumbnail}" alt="${video.title}">
                        </a>
                    </div>
                `;
            }
            
            // Platform badge color
            let platformColor = '';
            switch(video.platform) {
                case 'instagram':
                    platformColor = '#E1306C';
                    break;
                case 'youtube':
                    platformColor = '#FF0000';
                    break;
                case 'tiktok':
                    platformColor = '#000000';
                    break;
                case 'facebook':
                    platformColor = '#1877F2';
                    break;
            }
            
            videoCard.innerHTML = `
                ${embedHTML}
                <div class="video-info">
                    <span class="video-platform" style="background-color: ${platformColor}; color: white;">
                        ${video.platform.charAt(0).toUpperCase() + video.platform.slice(1)}
                    </span>
                    <h3 class="video-title">${video.title}</h3>
                    <div class="video-stats">
                        <span>${video.views.toLocaleString()} views</span>
                        <span class="performance">${video.performance_ratio}X average</span>
                    </div>
                </div>
            `;
            
            videosContainer.appendChild(videoCard);
        });
    }
});
