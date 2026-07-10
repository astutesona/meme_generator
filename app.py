from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from database.models import db, User, History, Gesture
import os

from core.gesture_detector import GestureDetector
from core.reaction_engine import ReactionEngine
from core.emotion_detector import EmotionDetector

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize Core AI Modules
gesture_detector = GestureDetector()
reaction_engine = ReactionEngine()
emotion_detector = EmotionDetector()

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('register'))
            
        new_user = User(username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/process_landmarks', methods=['POST'])
def handle_landmarks():
    data = request.json
    hands_landmarks = data.get('landmarks', [])
    if not hands_landmarks or len(hands_landmarks) == 0:
        return jsonify({"error": "No landmarks found"}), 400
    
    # 1. Recognize Gesture
    gesture_name = gesture_detector.recognize_gesture(hands_landmarks)
    
    # 2. Recognize Emotion (stubbed to Neutral as we aren't sending frames yet)
    emotion = "Neutral"
    
    # 3. Get Reaction
    reaction_data = reaction_engine.get_reaction(gesture_name, emotion)
    
    # 4. Add confidence (mock for rule-based, would be actual probability from a model)
    reaction_data['confidence'] = 0.95 if gesture_name != "Unknown" else 0.0
    
    # Return back to client
    return jsonify(reaction_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
