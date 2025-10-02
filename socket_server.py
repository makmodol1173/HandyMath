import socket
import json

class SocketServer:
    def __init__(self, host="127.0.0.1", port=5052):
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_landmarks(self, landmarks, frame_shape):
        if not landmarks or not landmarks.multi_hand_landmarks:
            return

        try:
            h, w, _ = frame_shape
            data = []
            for hand_landmarks in landmarks.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    data.extend([int(lm.x * w), int(h - lm.y * h), int(lm.z * 1000)])
            print(data)
            self.sock.sendto(",".join(map(str, data)).encode(), self.server_address)
        except Exception as e:
            print(f"⚠ Socket send error: {e}")

    def send_arithmetic_result(self, arithmetic):
        try:
            packet = {
                "mode": "Arithmetic",
                "expression": arithmetic.expression,
                "result": arithmetic.result
            }
            self.sock.sendto(json.dumps(packet).encode(), self.server_address)
        except Exception as e:
            print(f"⚠ JSON send error: {e}")

    def close(self):
        self.sock.close()
