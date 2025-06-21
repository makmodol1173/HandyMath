import cv2
import mediapipe as mp

class Detector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=4, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

    def detect_hands(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        landmarks = self.hands.process(frame_rgb)
        return landmarks
    
    def draw_landmarks(self, frame, landmarks):
        if landmarks.multi_hand_landmarks:
            # idx require for detecting which hands from multiple hand
            for idx, hand_landmarks in enumerate(landmarks.multi_hand_landmarks):
               
                # extract the label(left, right) of the hand
                handedness = landmarks.multi_handedness[idx].classification[0].label
               
                # Get the first(wrist) landmark for text positioning
                wrist_x = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].x * frame.shape[1])
                wrist_y = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].y * frame.shape[0])

                # Draw the handedness text
                cv2.putText(frame, handedness, (wrist_x - 20, wrist_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                # Draw the landmarks
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def detect_symbol(self, landmarks):
        FINGER_TIPS = [4, 8, 12, 16, 20]
    
        if landmarks.multi_hand_landmarks and landmarks.multi_handedness:
            for idx, hand_info in enumerate(landmarks.multi_handedness):
                label = hand_info.classification[0].label
                fingers = []
                hand_landmarks = landmarks.multi_hand_landmarks[idx]
    
                if label == "Right":
    
                    # Thumb
                    thumb_up = hand_landmarks.landmark[FINGER_TIPS[0]].x > hand_landmarks.landmark[FINGER_TIPS[0] - 1].x
                    fingers.append(1 if thumb_up else 0)
    
                    # Other fingers
                    for tip in FINGER_TIPS[1:]:
                        fingers.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y else 0)
    
                    # Map to numbers
                    if fingers == [0, 0, 0, 0, 0]: return 0
                    if fingers == [0, 1, 0, 0, 0]: return 1
                    if fingers == [0, 1, 1, 0, 0]: return 2
                    if fingers == [0, 1, 1, 1, 0]: return 3
                    if fingers == [0, 1, 1, 1, 1]: return 4
                    if fingers == [1, 1, 1, 1, 1]: return 5
                    if fingers == [1, 0, 0, 0, 1]: return 6
                    if fingers == [1, 1, 0, 0, 1]: return 7
                    if fingers == [1, 1, 1, 0, 1]: return 8
                    if fingers == [0, 1, 0, 0, 1]: return 9
    
                elif label == "Left":

                    # Thumb
                    thumb_up = hand_landmarks.landmark[FINGER_TIPS[0]].x < hand_landmarks.landmark[FINGER_TIPS[0] - 1].x
                    fingers.append(1 if thumb_up else 0)
    
                    # Other fingers
                    for tip in FINGER_TIPS[1:]:
                        fingers.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y else 0)
    
                    # Map to operators
                    if fingers == [0, 0, 0, 0, 0]: return '='
                    if fingers == [0, 1, 0, 0, 0]: return '+'
                    if fingers == [0, 1, 1, 0, 0]: return '-'
                    if fingers == [0, 1, 1, 1, 0]: return '*'
                    if fingers == [0, 1, 1, 1, 1]: return '/'
                    if fingers == [1, 1, 1, 1, 1]: return '^'
                    if fingers == [1, 0, 0, 0, 1]: return '('
                    if fingers == [1, 1, 0, 0, 1]: return ')'
                    if fingers == [1, 1, 1, 0, 1]: return 'E'
                    if fingers == [0, 1, 0, 0, 1]: return 'X'
    
        return -1

    def detect_thumb(self, landmarks):
        FINGER_TIP = 4
        THUMB_IP = 3
    
        thumbs_up = {"Left": False, "Right": False}
    
        if landmarks.multi_hand_landmarks and landmarks.multi_handedness:
            for idx, hand_info in enumerate(landmarks.multi_handedness):
                label = hand_info.classification[0].label
                hand_landmarks = landmarks.multi_hand_landmarks[idx]
    
                tip = hand_landmarks.landmark[FINGER_TIP]
                ip = hand_landmarks.landmark[THUMB_IP]
    
                if label == "Right":
                    thumbs_up["Right"] = tip.x > ip.x
                elif label == "Left":
                    thumbs_up["Left"] = tip.x < ip.x
    
        return thumbs_up["Right"] and thumbs_up["Left"]


