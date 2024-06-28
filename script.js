let videoQueue = [];
const videoPlayer = document.getElementById('videoPlayer');

function submitText() {
    const text = document.getElementById('textInput').value;
    if (text.trim() !== "") {
        fetchVideos(text);
    }
    document.getElementById('textInput').value = ""; // Clear input
}

function fetchVideos(paragraph) {
    fetch('/get_videos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ paragraph })
    })
    .then(response => response.json())
    .then(data => {
        videoQueue = data.map(video => video[1]); // Assuming URL is the second item in each video tuple
        if (videoQueue.length > 0) {
            playNextVideo();
        }
    })
    .catch(error => console.error('Error fetching videos:', error));
}

function playNextVideo() {
    if (videoQueue.length > 0) {
        const nextVideoUrl = videoQueue.shift();
        videoPlayer.src = nextVideoUrl;
        videoPlayer.play();
    }
}

videoPlayer.addEventListener('ended', playNextVideo);