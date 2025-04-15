import cv2
from Detector import Detector
from Calculation import Calculation

class Main:
    def run():
        detector = Detector()
        calculation = Calculation()
        cap = cv2.VideoCapture(0)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print('Ignoring empty camera frame.')
                break

            frame = cv2.flip(frame, 1)  # Mirror image
            
            landmarks = detector.detect_hands(frame)
            frame = detector.draw_landmarks(frame, landmarks)

            # print(calculation.calculate("100 * ( 2 + 12 ) / 14"))
            
            cv2.imshow('Hand Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    Main.run()