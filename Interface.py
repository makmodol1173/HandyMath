import cv2

class Interface:
    @staticmethod
    def show_main_menu(frame):
        main_menu_options = [
            "Select Your Choice:",
            "1. Arithmetic",
            "2. Matrix",
            "3. Complex",
            "4. Exit"
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
