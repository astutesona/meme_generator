const videoElement = document.getElementById('webcam');
const canvasElement = document.getElementById('output_canvas');
const canvasCtx = canvasElement.getContext('2d');
const toggleCameraBtn = document.getElementById('toggleCamera');
const fpsCounter = document.getElementById('fpsCounter');

let cameraActive = false;
let camera = null;
let lastFrameTime = 0;
let frameCount = 0;

// Initialize MediaPipe Hands
const hands = new Hands({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
}});
hands.setOptions({
  maxNumHands: 2,
  modelComplexity: 1,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5
});
hands.onResults(onResults);

function onResults(results) {
  // FPS calculation
  const now = performance.now();
  frameCount++;
  if (now - lastFrameTime >= 1000) {
      fpsCounter.innerText = `FPS: ${frameCount}`;
      frameCount = 0;
      lastFrameTime = now;
  }

  // Draw landmarks
  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  canvasCtx.drawImage(
      results.image, 0, 0, canvasElement.width, canvasElement.height);
  
  if (results.multiHandLandmarks) {
    for (const landmarks of results.multiHandLandmarks) {
      drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS,
                     {color: '#00FF00', lineWidth: 2});
      drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 1});
    }
    
    // Throttle socket emitting (e.g., every 5 frames) to avoid overloading the server
    if (frameCount % 5 === 0 && window.socket) {
        // Send ALL hands to the server for complex two-hand gesture logic (e.g., Namaste, Heart)
        window.socket.emit('process_landmarks', { landmarks: results.multiHandLandmarks });
    }
  }
  canvasCtx.restore();
}

// Removed simulateGestureDetection as backend now handles it.

// Camera Toggle Logic
toggleCameraBtn.addEventListener('click', () => {
    if (!cameraActive) {
        startCamera();
    } else {
        stopCamera();
    }
});

function startCamera() {
    // Adjust canvas size to video size
    videoElement.style.display = 'block';
    
    camera = new Camera(videoElement, {
        onFrame: async () => {
            canvasElement.width = videoElement.videoWidth;
            canvasElement.height = videoElement.videoHeight;
            await hands.send({image: videoElement});
        },
        width: 640,
        height: 480
    });
    camera.start();
    cameraActive = true;
    toggleCameraBtn.innerHTML = '<i class="fa-solid fa-video"></i>';
    toggleCameraBtn.classList.replace('btn-outline-info', 'btn-danger');
}

function stopCamera() {
    if (camera) {
        camera.stop();
    }
    videoElement.style.display = 'none';
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    cameraActive = false;
    toggleCameraBtn.innerHTML = '<i class="fa-solid fa-video-slash"></i>';
    toggleCameraBtn.classList.replace('btn-danger', 'btn-outline-info');
    fpsCounter.innerText = 'FPS: 0';
}
