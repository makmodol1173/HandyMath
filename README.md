# HandyMath

HandyMath is a computer‐vision “gesture calculator” that lets you draw numbers and operators in the air and computes the result in real time. Everything runs on your webcam feed with an FPS counter and overlays for the current expression and result.

[Preview](https://drive.google.com/file/d/1aLH89HAaP0Nm-2BDtQwHrY3lzPPLD85L/view?usp=sharing)

## Requirements

[Install Python on Your Device](https://www.python.org/downloads/)

## How to run

```bash
# Clone the repository
git clone https://github.com/makmodol1173/HandyMath.git
cd HandyMath

# Install required module
pip install -r requirements.txt

# Run the app
python main.py
```

## Features

- **Arithmetic Equation Solver** (supports +, -, \*, /, ^, parentheses)
- **Matrix Solver** (Add, Subtract, Multiply, Transpose, Determinant, Inverse)
- **Hand Gesture Input** (dual-hand support)
- **Voice Feedback** for better accessibility

## Gesture Controls

### Hand Gesture Reference

<table>
  <tr>
    <td><img src="./images/0.jpg" width="100px" height="100px"/><br/>0</td>
    <td><img src="./images/1.jpg" width="100px" height="100px"/><br/>1</td>
    <td><img src="./images/2.jpg" width="100px" height="100px"/><br/>2</td>
    <td><img src="./images/3.jpg" width="100px" height="100px"/><br/>3</td>
    <td><img src="./images/4.jpg" width="100px" height="100px"/><br/>4</td>
  </tr>
  <tr>
    <td><img src="./images/5.jpg" width="100px" height="100px"/><br/>5</td>
    <td><img src="./images/6.jpg" width="100px" height="100px"/><br/>6</td>
    <td><img src="./images/7.jpg" width="100px" height="100px"/><br/>7</td>
    <td><img src="./images/8.jpg" width="100px" height="100px"/><br/>8</td>
    <td><img src="./images/9.jpg" width="100px" height="100px"/><br/>9</td>
  </tr>
</table>

### Right Hand — **Number Input**

| Index | Decription            | Symbol |
| ----- | --------------------- | ------ |
| `0`   | All fingers closed    | `0`    |
| `1`   | Index finger          | `1`    |
| `2`   | Index + Middle        | `2`    |
| `3`   | Index + Middle + Ring | `3`    |
| `4`   | Four fingers          | `4`    |
| `5`   | All fingers open      | `5`    |
| `6`   | Thumb + Pinky         | `6`    |
| `7`   | Thumb + Two fingers   | `7`    |
| `8`   | Three fingers + Thumb | `8`    |
| `9`   | Index + Pinky         | `9`    |

### Left Hand — **Operators**

| Index | Decription            | Symbol |
| ----- | --------------------- | ------ |
| `0`   | All fingers closed    | `=`    |
| `1`   | Index finger          | `+`    |
| `2`   | Index + Middle        | `-`    |
| `3`   | Index + Middle + Ring | `*`    |
| `4`   | Four fingers          | `/`    |
| `5`   | All fingers open      | `^`    |
| `6`   | Thumb + Pinky         | `(`    |
| `7`   | Thumb + Two fingers   | `)`    |
| `8`   | Three fingers + Thumb | `E`    |
| `9`   | Index + Pinky         | `X`    |

- `E` represent `Backspace`
- `X` represent `Clear All`

## Workflow

### Main

### Arithmetic

#### Features

1. Gesture-Driven Input:

   - Detects digits (0–9) and operators (+, -, \*, /, (, )) using hand gestures.
   - Supports special gestures:
     - `=` → Evaluate expression
     - `E` → Backspace (delete last character)
     - `X` → Clear expression/result
     - `0` (after result shown) → Exit back

2. Arithmetic Expression Evaluator:

   - Operator precedence (+, -, \*, /)
   - Parentheses for grouping
   - Reject division by zero and mismatched parentheses

3. Visual Feedback with OpenCV:
   - Renders current expression and result on screen
   - Prompts user with "Proceed any numeric gesture" if empty
   - Prompts exit instruction after evaluation

#### Execution Flow

1. Class Initialization

   - Initializes two stacks: operands and operators
   - Initializes detector for gesture recognition
   - Stores the current expression and result

2. Process the frame with landmarks:

   - Render title text: “Arithmetic Calculation”
   - Detect a symbol from hand landmarks
   - If symbol is valid and debounce interval passed:
     - = → Evaluate expression using calculate()
     - E → Backspace
     - X → Clear
     - 0 → Exit mode if result shown
     - Otherwise append digit/operator to expression
   - Expression is being typed and shown real-time
   - Result shown if available
   - Exit command

3. Calculating Expression

   - The arithmetic expression is parsed and evaluated manually using two stacks.
   - Uses regex to reject expressions with illegal characters
   - Handles empty or malformed strings
   - Parsing Loop iterates over characters:
     - (`digit`) → parse full number
     - `(` → push to operator stack
     - `)` → evaluate stack until matching `(`
     - operators → handle precedence (pop previous ops if needed)
     - unary minus → detected when `-` follows operator or `(`
   - Uses apply_operation() to compute binary operations
   - Ensures proper precedence
   - Handles division-by-zero safely
   - Returns result (rounded to 5 decimal places) or error message

4. Applying Operation

   - Pops two operands and one operator from the stacks, performs the operation
   - Checks for division-by-zero
   - Returns computed result

5. Precedence is uded to detemine evaluation order.

#### Algorithmic Flow

The evaluator is a classic 2-stack infix parser, inspired by the Shunting Yard Algorithm by Edsger Dijkstra.

- Loop through each character:
  - If number → push to operand stack
  - If operator:
    - While top of operator stack has higher/equal precedence → pop & apply
    - Push current operator
  - If `(` → push
  - If `)` → pop & apply until `(`
- After loop → evaluate remaining operators

Stacks:

- Operand Stack: stores numbers (int)
- Operator Stack: stores operators (+, -, etc.)

### Marix

### Complex

## Contribution

### Arithmatic

1. handle floating point precision
2. handle railing or leading operators ("+2" or "3\*" or "-2+5" or "(-2+0)")
3. handle associativity of operators (e.g., exponentiation is right-associative: 2 ** 3 ** 2 = 512)
4. handle power(`^`) calculation
