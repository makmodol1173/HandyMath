import cv2
import time
from detector import Detector
import config
from socket_server import SocketServer

class Complex:
    def __init__(self, board_data):
        self.detector = Detector()
        self.socket_server = SocketServer()
        self.board_data = board_data

    def proceed(self, frame, landmarks):
        for i in range(0, 9):
            self.board_data[i] = ""

        current_time = time.time()
        symbol = self.detector.detect_symbol(landmarks)
        if(symbol != -1):
            print(f"Detected Symbol: {symbol}")

        text = "Complex Calculation\n(Coming Soon)"
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        x_pos = 50
        y_pos = 50
        self.board_data[0] = text.split("\n")[0]
        self.board_data[1] = text.split("\n")[1]
        cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        # Back menu
        text = "0. Exit"
        cv2.putText(frame, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        if isinstance(symbol, int) and symbol == 0:
            if current_time - config.last_detected_time >= config.debounce_interval:
                config.mode = None
                self.board_data[9] = config.mode
                config.last_detected_time = current_time
        
        self.socket_server.send_board_data(self.board_data)