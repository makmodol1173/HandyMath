import cv2
import mediapipe as mp

class Detector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=4, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

    def detect_hands(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.hands.process(frame_rgb)
    
    def draw_landmarks(self, frame, results):
        if results.multi_hand_landmarks:
            # idx require for detecting which hands from multiple hand
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
               
                # extract the label(left, right) of the hand
                label = results.multi_handedness[idx].classification[0].label
               
                # Get the first(wrist) landmark for text positioning
                wrist_x = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].x * frame.shape[1])
                wrist_y = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].y * frame.shape[0])

                # Draw the handedness text
                cv2.putText(frame, label, (wrist_x - 20, wrist_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                # Draw the landmarks
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def detect_symbol(self, results):
        if not (results.multi_hand_landmarks and results.multi_handedness):
            return -1

        FINGER_TIPS = [4, 8, 12, 16, 20]
    
        for idx, hand_info in enumerate(results.multi_handedness):
            label = hand_info.classification[0].label
            hand_landmarks = results.multi_hand_landmarks[idx]
    
            thumb = hand_landmarks.landmark[FINGER_TIPS[0]].x > hand_landmarks.landmark[FINGER_TIPS[0] - 1].x if label == "Right" else hand_landmarks.landmark[FINGER_TIPS[0]].x < hand_landmarks.landmark[FINGER_TIPS[0] - 1].x
            fingers = [1 if thumb else 0]
            fingers += [1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y else 0 for tip in FINGER_TIPS[1:]]

            if label == "Right":
                return {
                    (0, 0, 0, 0, 0): 0, 
                    (0, 1, 0, 0, 0): 1, 
                    (0, 1, 1, 0, 0): 2,
                    (0, 1, 1, 1, 0): 3, 
                    (0, 1, 1, 1, 1): 4, 
                    (1, 1, 1, 1, 1): 5,
                    (1, 0, 0, 0, 1): 6, 
                    (1, 1, 0, 0, 1): 7, 
                    (1, 1, 1, 0, 1): 8,
                    (0, 1, 0, 0, 1): 9
                }.get(tuple(fingers), -1)

            if label == "Left":
                return {
                    (0, 0, 0, 0, 0): '=', 
                    (0, 1, 0, 0, 0): '+', 
                    (0, 1, 1, 0, 0): '-',
                    (0, 1, 1, 1, 0): '*', 
                    (0, 1, 1, 1, 1): '/', 
                    (1, 1, 1, 1, 1): '^',
                    (1, 0, 0, 0, 1): '(', 
                    (1, 1, 0, 0, 1): ')', 
                    (1, 1, 1, 0, 1): 'E',
                    (0, 1, 0, 0, 1): 'X'
                }.get(tuple(fingers), -1)
    
        return -1

    def detect_thumb(self, results):
        if not (results.multi_hand_landmarks and results.multi_handedness):
            return False

        FINGER_TIP = 4
        THUMB_IP = 3
        thumbs = {"Left": False, "Right": False}
    
        for idx, hand_info in enumerate(results.multi_handedness):
            label = hand_info.classification[0].label
            hand_landmarks = results.multi_hand_landmarks[idx]
    
            tip = hand_landmarks.landmark[FINGER_TIP]
            ip = hand_landmarks.landmark[THUMB_IP]
    
            thumbs[label] = tip.x > ip.x if label == "Right" else tip.x < ip.x
    
        return thumbs["Right"] and thumbs["Left"]