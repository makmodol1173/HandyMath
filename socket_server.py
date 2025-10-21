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
            data = {"left": [], "right": []}
        
            for hand_landmarks, handedness in zip(landmarks.multi_hand_landmarks, landmarks.multi_handedness):
                hand_label = handedness.classification[0].label.lower()  # "Left" or "Right"
                hand_points = []
                
                for lm in hand_landmarks.landmark:
                    x = int(w - lm.x * w) if hand_label == "right" else int(lm.x * w)
                    y = int(h - lm.y * h)
                    z = int(lm.z * 1000)

                    hand_points.extend([x, y, z])
        
                data[hand_label] = hand_points
        
            packet = {
                "type": "landmarks",
                "landmarkData": data
            }
        
            json_data = json.dumps(packet).encode('utf-8')
            print(packet)
            self.sock.sendto(json_data, self.server_address)
        
        except Exception as e:
            print(f"⚠ Socket send error: {e}")


    def send_symbol(self, symbol):
        try:
            packet = {
                "type": "symbol",
                "symbolData": symbol
            }
            
            json_data = json.dumps(packet).encode('utf-8')
            print(packet)
            self.sock.sendto(json_data, self.server_address)
        
        except Exception as e:
            print(f"⚠ Socket send error: {e}")

    def send_mode(self, mode):
        try:
            packet = {
                "type": "mode",
                "modeData":  mode
            }
            
            json_data = json.dumps(packet).encode('utf-8')
            print(packet)
            self.sock.sendto(json_data, self.server_address)
        
        except Exception as e:
            print(f"⚠ Socket send error: {e}")

    def send_expression(self, expression):
        try:
            packet = {
                "type": "expression",
                "expressionData": expression
            }
            
            json_data = json.dumps(packet).encode('utf-8')
            print(packet)
            self.sock.sendto(json_data, self.server_address)
        
        except Exception as e:
            print(f"⚠ Socket send error: {e}")

    def send_result(self, result):
        try:
            packet = {
                "type": "result",
                "resultData": result
            }
            
            json_data = json.dumps(packet).encode('utf-8')
            print(packet)
            self.sock.sendto(json_data, self.server_address)
        
        except Exception as e:
            print(f"⚠ Socket send error: {e}")

    def close(self):
        self.sock.close()
