import socket
import json

class SocketServer:
    def __init__(self, host="127.0.0.1", port=5052):
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.state = {
            "type": None,
            "landmarkData": {"left": [], "right": []},
            "symbolData": None,
            "boardData": None
        }

    def send_landmarks(self, landmarks, frame_shape):
        if not landmarks or not landmarks.multi_hand_landmarks:
            return
    
        try:
            h, w, _ = frame_shape
            data = {"left": [], "right": []}
    
            for hand_landmarks, handedness in zip(landmarks.multi_hand_landmarks, landmarks.multi_handedness):
                hand_label = handedness.classification[0].label.lower()
                hand_points = []
    
                for lm in hand_landmarks.landmark:
                    x = int(w - lm.x * w) if hand_label == "right" else int(lm.x * w)
                    y = int(h - lm.y * h)
                    z = int(lm.z * 1000)
                    hand_points.extend([x, y, z])
    
                data[hand_label] = hand_points
    
            self.state["type"] = "landmarks"
            self.state["landmarkData"] = data
            self.send_state()
    
        except Exception as e:
            print(f"⚠ Socket send error: {e}")

    def send_board_data(self, boardData):
        self.state["type"] = "board"
        self.state["boardData"] = boardData
        self.send_state()

    def send_symbol(self, symbol):
        self.state["type"] = "symbol"
        self.state["symbolData"] = symbol
        self.send_state()


    def send_state(self):
        try:
            json_data = json.dumps(self.state).encode("utf-8")
            print("Sent state:", self.state)
            self.sock.sendto(json_data, self.server_address)
        except Exception as e:
            print(f"⚠ Socket send error: {e}")

    def close(self):
        self.sock.close()
