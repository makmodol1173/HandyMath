# EXPLORE IT
class Calculation:
    def __init__(self):
        self.operators = []
        self.operands = []

    def precedence(self, operator):
        if operator == '+' or operator == '-':
            return 1
        if operator == '*' or operator == '/':
            return 2
        return 0
    
    def apply_operation(self):
        if len(self.operators) == 0 or len(self.operands) == 0:
            return None
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