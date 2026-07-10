import random

class ReactionEngine:
    def __init__(self):
        # Database of reactions mapped by gesture
        self.reactions = {
            "Thumbs Up": {
                "emoji": "👍",
                "captions": [
                    "Mission Successfully Completed.",
                    "Great job!",
                    "Everything is awesome.",
                    "Approved!"
                ],
                "sound": "success.wav"
            },
            "Thumbs Down": {
                "emoji": "👎",
                "captions": [
                    "Mission Failed. We'll get 'em next time.",
                    "Not good enough.",
                    "Disapproved.",
                    "Try again."
                ],
                "sound": "fail.wav"
            },
            "Peace": {
                "emoji": "✌️",
                "captions": [
                    "Keeping life stress-free.",
                    "Peace out!",
                    "Chill vibes only.",
                    "Harmony and balance."
                ],
                "sound": "peace.wav"
            },
            "Fist": {
                "emoji": "✊",
                "captions": [
                    "Ready for battle.",
                    "Stay strong.",
                    "Power to the people.",
                    "Determination."
                ],
                "sound": "punch.wav"
            },
            "OK": {
                "emoji": "👌",
                "captions": [
                    "Absolutely perfect.",
                    "Got it!",
                    "Everything is fine.",
                    "Flawless."
                ],
                "sound": "notification.wav"
            },
            "Rock": {
                "emoji": "🤘",
                "captions": [
                    "Rock on!",
                    "Let's get loud.",
                    "Heavy metal vibes.",
                    "Party time!"
                ],
                "sound": "rock.wav"
            },
            "Call Me": {
                "emoji": "🤙",
                "captions": [
                    "Hit me up.",
                    "Call me later.",
                    "Hang loose.",
                    "Stay in touch."
                ],
                "sound": "ring.wav"
            },
            "Five Fingers": {
                "emoji": "🖐️",
                "captions": [
                    "Stop right there.",
                    "High five!",
                    "Talk to the hand.",
                    "I see you."
                ],
                "sound": "slap.wav"
            },
            "One Finger": {
                "emoji": "☝️",
                "captions": ["Wait a minute.", "I have a point.", "Look up there."],
                "sound": "notification.wav"
            },
            "Two Fingers": {
                "emoji": "✌️",
                "captions": ["Peace!", "Two of them."],
                "sound": "peace.wav"
            },
            "Three Fingers": {
                "emoji": "3️⃣",
                "captions": ["Three is the magic number.", "Trifecta."],
                "sound": "success.wav"
            },
            "Four Fingers": {
                "emoji": "4️⃣",
                "captions": ["Almost a full hand.", "Four!"],
                "sound": "success.wav"
            },
            "Point Left/Right": {
                "emoji": "👈👉",
                "captions": ["Check that out.", "Look over there.", "This way!"],
                "sound": "notification.wav"
            },
            "Love": {
                "emoji": "🤟",
                "captions": ["I love you too!", "Spreading the love.", "Much love."],
                "sound": "success.wav"
            },
            "Namaste": {
                "emoji": "🙏",
                "captions": ["Namaste.", "Greetings.", "Respect and peace.", "Welcome."],
                "sound": "peace.wav"
            },
            "Heart Gesture": {
                "emoji": "🫶",
                "captions": ["Sending you my heart.", "Pure love.", "Heart to heart."],
                "sound": "success.wav"
            },
            "Finger Heart": {
                "emoji": "🫰",
                "captions": ["Saranghae!", "Finger heart!", "Tiny love."],
                "sound": "success.wav"
            },
            "Unknown": {
                "emoji": "🤔",
                "captions": [
                    "What does that mean?",
                    "I don't recognize this gesture.",
                    "Are you trying to tell me something?",
                    "Processing..."
                ],
                "sound": "hmm.wav"
            }
        }
        
    def get_reaction(self, gesture_name, emotion="Neutral"):
        """ Generate a dynamic reaction based on gesture and emotion. """
        
        # Fallback to unknown if gesture not explicitly mapped
        data = self.reactions.get(gesture_name, self.reactions["Unknown"])
        
        emoji = data["emoji"]
        # AI Caption Generator logic (simplified by random choice for now)
        caption = random.choice(data["captions"])
        sound = data["sound"]
        
        # Combine with Emotion for advanced combinations (Rule 24)
        if emotion == "Happy" and gesture_name == "Peace":
            caption = "Ultimate joy and peace!"
            emoji = "✌️😁"
        elif emotion == "Angry" and gesture_name == "Fist":
            caption = "Furious and ready to strike!"
            emoji = "✊😡"
            
        # Map specific gestures to lists of memes (saved in static/memes)
        meme_map = {
            "Thumbs Up": ["thik_hai.jpg", "ok_madam.jpg"],
            "Thumbs Down": ["facepalm.jpg", "kya_kru.jpg"],
            "Call Me": ["hot.jpg"],
            "Point Left/Right": ["loser.jpg", "kaun_sikha.jpg"],
            "One Finger": ["kaun_sikha.jpg"],
            "Two Fingers": ["i_dont_care.jpg"],
            "Peace": ["i_dont_care.jpg"],
            "Three Fingers": ["big3.jpg"],
            "Four Fingers": ["kya_kru.jpg"],
            "Five Fingers": ["kasam_se.jpg"],
            "Fist": ["ab_tu_gaya_beta.jpg"],
            "Love": ["miss_you.jpg", "u_dont_love_me.jpg"],
            "Heart Gesture": ["kissing_heart.jpg", "dino.jpg"],
            "Finger Heart": ["finger_heart.jpg"],
            "OK": ["thik_hai.jpg"]
        }
        
        # Select the specific meme for the gesture, or fallback to placeholder
        memes_list = meme_map.get(gesture_name, ["placeholder_meme.png"])
        meme_filename = random.choice(memes_list)
        
        # In a real app, this would query the DB for the Meme table
        meme_url = f"/static/memes/{meme_filename}" 
        
        return {
            "gesture": gesture_name,
            "emoji": emoji,
            "caption": caption,
            "sound": sound,
            "meme_url": meme_url,
            "emotion": emotion
        }
