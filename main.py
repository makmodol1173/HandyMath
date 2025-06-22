import cv2
import time
from detector import Detector
from arithmetic import Arithmetic
from matrix import Matrix
from complex import Complex
from interface import Interface
import config

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
       print("Camera access error.")
       return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    detector = Detector()
    interface = Interface()
    handlers = {
        "Arithmetic": Arithmetic().proceed,
        "Matrix": Matrix().proceed,
        "Complex": Complex().proceed,
    }

    prev_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Empty frame.")
                continue

            frame = cv2.flip(frame, 1)
            landmarks = detector.detect_hands(frame)
            frame = detector.draw_landmarks(frame, landmarks)

            if not config.is_activated:
                cv2.putText(frame, "Welcome to HandyMath", (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                if detector.detect_thumb(landmarks):
                    config.is_activated = True
                    config.last_detected_time = time.time()
            else:
                fps = int(1 / (time.time() - prev_time))
                text = f'FPS: {fps:02}'
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_pos = frame.shape[1] - text_width - 170
                y_pos = 50
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                prev_time = time.time()

            if config.mode is None and config.is_activated:
                interface.show_main_menu(frame)
                symbol = detector.detect_symbol(landmarks)
                print(f"Detected Symbol: {symbol}")
                if isinstance(symbol, int) and 0 <= symbol <= 3:
                    if time.time() - config.last_detected_time >= config.debounce_interval:
                        config.mode = [None, "Arithmetic", "Matrix", "Complex"][symbol]
                        config.is_activated = symbol != 0
                        config.last_detected_time = time.time()

            elif config.mode is not None and config.is_activated:
                text = f"Mode: {config.mode}"
                text_sizes = [cv2.getTextSize(option, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0] for option in ["Arithmetic", "Matrix", "Complex"]]
                max_width = max([w for (w, h) in text_sizes])
                x_pos = frame.shape[1] - max_width - 170
                y_pos = 100
                cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

            if handler := handlers.get(config.mode):
                handler(frame, landmarks)

            cv2.imshow('HandyMath', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as exception:
        print(f"Error: {exception}")
    finally:            
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()