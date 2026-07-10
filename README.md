# AI Gesture-to-Meme & Emotion Reaction System

An intelligent real-time system that captures hand gestures through a webcam, recognizes them using Computer Vision, and instantly displays emojis, funny memes, AI-generated captions, voice responses, and reaction sounds.

**Built for MCA Final Year Major Project.**

## Features
- Real-time webcam processing using MediaPipe Hands (Client-side for 30+ FPS).
- Recognizes 22 distinct hand gestures.
- Dynamic generation of Emojis, Captions, Text-to-Speech (TTS), and Memes.
- User authentication, Profile, and Analytics Dashboard.
- Dark mode, glassmorphism UI, GSAP animations.
- SQLite database to store user history and analytics.

## Tech Stack
- **Backend**: Python 3, Flask, Flask-SocketIO, SQLite, Flask-Login.
- **Frontend**: HTML5, CSS3, JS, Bootstrap 5, GSAP, Chart.js.
- **Computer Vision**: MediaPipe (JS wrapper), backend heuristic gesture classifier.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd gesture_meme
   ```

2. **Create a virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python app.py
   ```
   Access the app at `http://127.0.0.1:5000`

4. **Generate Documentation (Report & PPT script):**
   ```bash
   python utils/document_generator.py
   ```

## Deployment Guide

### GitHub
1. Initialize git: `git init`
2. Add files: `git add .`
3. Commit: `git commit -m "Initial Commit"`
4. Push to remote: `git push -u origin main`

### Render / Railway
1. Create a `Procfile` with: `web: gunicorn -k eventlet -w 1 app:app`
2. Connect your GitHub repository to the Render/Railway dashboard.
3. Deploy!

## Software Engineering Diagrams
Use the generated `docs/Project_Report.md` as the base for your SRS. ER Diagrams and UMLs can be conceptualized directly from the `database/models.py`.

## Future Enhancements
- Fine-tune a custom TensorFlow model for gesture recognition instead of heuristics.
- Integrate DeepFace for real-time Face Emotion detection.
- LLM API integration for dynamic caption generation.
