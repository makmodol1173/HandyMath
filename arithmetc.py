import cv2
import time
import config
from detector import Detector

class Arithmetic:

    def __init__(self):
        self.operators = []
        self.operands = []
        self.expression = ""
        self.result = ""
        self.detector = Detector()

    def precedence(self, operator):
        if operator == '+' or operator == '-':
            return 1
        if operator == '*' or operator == '/':
            return 2
        return 0
    
    def apply_operation(self):
        if len(self.operators) == 0:
            return "Invalid Expression"

        if len(self.operands) < 2:
            self.operators.pop()
            return "Invalid Expression"
    
        right = self.operands.pop()
        left = self.operands.pop()
        op = self.operators.pop()

        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right if right != 0 else float('inf')
    
    def calculate(self, expression):
        self.operators = []
        self.operands = []
        i = 0
        while i < len(expression):
            if expression[i] == ' ':
                i += 1
                continue
            if expression[i] == '(':
                self.operators.append(expression[i])
            elif expression[i] == ')':
                while len(self.operators) > 0 and self.operators[-1] != '(':
                    result = self.apply_operation()
                    if result is not None:
                        self.operands.append(result)
                self.operators.pop()
            elif expression[i].isdigit():
                num = 0
                while (i < len(expression) and expression[i].isdigit()):
                    num = (num * 10) + int(expression[i])
                    i += 1
                self.operands.append(num)
                continue
            else:
                while (len(self.operators) > 0 and self.precedence(self.operators[-1]) >= self.precedence(expression[i])):
                    result = self.apply_operation()
                    if result is not None:
                        self.operands.append(result)
                self.operators.append(expression[i])
            i += 1
        
        while len(self.operators) > 0:
            result = self.apply_operation()
            if result is not None:
                self.operands.append(result)
        
        return self.operands[-1] if len(self.operands) > 0 else None
    
    def proceed(self, frame, landmarks):
        current_time = time.time()

        text = "Arithmetic Calculation"
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        x_pos = 50
        y_pos = 50
        cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        symbol = self.detector.detect_symbol(landmarks)
        print(f"Detected Symbol: {symbol}")

        if (isinstance(symbol, int) and 0 <= symbol <= 9) or symbol in ['=', '+', '-', '*', '/', '^', '(', ')', 'E', 'X'] and self.result=="":
            if current_time - config.last_detected_time >= config.debounce_interval:
                if symbol == '=':
                    self.result = str(self.calculate(self.expression))
                elif symbol == 'E':
                    self.expression = self.expression[:-1]
                elif symbol == 'X':
                    self.expression = ""
                    self.result = ""
                elif symbol == 0 and self.result != "":
                    self.expression = ""
                    self.result = ""
                    config.mode = None
                else:
                    if self.result == "":
                        self.expression += str(symbol)
                config.last_detected_time = current_time
        
        if self.expression == "":
            text = "Proceed any numeric gesture"
            x_pos = 50
            y_pos = 100
            cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        if self.expression != "":
            text = f"Expression: {self.expression}"
            x_pos = 50
            y_pos = 100
            cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        if self.result != "":
            text = f"Result: {self.result}"
            x_pos = 50
            y_pos = 150
            cv2.putText(frame, text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # Back menu
            text = "0. Exit"
            cv2.putText(frame, text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
