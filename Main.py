import cv2
import time
from Detector import Detector
from Calculation import Calculation

class Main:
    expression = ""
    result = ""
    last_detected_time = 0
    debounce_interval = 1.0

    @staticmethod
    def run():
        detector = Detector()
        calculation = Calculation()
        cap = cv2.VideoCapture(0)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        prev_frame_time = time.time()

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print('Ignoring empty camera frame.')
                break

            # Mirror image
            frame = cv2.flip(frame, 1) 
            
            # Calculate FPS
            current_time = time.time()
            fps = 1 / (current_time - prev_frame_time)
            prev_frame_time = current_time

            landmarks = detector.detect_hands(frame)
            frame = detector.draw_landmarks(frame, landmarks)

            symbol = detector.detect_symbol(landmarks)

            if isinstance(symbol, int) and 0 <= symbol <= 9 or symbol in ['=', '+', '-', '*', '/', '^', '(', ')', '#', 'E', 'X']:
                time_since_last = current_time - Main.last_detected_time
                if time_since_last >= Main.debounce_interval:
                    if(symbol != '=' and Main.result == ""):
                        Main.expression += str(symbol)
                    Main.last_detected_time = current_time
                    if(symbol == '='):
                        Main.result = calculation.calculate(Main.expression)
                    elif symbol == 'E':
                        Main.expression = ""
                        Main.result = ""

            # Show FPS
            cv2.putText(frame, f'FPS: {int(fps)}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Show the expression
            if Main.expression != "":
                cv2.putText(frame, f'Expression: {Main.expression}', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Show the result
            if Main.result != "":
                cv2.putText(frame, f'Result: {Main.result}', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('Hand Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    Main.run()