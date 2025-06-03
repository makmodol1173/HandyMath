import cv2
import time
from Detector import Detector
from Calculation import Calculation
from Interface import Interface

class Main:

    @staticmethod
    def run():
        # Initialize components
        detector = Detector()
        calculation = Calculation()
        interface = Interface()
        cap = cv2.VideoCapture(0)

        # Set webcam width and height
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Initial State
        prev_frame_time = time.time()
        is_activated = False
        mode = None
        last_detected_time = 0
        debounce_interval = 0.5

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print('Ignoring empty camera frame.')
                break

            # Mirror image
            frame = cv2.flip(frame, 1) 

            # Detect hands and draw landmarks
            landmarks = detector.detect_hands(frame)
            frame = detector.draw_landmarks(frame, landmarks)

            if not is_activated:
                # Show Welcome Message
                text = "Welcome to HandyMath"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_pos = (frame.shape[1] - text_width) // 2
                y_pos = 50
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                # Activation Detection via two thumbs
                is_activated = detector.detect_thumb(landmarks)
            else:
                # Calculate and show FPS
                current_time = time.time()
                fps = 1 / (current_time - prev_frame_time)
                prev_frame_time = current_time
    
                fps_int = int(fps)
                text = f'FPS: {fps_int:02}'
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_pos = frame.shape[1] - text_width - 170
                y_pos = 50
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

                interface.show_main_menu(frame)
                # Main menu selection
                symbol = detector.detect_symbol(landmarks)
                print(f"Detected Symbol: {symbol}")
                if isinstance(symbol, int) and 1 <= symbol <= 4 and mode is None:
                    time_since_last = current_time - last_detected_time
                    last_detected_time = current_time
                    if time_since_last >= debounce_interval:
                        if symbol == 1:
                            mode = "Arithmetic"
                        elif symbol == 2:
                            mode = "Matrix"
                        elif symbol == 3:
                            mode = "Complex"
                        elif symbol == 4:
                            is_activated = False
                            mode = None

            if is_activated and mode is not None:
                text = f"{mode} Mode Activated"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_pos = 50
                y_pos = 50
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow('HandyMath', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    Main.run()