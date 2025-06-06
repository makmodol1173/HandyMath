import cv2
import time
from Detector import Detector
from Interface import Interface
import config

class Matrix:
    def __init__(self):
        self.mode = None
        self.last_detected_time = 0
        self.debounce_interval = 3
        self.detector = Detector()
        self.interface = Interface()

    def proceed(self, frame, landmarks):
        current_time = time.time()

        text = "Matrix Calculation"
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        x_pos = 50
        y_pos = 50
        cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        if self.mode is None:
            self.interface.show_matrix_menu(frame)
            symbol = self.detector.detect_symbol(landmarks)
            print(f"Detected Symbol: {symbol}")
            if isinstance(symbol, int) and 1 <= symbol <= 5 and self.mode is None:
                time_since_last = current_time - self.last_detected_time
                if time_since_last >= self.debounce_interval:
                    if symbol == 1:
                        self.mode = "Dimension"
                    elif symbol == 2:
                        self.mode = "Input"
                    elif symbol == 3:
                        self.mode = "Select"
                    elif symbol == 4:
                        self.mode = "Operation"
                    elif symbol == 5:
                        config.mode = None
                        self.mode = None
                    self.last_detected_time = current_time
        else:
            text = f"Mode: {self.mode}"
            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            x_pos = 50
            y_pos = 100
            cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        if self.mode == "Dimension":
            print("Dimension mode selected")
        elif self.mode == "Input":
            print("Input mode selected")
        elif self.mode == "Select":
            print("Select mode selected")
        elif self.mode == "Operation":
            print("Operation mode selected")
        
        return