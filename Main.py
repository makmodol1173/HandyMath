import cv2
import time
from Detector import Detector
from Arithmetic import Arithmetic
from Matrix import Matrix
from Complex import Complex
from Interface import Interface
import config

class Main:

    def run():
        # Initialize components
        detector = Detector()
        arithmetic = Arithmetic()
        matrix = Matrix()
        complex = Complex()
        interface = Interface()
        cap = cv2.VideoCapture(0)

        # Set webcam width and height
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Initial State
        prev_frame_time = time.time()

        while cap.isOpened():
            # Capture frame
            success, frame = cap.read()
            if not success:
                print('Ignoring empty camera frame.')
                break

            # Mirror image
            frame = cv2.flip(frame, 1) 

            # Detect hands and draw landmarks
            landmarks = detector.detect_hands(frame)
            frame = detector.draw_landmarks(frame, landmarks)

            current_time = time.time()

            # Show Welcome Message
            if not config.is_activated:
                text = "Welcome to HandyMath"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_pos = (frame.shape[1] - text_width) // 2
                y_pos = 50
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                # Activation Detection via two thumbs
                if detector.detect_thumb(landmarks):
                    config.is_activated = True
                    config.last_detected_time = current_time

            elif config.is_activated:
                # Calculate and show FPS
                fps = 1 / (current_time - prev_frame_time)
                prev_frame_time = current_time

                if current_time - config.last_detected_time >= config.cooldown_period:
                    fps_int = int(fps)
                    text = f'FPS: {fps_int:02}'
                    (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                    x_pos = frame.shape[1] - text_width - 170
                    y_pos = 50
                    cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

            if config.mode is None and config.is_activated:
                # Wait for cooldown after activation before showing menu
                if current_time - config.last_detected_time >= config.cooldown_period:
                    interface.show_main_menu(frame)
                    # Main menu selection
                    symbol = detector.detect_symbol(landmarks)
                    print(f"Detected Symbol: {symbol}")
                    if isinstance(symbol, int) and 0 <= symbol <= 3:
                        if current_time - config.last_detected_time >= config.debounce_interval:
                            if symbol == 1:
                                config.mode = "Arithmetic"
                            elif symbol == 2:
                                config.mode = "Matrix"
                            elif symbol == 3:
                                config.mode = "Complex"
                            elif symbol == 0:
                                config.is_activated = False
                                config.mode = None
                            config.last_detected_time = current_time

            elif config.mode is not None and config.is_activated:
                text = f"Mode: {config.mode}"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_pos = frame.shape[1] - text_width - 30
                y_pos = 100
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

            # Proceed with selected mode after cooldown
            if config.mode == "Arithmetic":
                arithmetic.proceed(frame, landmarks)
            elif config.mode == "Matrix":
                matrix.proceed(frame, landmarks)
            elif config.mode == "Complex":
                complex.proceed(frame, landmarks)

            cv2.imshow('HandyMath', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    Main.run()
