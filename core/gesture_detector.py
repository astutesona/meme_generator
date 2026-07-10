import math

class GestureDetector:
    def __init__(self):
        # MediaPipe landmark indices
        self.WRIST = 0
        self.THUMB_CMC = 1
        self.THUMB_MCP = 2
        self.THUMB_IP = 3
        self.THUMB_TIP = 4
        
        self.INDEX_FINGER_MCP = 5
        self.INDEX_FINGER_PIP = 6
        self.INDEX_FINGER_DIP = 7
        self.INDEX_FINGER_TIP = 8
        
        self.MIDDLE_FINGER_MCP = 9
        self.MIDDLE_FINGER_PIP = 10
        self.MIDDLE_FINGER_DIP = 11
        self.MIDDLE_FINGER_TIP = 12
        
        self.RING_FINGER_MCP = 13
        self.RING_FINGER_PIP = 14
        self.RING_FINGER_DIP = 15
        self.RING_FINGER_TIP = 16
        
        self.PINKY_MCP = 17
        self.PINKY_PIP = 18
        self.PINKY_DIP = 19
        self.PINKY_TIP = 20

    def get_finger_states(self, landmarks):
        """ Returns a list of booleans indicating if each finger is extended (True) or folded (False).
            Order: [Thumb, Index, Middle, Ring, Pinky] """
        states = []
        
        if not landmarks:
            return states

        # Thumb: compare distance from thumb tip to pinky MCP vs thumb MCP to pinky MCP
        # This is more robust against hand rotation than comparing X/Y coords
        dist_thumb_to_pinky = math.dist((landmarks[self.THUMB_TIP]['x'], landmarks[self.THUMB_TIP]['y']),
                                        (landmarks[self.PINKY_MCP]['x'], landmarks[self.PINKY_MCP]['y']))
        dist_thumb_mcp_to_pinky = math.dist((landmarks[self.THUMB_MCP]['x'], landmarks[self.THUMB_MCP]['y']),
                                            (landmarks[self.PINKY_MCP]['x'], landmarks[self.PINKY_MCP]['y']))
        
        thumb_is_open = dist_thumb_to_pinky > dist_thumb_mcp_to_pinky * 1.1
        states.append(thumb_is_open)

        # Other fingers: A finger is extended if its tip is further from the wrist than its PIP joint
        fingers = [
            (self.INDEX_FINGER_TIP, self.INDEX_FINGER_PIP),
            (self.MIDDLE_FINGER_TIP, self.MIDDLE_FINGER_PIP),
            (self.RING_FINGER_TIP, self.RING_FINGER_PIP),
            (self.PINKY_TIP, self.PINKY_PIP)
        ]
        
        for tip, pip in fingers:
            dist_tip = math.dist((landmarks[tip]['x'], landmarks[tip]['y']), 
                                 (landmarks[self.WRIST]['x'], landmarks[self.WRIST]['y']))
            dist_pip = math.dist((landmarks[pip]['x'], landmarks[pip]['y']), 
                                 (landmarks[self.WRIST]['x'], landmarks[self.WRIST]['y']))
            
            is_up = dist_tip > dist_pip
            states.append(is_up)
            
        return states

    def recognize_gesture(self, hands_landmarks):
        """ Identifies one of the gestures based on a list of hand landmarks. """
        if not hands_landmarks:
            return "Unknown"
            
        # Two-hand gestures
        if len(hands_landmarks) == 2:
            hand1 = hands_landmarks[0]
            hand2 = hands_landmarks[1]
            
            # Namaste: Wrists are close together
            dist_wrists = math.dist((hand1[self.WRIST]['x'], hand1[self.WRIST]['y']),
                                    (hand2[self.WRIST]['x'], hand2[self.WRIST]['y']))
            if dist_wrists < 0.2:
                # To be strict we should check if palms are facing each other, but wrist distance is a good proxy
                return "Namaste"
                
            # Heart Gesture: Thumb and index of both hands close together
            dist_thumbs = math.dist((hand1[self.THUMB_TIP]['x'], hand1[self.THUMB_TIP]['y']),
                                    (hand2[self.THUMB_TIP]['x'], hand2[self.THUMB_TIP]['y']))
            dist_indexes = math.dist((hand1[self.INDEX_FINGER_TIP]['x'], hand1[self.INDEX_FINGER_TIP]['y']),
                                     (hand2[self.INDEX_FINGER_TIP]['x'], hand2[self.INDEX_FINGER_TIP]['y']))
            if dist_thumbs < 0.1 and dist_indexes < 0.1:
                return "Heart Gesture"
                
            # Fallback to checking the first hand if no two-hand gesture matched
            landmarks = hands_landmarks[0]
        else:
            # Single hand
            landmarks = hands_landmarks[0]
            
        states = self.get_finger_states(landmarks)
        if not states or len(states) != 5:
            return "Unknown"

        thumb, index, middle, ring, pinky = states
        
        # Check for OK (thumb and index tips close to each other, others extended)
        dist_tips = math.dist((landmarks[self.THUMB_TIP]['x'], landmarks[self.THUMB_TIP]['y']), 
                              (landmarks[self.INDEX_FINGER_TIP]['x'], landmarks[self.INDEX_FINGER_TIP]['y']))
                              
        if dist_tips < 0.05:
            if middle and ring and pinky:
                return "OK"
            elif not middle and not ring and not pinky:
                return "Finger Heart"

        if thumb and index and middle and ring and pinky:
            # We'll map Five Fingers to Open Palm (Stop/Wave are contextual, Open Palm is baseline)
            return "Five Fingers"
        elif thumb and index and not middle and not ring and pinky:
            return "Love" # ASL I Love You
        elif not thumb and index and not middle and not ring and not pinky:
            return "One Finger"
        elif not thumb and index and middle and not ring and not pinky:
            return "Peace" # Two Fingers / Victory
        elif not thumb and index and middle and ring and not pinky:
            return "Three Fingers"
        elif not thumb and index and middle and ring and pinky:
            return "Four Fingers"
        elif not thumb and not index and not middle and not ring and not pinky:
            return "Fist"
        elif thumb and not index and not middle and not ring and pinky:
            return "Call Me"
        elif thumb and not index and not middle and not ring and not pinky:
            # Distinguish Thumbs up vs down based on y coordinate (relative to MCP)
            if landmarks[self.THUMB_TIP]['y'] < landmarks[self.THUMB_MCP]['y']:
                return "Thumbs Up"
            else:
                return "Thumbs Down"
        elif thumb and index and not middle and not ring and not pinky:
            # Point Left/Right or Gun
            return "Point Left/Right"
        elif not thumb and index and not middle and not ring and pinky:
            return "Rock"
                
        return "Unknown"
