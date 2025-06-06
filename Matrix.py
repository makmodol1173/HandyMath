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
        self.cooldown_period = 1  # Cooldown after entering matrix mode
        self.matrix_mode_entered_time = None  # Timestamp of entering matrix mode
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

        # Handle initial menu and cooldown
        if self.mode is None:
            self.interface.show_matrix_menu(frame)

            if isinstance(symbol, int) and 0 <= symbol <= 5:
                time_since_last = current_time - self.last_detected_time
                if time_since_last >= self.debounce_interval:
                    if symbol == 1:
                        self.mode = "Dimension"
                        self.matrix_mode_entered_time = current_time
                    elif symbol == 2:
                        self.mode = "Input"
                        self.matrix_mode_entered_time = current_time
                    elif symbol == 3:
                        self.mode = "Select"
                        self.matrix_mode_entered_time = current_time
                    elif symbol == 4:
                        self.mode = "Operation"
                        self.matrix_mode_entered_time = current_time
                    elif symbol == 0:
                        config.mode = None
                        self.mode = None
                    self.last_detected_time = current_time
            return  # Skip drawing matrix submenus until a mode is selected

        # Cooldown check before proceeding inside the selected mode
        if self.matrix_mode_entered_time and current_time - self.matrix_mode_entered_time < self.cooldown_period:
            return

        # Show current mode label
        text = f"Matrix Mode: {self.mode}"
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        x_pos = 50
        y_pos = 100
        cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        if self.mode == "Dimension":
            # -- MATRIX CREATION STEP --
            if self.current_matrix is None and current_time - self.last_detected_time >= self.cooldown_period:
                text = f"Enter Matrix ID(1-9):"
                cv2.putText(frame, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                if isinstance(symbol, int) and 1 <= symbol <= 9:
                    if current_time - self.last_detected_time >= self.debounce_interval:
                        self.current_matrix = symbol
                        self.last_detected_time = current_time

            if self.current_matrix is not None:
                cv2.putText(frame, f"Creating Matrix: M{self.current_matrix}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            if self.current_matrix is not None and self.current_row == 0 and current_time - self.last_detected_time >= self.cooldown_period:
                cv2.putText(frame, f"Enter number of row (1-9):", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                if isinstance(symbol, int) and 1 <= symbol <= 9:
                    if current_time - self.last_detected_time >= self.debounce_interval:
                        self.current_row = symbol
                        self.last_detected_time = current_time

            if self.current_row != 0 and current_time - self.last_detected_time >= self.cooldown_period:
                cv2.putText(frame, f"Selected Row: {self.current_row}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            if self.current_row != 0 and self.current_col == 0:
                cv2.putText(frame, f"Enter number of col (1-9):", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                if isinstance(symbol, int) and 1 <= symbol <= 9:
                    if current_time - self.last_detected_time >= self.debounce_interval:
                        self.current_col = symbol
                        self.last_detected_time = current_time

            if self.current_col != 0 and current_time - self.last_detected_time >= self.cooldown_period:
                cv2.putText(frame, f"Selected Col: {self.current_col}", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            if self.current_matrix and self.current_row and self.current_col:
                self.matrices[self.current_matrix] = np.zeros((self.current_row, self.current_col))
                cv2.putText(frame, f"Matrix M{self.current_matrix} Created: {self.current_row}x{self.current_col}", (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                if current_time - self.last_detected_time >= self.cooldown_period:
                    self.mode = None
                    self.current_matrix = None
                    self.current_row = 0
                    self.current_col = 0

        elif self.mode == "Input":
            print("Input mode selected")
        elif self.mode == "Select":
            if self.current_matrix is None:
                cv2.putText(frame, f"Enter Matrix ID(1-9):", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                if isinstance(symbol, int) and 1 <= symbol <= 9:
                    if current_time - self.last_detected_time >= self.debounce_interval:
                        self.current_matrix = symbol
                        self.last_detected_time = current_time

            if self.current_matrix is not None:
                matrix_str = self.get_matrix_string(self.current_matrix)
                lines = matrix_str.split('\n')
                y_offset = 150
                for i, line in enumerate(lines[:5]):
                    cv2.putText(frame, line, (50, y_offset + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

                cv2.putText(frame, "0. Back", (50, y_offset + 180), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                if isinstance(symbol, int) and symbol == 0:
                    if current_time - self.last_detected_time >= self.debounce_interval:
                        self.current_matrix = None
                        self.mode = None
                        self.last_detected_time = current_time

        elif self.mode == "Operation":
            print("Operation mode selected")

    def get_matrix_string(self, matrix_id):
        if matrix_id in self.matrices:
            m = self.matrices[matrix_id]
            result = f"Matrix {matrix_id} ({m.shape[0]}x{m.shape[1]}):\n"
            for row in m:
                result += " ".join([f"{val:.1f}" for val in row]) + "\n"
            return result
        return f"Matrix {matrix_id} not found"
