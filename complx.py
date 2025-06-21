import cv2
import time
from detector import Detector
import config

class Complex:
    def __init__(self):
        self.detector = Detector()

    def proceed(self, frame, landmarks):
        current_time = time.time()
        symbol = self.detector.detect_symbol(landmarks)
        print(f"Detected Symbol: {symbol}")

        text = "Complex Calculation\n(Coming Soon)"
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        x_pos = 50
        y_pos = 50
        cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        # Back menu
        text = "0. Exit"
        cv2.putText(frame, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        if isinstance(symbol, int) and symbol == 0:
            if current_time - config.last_detected_time >= config.debounce_interval:
                config.mode = None
                config.last_detected_time = current_time