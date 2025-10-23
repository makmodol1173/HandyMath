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
            "modeData": None,
            "subModeData": None,
            "expressionData": None,
            "resultData": None,
            "matrixData": None
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

    def send_matrix(self, matrixData, key):
        data = ["", "", "", "", "", "", "", "", "", ""]
        data[key] = matrixData
        self.state["type"] = "matrix"
        self.state["matrixData"] = data
        self.send_state()

    def send_symbol(self, symbol):
        self.state["type"] = "symbol"
        self.state["symbolData"] = symbol
        self.send_state()

    def send_mode(self, mode):
        self.state["type"] = "mode"
        self.state["modeData"] = mode
        self.send_state()

    def send_submode(self, subMode):
        self.state["type"] = "subMode"
        self.state["subModeData"] = subMode
        self.send_state()

    def send_expression(self, expression):
        self.state["type"] = "expression"
        self.state["expressionData"] = expression
        self.send_state()

    def send_result(self, result):
        self.state["type"] = "result"
        self.state["resultData"] = result
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
