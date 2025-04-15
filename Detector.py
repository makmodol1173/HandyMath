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