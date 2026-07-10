import os

def generate_report(output_dir="docs"):
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "Project_Report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# AI Gesture-to-Meme & Emotion Reaction System\n\n")
        f.write("## 1. Abstract\n")
        f.write("This project proposes an intelligent real-time system that captures hand gestures and face emotions via webcam, and instantly generates a dynamic reaction containing emojis, memes, and AI captions.\n\n")
        f.write("## 2. Introduction\n")
        f.write("With the rise of non-verbal digital communication, this system bridges the gap between human gestures and digital meme culture...\n\n")
        f.write("## 3. System Architecture\n")
        f.write("- **Frontend:** HTML5, CSS3, JS, Bootstrap 5, GSAP\n")
        f.write("- **Backend:** Python, Flask, Flask-SocketIO\n")
        f.write("- **AI Modules:** MediaPipe Hands, OpenCV\n")
        f.write("- **Database:** SQLite\n\n")
        f.write("## 4. Implementation Details\n")
        f.write("The system detects 21 hand landmarks and uses a heuristic algorithm to classify 22 distinct gestures...\n\n")
        f.write("## 5. Conclusion\n")
        f.write("The AI Gesture-to-Meme system successfully demonstrates the integration of real-time computer vision with dynamic UI rendering for interactive communication.\n")

def generate_ppt_script(output_dir="docs"):
    os.makedirs(output_dir, exist_ok=True)
    ppt_path = os.path.join(output_dir, "Presentation_Script.md")
    with open(ppt_path, "w", encoding="utf-8") as f:
        f.write("# Slide 1: Title\n")
        f.write("**Title:** AI Gesture-to-Meme, Emoji & Emotion Reaction System\n")
        f.write("**Subtitle:** MCA Final Year Project\n\n")
        f.write("# Slide 2: Problem Statement\n")
        f.write("- Traditional communication lacks instant, personalized meme generation.\n")
        f.write("- Need for a seamless gesture-to-meme bridge.\n\n")
        f.write("# Slide 3: Proposed Solution\n")
        f.write("- Real-time webcam integration.\n")
        f.write("- 22 gestures supported.\n")
        f.write("- Dynamic AI reaction generation (Meme, TTS, Sound).\n\n")
        f.write("# Slide 4: Tech Stack\n")
        f.write("- Python, Flask, MediaPipe, OpenCV, SocketIO, Bootstrap 5.\n\n")
        f.write("# Slide 5-20: Architecture, ER Diagrams, UI Demo, Conclusion...\n")

if __name__ == "__main__":
    generate_report()
    generate_ppt_script()
    print("Documentation generated in docs/ folder.")
