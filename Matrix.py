import cv2
import time
import numpy as np
from Detector import Detector
from Interface import Interface
import config

class Matrix:
    def __init__(self):
        self.mode = None
        self.operation_mode = None
        self.detector = Detector()
        self.interface = Interface()
        self.matrices = {}
        self.current_matrix = None
        self.current_row = 0
        self.current_col = 0
        self.operand_matrices = []

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
            if isinstance(symbol, int) and 0 <= symbol <= 4:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    if symbol == 1:
                        self.mode = "Dimension"
                    elif symbol == 2:
                        self.mode = "Input"
                    elif symbol == 3:
                        self.mode = "Select"
                    elif symbol == 4:
                        self.mode = "Operation"
                    elif symbol == 0:
                        self.mode = None
                        config.mode = None
                    config.last_detected_time = current_time

        elif self.mode is not None:
            # Show current mode label
            text = f"Matrix Mode: {self.mode}"
            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            x_pos = 50
            y_pos = 100
            cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        if self.mode == "Dimension":
            self.handle_dimension_mode(frame, symbol)
        elif self.mode == "Input":
            self.handle_input_mode(frame, symbol)
        elif self.mode == "Select":
            self.handle_selection_mode(frame, symbol)
        elif self.mode == "Operation":
            self.handle_operation_mode(frame, symbol)

    def handle_determinant_mode(self, frame, symbol):
        current_time = time.time()
        if self.operand_matrices is None or len(self.operand_matrices) == 0:
            text = "Select Matrix ID(1-9):"
            cv2.putText(frame, text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.current_matrix = symbol
                    self.operand_matrices.append(self.current_matrix)
                    self.current_matrix = None
                    config.last_detected_time = current_time

        elif self.operand_matrices is not None and len(self.operand_matrices) == 1:
            cv2.putText(frame, f"Selected Matrices: M{self.operand_matrices[0]}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            text = f"Result of Deteminant: {np.linalg.det(self.matrices[self.operand_matrices[0]]):.2f}"
            cv2.putText(frame, text, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            # Back menu
            text = "0. Exit"
            cv2.putText(frame, text, (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and symbol == 0:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.operation_mode = None
                    self.current_matrix = None
                    self.operand_matrices.clear()
                    config.last_detected_time = current_time

    def handle_addition(self, frame, symbol):
        current_time = time.time()
        if self.operand_matrices is None or len(self.operand_matrices) == 0:
            text = "Select Matrix ID(1-9):"
            cv2.putText(frame, text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.current_matrix = symbol
                    self.operand_matrices.append(self.current_matrix)
                    self.current_matrix = None
                    config.last_detected_time = current_time

        elif self.operand_matrices is not None and len(self.operand_matrices) == 1:
            cv2.putText(frame, f"Selected Matrices: M{self.operand_matrices[0]}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            text = "Select another Matrix ID(1-9):"
            cv2.putText(frame, text, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.current_matrix = symbol
                    self.operand_matrices.append(self.current_matrix)
                    self.current_matrix = None
                    config.last_detected_time = current_time
        elif self.operand_matrices is not None and len(self.operand_matrices) == 2:
            cv2.putText(frame, f"Selected Matrices: M{self.operand_matrices[1]}", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            m1 = self.matrices[self.operand_matrices[0]]
            m2 = self.matrices[self.operand_matrices[1]]
            if m1.shape == m2.shape:
                result = m1 + m2
                self.matrices["R"] = result
            else:
                print("Matrices must have the same dimensions for addition.")
            self.operand_matrices.clear()
        
        if "R" in self.matrices:
            cv2.putText(frame, "Result of Addition:", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            y_offset = 350
            matrix_str = self.get_matrix_string("R")
            lines = matrix_str.split('\n')
            for i, line in enumerate(lines[:5]):
                cv2.putText(frame, line, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                y_offset += 30        
            
            # Back menu
            text = "0. Exit"
            y_pos = 350 if self.current_matrix is None else y_offset + 70 
            cv2.putText(frame, text, (50, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and symbol == 0:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.operation_mode = None
                    self.current_matrix = None
                    config.last_detected_time = current_time

    def handle_operation_mode(self, frame, symbol):
        if self.operation_mode is None:
            self.interface.show_matrix_operation_menu(frame)
            if isinstance(symbol, int) and 0 <= symbol <= 6:
                if time.time() - config.last_detected_time >= config.debounce_interval:
                    if symbol == 1:
                        self.operation_mode = "Addition"
                    elif symbol == 2:
                        self.operation_mode = "Subtraction"
                    elif symbol == 3:
                        self.operation_mode = "Multiplication"
                    elif symbol == 4:
                        self.operation_mode = "Transpose"
                    elif symbol == 5:
                        self.operation_mode = "Determinant"
                    elif symbol == 6:
                        self.operation_mode = "Inverse"
                    elif symbol == 0:
                        self.operation_mode = None
                        self.mode = None
                    config.last_detected_time = time.time()
        
        elif self.operation_mode is not None:
            # Show current operation mode label
            text = f"Matrix Operation Mode: {self.operation_mode}"
            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            x_pos = 50
            y_pos = 150
            cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        if self.operation_mode == "Addition":
            self.handle_addition(frame, symbol)
            # print("Addition Mode Selected")
        elif self.operation_mode == "Subtraction":
            print("Subtraction Mode Selected")
        elif self.operation_mode == "Multiplication":
            print("Multiplication Mode Selected")
        elif self.operation_mode == "Transpose":
            print("Transpose Mode Selected")
        elif self.operation_mode == "Determinant":
            self.handle_determinant_mode(frame, symbol)
            # print("Determinant Mode Selected")
        elif self.operation_mode == "Inverse":
            print("Inverse Mode Selected")

    def handle_input_mode(self, frame, symbol):
        current_time = time.time()
        # Handle matrix selection
        if self.current_matrix is None:
            text = "Select Matrix ID(1-9):"
            cv2.putText(frame, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.current_matrix = symbol
                    config.last_detected_time = current_time
        
        # Displaying selected matrix id
        if self.current_matrix is not None:
            cv2.putText(frame, f"Selected Matrix: M{self.current_matrix}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Show matrix content if selected
        y_offset = 200
        if self.current_matrix is not None and self.current_matrix in self.matrices:
            matrix_str = self.get_matrix_string(self.current_matrix)
            lines = matrix_str.split('\n')
            for i, line in enumerate(lines[:5]):
                cv2.putText(frame, line, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                y_offset += 30        

        # Getting input
        if self.current_matrix is not None and self.current_matrix in self.matrices:
            if isinstance(symbol, int) and 0 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    matrix = self.matrices[self.current_matrix]
                    if self.current_row < matrix.shape[0] and self.current_col < matrix.shape[1]:
                        matrix[self.current_row, self.current_col] = symbol
                        
                        # Move to next position
                        self.current_col += 1
                        if self.current_col >= matrix.shape[1]:
                            self.current_col = 0
                            self.current_row += 1
                        config.last_detected_time = current_time
        
        # Back menu
        text = "0. Exit"
        y_pos = 200 if self.current_matrix is None else y_offset + 70 
        cv2.putText(frame, text, (50, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        if isinstance(symbol, int) and symbol == 0:
            if current_time - config.last_detected_time >= config.debounce_interval:
                self.mode = None
                self.current_matrix = None
                config.last_detected_time = current_time

    def handle_selection_mode(self, frame, symbol):
        current_time = time.time()
        # Handle matrix selection
        if self.current_matrix is None:
            text = "Select Matrix ID(1-9):"
            cv2.putText(frame, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.current_matrix = symbol
                    config.last_detected_time = current_time
        
        # Displaying selected matrix id
        elif self.current_matrix is not None:
            cv2.putText(frame, f"Selected Matrix: M{self.current_matrix}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Show matrix content if selected
        y_offset = 200
        if self.current_matrix is not None and self.current_matrix in self.matrices:
            matrix_str = self.get_matrix_string(self.current_matrix)
            lines = matrix_str.split('\n')
            for i, line in enumerate(lines[:5]):
                cv2.putText(frame, line, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                y_offset += 30

        # Back menu
        text = "0. Exit"
        y_pos = 200 if self.current_matrix is None else y_offset + 20 
        cv2.putText(frame, text, (50, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        if isinstance(symbol, int) and symbol == 0:
            if current_time - config.last_detected_time >= config.debounce_interval:
                self.mode = None
                self.current_matrix = None
                config.last_detected_time = current_time

    def handle_dimension_mode(self, frame, symbol):
        current_time = time.time()
        # Handle matrix id input
        if self.current_matrix is None:
            text = f"Enter Matrix ID(1-9):"
            cv2.putText(frame, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.current_matrix = symbol
                    config.last_detected_time = current_time
        
        # Displaying current matrix id
        elif self.current_matrix is not None:
            cv2.putText(frame, f"Creating Matrix: M{self.current_matrix}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Handle row input
        if self.current_matrix is not None and self.current_row == 0:
                cv2.putText(frame, f"Enter number of row (1-9):", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                if isinstance(symbol, int) and 1 <= symbol <= 9:
                    if current_time - config.last_detected_time >= config.debounce_interval:
                        self.current_row = symbol
                        config.last_detected_time = current_time
        # Displaying current row
        elif self.current_matrix is not None and self.current_row != 0:
            cv2.putText(frame, f"Selected Row: {self.current_row}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Handle column input
        if self.current_matrix is not None and self.current_row != 0 and self.current_col == 0:
            cv2.putText(frame, f"Enter number of column (1-9):", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.current_col = symbol
                    config.last_detected_time = current_time
        # Displaying current column
        elif self.current_matrix is not None and self.current_row != 0 and self.current_col != 0:
            cv2.putText(frame, f"Selected Column: {self.current_col}", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Create matrix if dimensions are set
        if self.current_matrix is not None and self.current_row != 0 and self.current_col != 0:
            if self.current_matrix not in self.matrices:
                self.matrices[self.current_matrix] = np.zeros((self.current_row, self.current_col), dtype=float)
            cv2.putText(frame, f"Matrix M{self.current_matrix} created with dimensions {self.current_row}x{self.current_col}", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Reset mode after matrix creation
            if current_time - config.last_detected_time >= config.debounce_interval:
                self.mode = None
                self.current_matrix = None
                self.current_row = 0
                self.current_col = 0

    def get_matrix_string(self, matrix_id):
        if matrix_id in self.matrices:
            m = self.matrices[matrix_id]
            result = f"Matrix {matrix_id} ({m.shape[0]}x{m.shape[1]}):\n"
            for row in m:
                result += " ".join([f"{val:.1f}" for val in row]) + "\n"
            return result
        return f"Matrix {matrix_id} not found"
