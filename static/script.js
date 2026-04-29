// Face Recognition System JavaScript

// Global variables
let videoElement;
let statusElement;
let accuracyElement;
let isProcessing = false;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeFaceRecognition();
});

function initializeFaceRecognition() {
    videoElement = document.getElementById('video');
    statusElement = document.getElementById('status');
    accuracyElement = document.getElementById('accuracy');
    
    if (!videoElement || !statusElement) {
        console.error('Required elements not found');
        return;
    }
    
    // Start webcam access
    accessWebcam();
    
    // Start face checking interval
    setInterval(checkFace, 1000);
}

function accessWebcam() {
    navigator.mediaDevices.getUserMedia({ 
        video: { 
            facingMode: "user",
            width: { ideal: 640 },
            height: { ideal: 480 }
        }, 
        audio: false 
    })
    .then(stream => {
        videoElement.srcObject = stream;
        updateStatus('Camera initialized', 'waiting');
    })
    .catch(err => {
        console.error('Camera access error:', err);
        updateStatus('Camera access denied: ' + err.message, 'closed');
    });
}

function captureFrame() {
    if (!videoElement.videoWidth || !videoElement.videoHeight) {
        return null;
    }
    
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg', 0.8);
}

async function checkFace() {
    if (isProcessing) return;
    
    isProcessing = true;
    
    try {
        const imageData = captureFrame();
        if (!imageData) {
            isProcessing = false;
            return;
        }
        
        const response = await fetch('https://your-backend-url.replit.app/check_face', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                image: imageData 
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        updateUI(data);
        
    } catch (error) {
        console.error('Face check error:', error);
        updateStatus('Server connection error', 'closed');
    } finally {
        isProcessing = false;
    }
}

function updateUI(data) {
    // Update status
    if (data.matched) {
        updateStatus('✅ Folder Opened', 'opened');
    } else if (data.status === "closed") {
        updateStatus('❌ Folder Closed', 'closed');
    } else {
        updateStatus('⌛ Waiting for Match...', 'waiting');
    }
    
    // Update accuracy
    if (data.accuracy !== undefined) {
        updateAccuracy(data.accuracy);
    }
    
    // Update video border
    updateVideoBorder(data);
}

function updateStatus(message, statusClass) {
    if (statusElement) {
        statusElement.textContent = message;
        statusElement.className = statusClass;
    }
}

function updateAccuracy(accuracy) {
    if (accuracyElement) {
        accuracyElement.textContent = `Face Accuracy: ${accuracy}%`;
    }
}

function updateVideoBorder(data) {
    if (!videoElement) return;
    
    // Remove all video classes
    videoElement.classList.remove('video-opened', 'video-closed', 'video-waiting');
    
    // Add appropriate class based on status
    if (data.matched) {
        videoElement.classList.add('video-opened');
    } else if (data.status === "closed") {
        videoElement.classList.add('video-closed');
    } else {
        videoElement.classList.add('video-waiting');
    }
}

// Utility functions
function showMessage(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
}

// Export functions for global access if needed
window.FaceRecognition = {
    initializeFaceRecognition,
    accessWebcam,
    checkFace,
    captureFrame
};
