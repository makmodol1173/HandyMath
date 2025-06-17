import cv2

class Interface:
    @staticmethod
    def show_main_menu(frame):
        main_menu_options = [
            "Select Your Choice:",
            "1. Arithmetic",
            "2. Matrix",
            "3. Complex",
            "0. Exit"
        ]

        # Determine the width of the longest line to right-align all menu options
        text_sizes = [cv2.getTextSize(option, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0] for option in main_menu_options]
        max_width = max([w for (w, h) in text_sizes])
        x_pos = frame.shape[1] - max_width - 50  # 50 pixels padding from right edge
        y_start = 100  # Starting Y position
        line_height = 40  # Space between lines

        for i, option in enumerate(main_menu_options):
            y_pos = y_start + i * line_height
            cv2.putText(frame, option, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    @staticmethod
    def show_matrix_menu(frame):
        matrix_menu_options = [
            "Select Your Choice:",
            "1. Dimension",
            "2. Input",
            "3. Select",
            "4. Operation",
            "0. Exit"
        ]
        
        # Determine the width of the longest line to right-align all menu options
        text_sizes = [cv2.getTextSize(option, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0] for option in matrix_menu_options]
        max_width = max([w for (w, h) in text_sizes])
        x_pos = 50
        y_start = 100  # Starting Y position
        line_height = 40  # Space between lines

        for i, option in enumerate(matrix_menu_options):
            y_pos = y_start + i * line_height
            cv2.putText(frame, option, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    
    @staticmethod
    def show_matrix_operation_menu(frame):
        matrix_operation_menu_options = [
            "Select Your Choice:",
            "1. Addition",
            "2. Subtraction",
            "3. Multiplication",
            "4. Transponse",
            "5. Determinant",
            "6. Inverse",
            "0. Exit"
        ]
        # Determine the width of the longest line to right-align all menu options
        text_sizes = [cv2.getTextSize(option, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0] for option in matrix_operation_menu_options]
        max_width = max([w for (w, h) in text_sizes])
        x_pos = 50
        y_start = 150  # Starting Y position
        line_height = 40  # Space between lines
        for i, option in enumerate(matrix_operation_menu_options):
            y_pos = y_start + i * line_height
            cv2.putText(frame, option, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)