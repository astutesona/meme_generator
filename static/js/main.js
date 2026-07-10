document.addEventListener('DOMContentLoaded', () => {
    // Theme Toggle Logic
    const themeToggleBtn = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;
    const icon = themeToggleBtn.querySelector('i');

    // Check local storage for theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setTheme(savedTheme);

    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = htmlElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    });

    function setTheme(theme) {
        htmlElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Update Icon
        if (theme === 'dark') {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
            themeToggleBtn.classList.replace('btn-outline-dark', 'btn-outline-light');
        } else {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
            themeToggleBtn.classList.replace('btn-outline-light', 'btn-outline-dark');
        }
    }

    // Animate updates with GSAP and play audio/TTS
    window.updateUI = function(data) {
        const { gesture, emoji, confidence, caption, meme_url, sound } = data;

        // Always update confidence
        document.getElementById('confidenceDisplay').innerHTML = `Confidence: <span class="fw-bold text-success">${(confidence * 100).toFixed(1)}%</span>`;

        // If gesture hasn't changed, don't re-trigger heavy DOM updates and GSAP animations
        if (window.lastGesture === gesture) {
            return;
        }
        
        // Optionally ignore 'Unknown' to prevent flickering if hand tracking drops for a single frame
        if (gesture === 'Unknown' && window.lastGesture !== undefined) {
            return;
        }

        window.lastGesture = gesture;
        
        // Text to Speech
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel(); // Cancel any ongoing speech to prevent queue build up
            const utterance = new SpeechSynthesisUtterance(caption);
            utterance.rate = 1.1;
            window.speechSynthesis.speak(utterance);
        }

        // Play Sound (Assuming sounds are in static/sounds folder)
        if (sound) {
            const audio = new Audio(`/static/sounds/${sound}`);
            audio.play().catch(e => console.log('Audio play failed:', e));
        }

        // Update Text
        document.getElementById('gestureName').innerText = gesture;
        document.getElementById('aiCaption').innerText = `"${caption}"`;

        // Update Image
        const memeImg = document.getElementById('memeDisplay');
        if (meme_url) {
            memeImg.src = meme_url;
            memeImg.classList.remove('d-none');
        }

        // GSAP Animations
        gsap.killTweensOf(".caption-box");
        gsap.fromTo(".caption-box", { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5 });
    }
});
