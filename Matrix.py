import cv2
import time
import numpy as np
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
        self.matrices = {}
        self.current_matrix = None
        self.current_row = 0
        self.current_col = 0

    def proceed(self, frame, landmarks):
        current_time = time.time()

        text = "Matrix Calculation"
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        x_pos = 50
        y_pos = 50
        cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        symbol = self.detector.detect_symbol(landmarks)
        print(f"Detected Symbol: {symbol}")

        if self.mode is None:
            self.interface.show_matrix_menu(frame)

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
            text = f"Matrix Mode: {self.mode}"
            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            x_pos = 50
            y_pos = 100
            cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        if self.mode == "Dimension":

            if self.current_matrix is None:
                text = f"Enter Matrix ID(1-9):"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_pos = 50
                y_pos = 150
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                
                if isinstance(symbol, int) and 1 <= symbol <= 9:
                    time_since_last = current_time - self.last_detected_time
                    if time_since_last >= self.debounce_interval:
                        self.current_matrix = symbol
            
            if self.current_matrix is not None:
                text = f"Creating Matrix: M{self.current_matrix}"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_pos = 50
                y_pos = 150
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

            if self.current_matrix is not None and self.current_row == 0:
                text = f"Enter number of row (1-9):"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_pos = 50
                y_pos = 200
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

                if isinstance(symbol, int) and 1 <= symbol <= 9:
                    time_since_last = current_time - self.last_detected_time
                    if time_since_last >= self.debounce_interval:
                        self.current_row = symbol
                            
            if self.current_matrix is not None and self.current_row is not None:
                text = f"Selected Row: {self.current_row}"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_pos = 50
                y_pos = 200
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

            if self.current_matrix is not None and self.current_row != 0 and self.current_col == 0:
                text = f"Enter number of col (1-9):"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_pos = 50
                y_pos = 250
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

                if isinstance(symbol, int) and 1 <= symbol <= 9:
                    time_since_last = current_time - self.last_detected_time
                    if time_since_last >= self.debounce_interval:
                        self.current_col = symbol

            if self.current_matrix is not None and self.current_row != 0 and self.current_col != 0:
                text = f"Selected Col: {self.current_col}"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_pos = 50
                y_pos = 250
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                            
            if self.current_matrix is not None and self.current_row != 0 and self.current_col != 0:
                text = f"Matrix M{self.current_matrix} Created with Dimension: {self.current_row}*{self.current_col}"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_pos = 50
                y_pos = 350
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                self.mode = None

        elif self.mode == "Input":
            print("Input mode selected")
        elif self.mode == "Select":
            print("Select mode selected")
        elif self.mode == "Operation":
            print("Operation mode selected")
        
        return