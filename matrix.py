import cv2
import time
import numpy as np
from detector import Detector
from interface import Interface
from socket_server import SocketServer
import config

class Matrix:
    def __init__(self, board_data):
        self.mode = None
        self.operation_mode = None
        self.detector = Detector()
        self.interface = Interface()
        self.matrices = {}
        self.current_matrix = None
        self.current_row = 0
        self.current_col = 0
        self.operand_matrices = []
        self.matrix_input_completed = False
        self.socket_server = SocketServer()
        self.board_data = board_data
        self.matrix_menu_options = [
            "Select Your Choice: ",
            "1. Dimension       ",
            "2. Input           ",
            "3. Select          ",
            "4. Operation       ",
            "0. Exit            "
        ]
        self.matrix_operation_menu_options = [
            "Select Your Choice:",
            "1. Addition",
            "2. Subtraction",
            "3. Multiplication",
            "4. Transponse",
            "5. Determinant",
            "6. Inverse",
            "0. Exit"
        ]

    def validate_square(self, matrix):
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Matrix must be square.")

    def safe_inverse(self, matrix):
        self.validate_square(matrix)
        det = np.linalg.det(matrix)
        if np.isclose(det, 0):
            raise np.linalg.LinAlgError("Matrix is singular and cannot be inverted.")
        return np.linalg.inv(matrix)
        
    def proceed(self, frame, landmarks):
        current_time = time.time()

        text = "Matrix Calculation"
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        x_pos = 50
        y_pos = 50
        cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        symbol = self.detector.detect_symbol(landmarks)
        if(symbol != -1):
            print(f"Detected Symbol: {symbol}")

        # Handle initial menu and cooldown
        if self.mode is None:
            self.interface.show_matrix_menu(frame, self.matrix_menu_options)
            for i in range(0, 8):
                if i < len(self.matrix_menu_options):
                    self.board_data[i] = self.matrix_menu_options[i]
                else:
                    self.board_data[i] = ""
            if isinstance(symbol, int) and 0 <= symbol <= 4:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.mode = [None, "Dimension", "Input", "Select", "Operation"][symbol]
                    if symbol == 0:
                        config.mode = None
                    config.last_detected_time = current_time

        elif self.mode is not None:
            # Show current mode label
            text = f"Matrix Mode: {self.mode}"
            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            x_pos = 50
            y_pos = 100
            self.board_data[0] = text
            for i in range(1, 8):
                self.board_data[i] = ""
            cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        handlers = {
            "Dimension": self.handle_dimension_mode,
            "Input": self.handle_input_mode,
            "Select": self.handle_selection_mode,
            "Operation": self.handle_operation_mode
        }
        if self.mode in handlers:
            handlers[self.mode](frame, symbol)

        self.socket_server.send_board_data(self.board_data)

    def handle_determinant_mode(self, frame, symbol):
        current_time = time.time()
        exit_pos = 250

        if len(self.operand_matrices) == 0:
            text = "Select Matrix ID(1-9):"
            cv2.putText(frame, text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    if symbol in self.matrices:
                        self.operand_matrices.append(symbol)
                        config.last_detected_time = current_time
                    else:
                        exit_pos = 300
                        cv2.putText(frame, f"Selected Matrices: M{symbol} not found", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        elif len(self.operand_matrices) == 1:
            cv2.putText(frame, f"Selected Matrices: M{self.operand_matrices[0]}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            try:
                self.validate_square(self.matrices[self.operand_matrices[0]])
                det = np.linalg.det(self.matrices[self.operand_matrices[0]])
                text = f"Result of Deteminant: {np.linalg.det(self.matrices[self.operand_matrices[0]]):.2f}"
                cv2.putText(frame, text, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                exit_pos = 300
            except ValueError as exception:
                exit_pos = 300
                cv2.putText(frame, f"{exception}", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Back menu
        text = "0. Exit"
        y_pos = exit_pos
        cv2.putText(frame, text, (50, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        if isinstance(symbol, int) and symbol == 0:
            if current_time - config.last_detected_time >= config.debounce_interval:
                self.operation_mode = None
                self.current_matrix = None
                self.current_row = 0
                self.current_col = 0
                self.operand_matrices.clear()
                config.last_detected_time = current_time

    def handle_unary_operation(self, frame, symbol, operator):
        current_time = time.time()
        exit_pos = 250
        if len(self.operand_matrices) == 0:
            text = "Select Matrix ID(1-9):"
            cv2.putText(frame, text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    if symbol in self.matrices:
                        self.operand_matrices.append(symbol)
                        config.last_detected_time = current_time
                    else:
                        exit_pos = 300
                        cv2.putText(frame, f"Selected Matrices: M{symbol} not found", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        elif len(self.operand_matrices) == 1:
            cv2.putText(frame, f"Selected Matrices: M{self.operand_matrices[0]}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            try:
                matrix = self.matrices[self.operand_matrices[0]]
                self.matrices["R"] = self.safe_inverse(matrix) if operator == "INV" else matrix.T
            except (ValueError, np.linalg.LinAlgError) as exception:
                exit_pos = 300
                cv2.putText(frame, f"{exception}", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        if "R" in self.matrices:
            cv2.putText(frame, f"Result of {"Inverse" if operator == "INV" else "Transponse"} :", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            y_offset = 300
            matrix_str = self.get_matrix_string("R")
            lines = matrix_str.split('\n')
            for i, line in enumerate(lines):
                cv2.putText(frame, line, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                y_offset += 30 
            exit_pos = y_offset + 20
            
        # Back menu
        text = "0. Exit"
        y_pos = exit_pos
        cv2.putText(frame, text, (50, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        if isinstance(symbol, int) and symbol == 0:
            if current_time - config.last_detected_time >= config.debounce_interval:
                self.operation_mode = None
                self.current_matrix = None
                self.current_row = 0
                self.current_col = 0
                if "R" in self.matrices:
                    del self.matrices["R"]
                self.operand_matrices.clear()
                config.last_detected_time = current_time
            
    def handle_binary_operation(self, frame, symbol, operator):
        current_time = time.time()
        exit_pos = 250
        if len(self.operand_matrices) == 0:
            text = "Select Matrix ID(1-9):"
            cv2.putText(frame, text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    if symbol in self.matrices:
                        self.operand_matrices.append(symbol)
                        config.last_detected_time = current_time
                    else:
                        exit_pos = 300
                        cv2.putText(frame, f"Selected Matrices: M{symbol} not found", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        elif len(self.operand_matrices) == 1:
            exit_pos = exit_pos + 50
            text = "Select another Matrix ID(1-9):"
            cv2.putText(frame, text, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    if symbol in self.matrices:
                        self.operand_matrices.append(symbol)
                        config.last_detected_time = current_time
                    else:
                        exit_pos = 350
                        cv2.putText(frame, f"Selected Matrices: M{symbol} not found", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        elif len(self.operand_matrices) == 2:
            m1 = self.matrices[self.operand_matrices[0]]
            m2 = self.matrices[self.operand_matrices[1]]
            try:
                if (operator in ["+", "-"] and m1.shape != m2.shape) or (operator == "*" and m1.shape[1] != m2.shape[0]):
                    raise ValueError("Shape mismatch")
                self.matrices["R"] = m1 + m2 if operator == "+" else m1 - m2 if operator == "-" else np.matmul(m1, m2)
            except ValueError as exception:
                exit_pos = 350
                cv2.putText(frame, f"{exception}", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        if len(self.operand_matrices) >= 1:
            cv2.putText(frame, f"Selected Matrices: M{self.operand_matrices[0]}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        if len(self.operand_matrices) >= 2:
            cv2.putText(frame, f"Selected Matrices: M{self.operand_matrices[1]}", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        if "R" in self.matrices:
            cv2.putText(frame, "Result of Addition:", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            y_offset = 350
            matrix_str = self.get_matrix_string("R")
            lines = matrix_str.split('\n')
            for i, line in enumerate(lines):
                cv2.putText(frame, line, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                y_offset += 30
            exit_pos = y_offset + 20        
            
        # Back menu
        text = "0. Exit"
        y_pos = exit_pos
        cv2.putText(frame, text, (50, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        if isinstance(symbol, int) and symbol == 0:
            if current_time - config.last_detected_time >= config.debounce_interval:
                self.operation_mode = None
                self.current_matrix = None
                self.current_row = 0
                self.current_col = 0
                if "R" in self.matrices:
                    del self.matrices["R"]
                self.operand_matrices.clear()
                config.last_detected_time = current_time

    def handle_operation_mode(self, frame, symbol):
        if self.operation_mode is None:
            self.interface.show_matrix_operation_menu(frame, self.matrix_operation_menu_options)
            for i in range(len(self.board_data)):
                if i < len(self.matrix_operation_menu_options):
                    self.board_data[i] = self.matrix_operation_menu_options[i]
                else:
                    self.board_data[i] = ""

            if isinstance(symbol, int) and 0 <= symbol <= 6:
                if time.time() - config.last_detected_time >= config.debounce_interval:
                    self.operation_mode = [None, "Addition", "Subtraction", "Multiplication", "Transpose", "Determinant", "Inverse"][symbol]
                    if symbol == 0:
                        self.mode = None
                    config.last_detected_time = time.time()
        
        else:
            # Show current operation mode label
            text = f"Operation Mode: {self.operation_mode}"
            x_pos = 50
            y_pos = 150
            cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            self.board_data[1] = text

        operations = {
            "Addition": lambda: self.handle_binary_operation(frame, symbol, "+"),
            "Subtraction": lambda: self.handle_binary_operation(frame, symbol, "-"),
            "Multiplication": lambda: self.handle_binary_operation(frame, symbol, "*"),
            "Transpose": lambda: self.handle_unary_operation(frame, symbol, "TRN"),
            "Inverse": lambda: self.handle_unary_operation(frame, symbol, "INV"),
            "Determinant": lambda: self.handle_determinant_mode(frame, symbol)
        }

        if self.operation_mode in operations:
            operations[self.operation_mode]()

    def handle_input_mode(self, frame, symbol):
        current_time = time.time()
        exit_pos = 200
        # Handle matrix selection
        if self.current_matrix is None:
            text = "Select Matrix ID(1-9):"
            cv2.putText(frame, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            self.board_data[1] = text

            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    if symbol in self.matrices:
                        self.current_matrix = symbol
                        config.last_detected_time = current_time
                    else:
                        exit_pos = 250
                        text = f"Selected Matrices: M{symbol} not found"
                        cv2.putText(frame, text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        self.board_data[1] = text

        # Displaying selected matrix id
        if self.current_matrix is not None:
            text = f"Selected Matrix: M{self.current_matrix}"
            cv2.putText(frame, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            self.board_data[1] = text

        # Show matrix content if selected
        y_offset = 200
        last_item = 2
        if self.current_matrix is not None and self.current_matrix in self.matrices:
            matrix_str = self.get_matrix_string(self.current_matrix)
            lines = matrix_str.split('\n')
            for i, line in enumerate(lines):
                cv2.putText(frame, line, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                y_offset += 30      
                self.board_data[i] = line

        # Getting input
        if self.current_matrix is not None and self.current_matrix in self.matrices:
            if isinstance(symbol, int) and 0 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    matrix = self.matrices[self.current_matrix]
                    if self.current_row < matrix.shape[0] and self.current_col < matrix.shape[1]:
                        matrix[self.current_row, self.current_col] = symbol
                        config.last_detected_time = current_time
                        
                        # Move to next position
                        self.current_col += 1
                        if self.current_col >= matrix.shape[1]:
                            self.current_col = 0
                            self.current_row += 1
                        if self.current_row >= matrix.shape[0]:
                            self.matrix_input_completed = True
            
        if self.matrix_input_completed:
            text = f"Matrix M{self.current_matrix} input completed"
            cv2.putText(frame, text, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            self.board_data[last_item] = text
            last_item = last_item + 1
            if current_time - config.last_detected_time >= config.debounce_interval:
                self.mode = None
                self.current_matrix = None
                self.current_row = 0
                self.current_col = 0
                self.matrix_input_completed = False

        if self.current_matrix is None:
            # Back menu
            text = "0. Exit"
            y_pos = exit_pos
            cv2.putText(frame, text, (50, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            self.board_data[last_item] = text
            if isinstance(symbol, int) and symbol == 0:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.mode = None
                    self.current_matrix = None
                    self.current_row = 0
                    self.current_col = 0
                    config.last_detected_time = current_time
                    for i in range(0, last_item):
                        self.board_data[i] = ""

    def handle_selection_mode(self, frame, symbol):
        current_time = time.time()
        exit_pos = 200
        # Handle matrix selection
        if self.current_matrix is None:
            text = "Select Matrix ID(1-9):"
            cv2.putText(frame, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            self.board_data[1] = text

            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    if symbol in self.matrices:
                        self.current_matrix = symbol
                        config.last_detected_time = current_time
                    else:
                        exit_pos = 250
                        text = f"Selected Matrices: M{symbol} not found"
                        cv2.putText(frame, text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        self.board_data[1] = text

        # Displaying selected matrix id
        elif self.current_matrix is not None and self.current_matrix in self.matrices:
            text = f"Selected Matrix: M{self.current_matrix}"
            cv2.putText(frame, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            self.board_data[1] = text

        # Show matrix content if selected
        y_offset = 200
        last_item = 2
        if self.current_matrix is not None and self.current_matrix in self.matrices:
            matrix_str = self.get_matrix_string(self.current_matrix)
            lines = matrix_str.split('\n')
            for i, line in enumerate(lines, start = 2):
                cv2.putText(frame, line, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                y_offset += 30
                self.board_data[i] = line
                last_item = i
            exit_pos = y_offset + 20

        # Back menu
        text = "0. Exit"
        y_pos = exit_pos
        cv2.putText(frame, text, (50, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        self.board_data[last_item] = text
        if isinstance(symbol, int) and symbol == 0:
            if current_time - config.last_detected_time >= config.debounce_interval:
                self.mode = None
                self.current_matrix = None
                self.current_row = 0
                self.current_col = 0 
                config.last_detected_time = current_time
                for i in range(0, last_item):
                    self.board_data[i] = ""

    def handle_dimension_mode(self, frame, symbol):
        current_time = time.time()
        # Handle matrix id input
        if self.current_matrix is None:
            text = f"Enter Matrix ID(1-9):"
            self.board_data[1] = text
            cv2.putText(frame, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.current_matrix = symbol
                    config.last_detected_time = current_time
        
        # Displaying current matrix
        elif self.current_matrix is not None:
            text = f"Created Matrix: M{self.current_matrix}"
            self.board_data[1] = text
            cv2.putText(frame, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Handle row input
        if self.current_matrix is not None and self.current_row == 0:
            text = f"Enter number of row (1-9):"
            self.board_data[2] = text
            cv2.putText(frame, text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.current_row = symbol
                    config.last_detected_time = current_time

        # Displaying current row
        elif self.current_matrix is not None and self.current_row != 0:
            text = f"Selected Row: {self.current_row}"
            cv2.putText(frame, text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            self.board_data[2] = text

        # Handle column input
        if self.current_matrix is not None and self.current_row != 0 and self.current_col == 0:
            text = f"Enter number of column (1-9):"
            cv2.putText(frame, text, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            self.board_data[3] = text
            if isinstance(symbol, int) and 1 <= symbol <= 9:
                if current_time - config.last_detected_time >= config.debounce_interval:
                    self.current_col = symbol
                    config.last_detected_time = current_time
        # Displaying current column
        elif self.current_matrix is not None and self.current_row != 0 and self.current_col != 0:
            text = f"Selected Column: {self.current_col}"
            cv2.putText(frame, text, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            self.board_data[3] = text

        # Create matrix if dimensions are set
        if self.current_matrix is not None and self.current_row != 0 and self.current_col != 0:
            if self.current_matrix not in self.matrices:
                self.matrices[self.current_matrix] = np.zeros((self.current_row, self.current_col))
            text = f"Matrix M{self.current_matrix} created with dimensions {self.current_row}x{self.current_col}"
            cv2.putText(frame, text, (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            self.board_data[4] = text

            # Reset mode after matrix creation
            if current_time - config.last_detected_time >= config.debounce_interval:
                self.mode = None
                self.current_matrix = None
                self.current_row = 0
                self.current_col = 0
                self.board_data[0] = ""
                self.board_data[1] = ""
                self.board_data[2] = ""
                self.board_data[3] = ""

    def get_matrix_string(self, matrix_id):
        if matrix_id in self.matrices:
            m = self.matrices[matrix_id]
            result = f"Matrix {matrix_id} ({m.shape[0]}x{m.shape[1]}):\n"
            for row in m:
                result += " ".join([f"{val:.1f}" for val in row]) + "\n"
            return result
        return f"Matrix {matrix_id} not found"
