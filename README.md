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

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
# source venv/bin/activate

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

| Index | Decription                    | Symbol |
| ----- | ----------------------------- | ------ |
| `0`   | All fingers closed            | `0`    |
| `1`   | Index finger                  | `1`    |
| `2`   | Index + Middle                | `2`    |
| `3`   | Index + Middle + Ring         | `3`    |
| `4`   | Index + Middle + Ring + Pinky | `4`    |
| `5`   | All fingers open              | `5`    |
| `6`   | Thumb + Pinky                 | `6`    |
| `7`   | Thumb + Index + Pinky         | `7`    |
| `8`   | Thumb + Index + Middle + Pinky| `8`    |
| `9`   | Index + Pinky                 | `9`    |

### Left Hand — **Operators**

| Index | Decription                    | Symbol |
| ----- | ----------------------------- | ------ |
| `0`   | All fingers closed            | `=`    |
| `1`   | Index finger                  | `+`    |
| `2`   | Index + Middle                | `-`    |
| `3`   | Index + Middle + Ring         | `*`    |
| `4`   | Index + Middle + Ring + Pinky | `/`    |
| `5`   | All fingers open              | `^`    |
| `6`   | Thumb + Pinky                 | `(`    |
| `7`   | Thumb + Index + Pinky         | `)`    |
| `8`   | Thumb + Index + Middle + Pinky| `E`    |
| `9`   | Index + Pinky                 | `X`    |

- `E` represent `Backspace`
- `X` represent `Clear All`

## Workflow

### Detector

1. **Initialization:**

   - Uses MediaPipe’s real-time hand tracking pipeline.
   - Configured for up to 4 hands (`max_num_hands=4`), real-time tracking.
   - Initializes drawing utility (`mp.solutions.drawing_utils`) for visual output.
   - Defines landmark indices for finger tips (`[4, 8, 12, 16, 20]`).

2. **Hand Detection:**

   - Converts each frame to RGB (MediaPipe uses RGB).
   - Passes the frame through the model to detect hand landmarks.
   - Returns a `results` object with:
     - `multi_hand_landmarks`: list of hand landmarks
     - `multi_handedness`: list of `Left` / `Right` classifications

3. **Draw Landmarks:**

   - Draws hand skeleton and hand label (Left or Right) on the image.
   - For each detected hand:
     - Gets WRIST landmark to position the label text.
     - Draws 21 landmarks and connections using drawing_utils.

4. **Detect Symbol:**

   This is the gesture recognition engine.

   - Checks each detected hand and identifies:
     - Which fingers are extended (1) or folded (0).
     - Distinguishes between Left and Right hands.
   - Constructs a binary finger pattern like [0, 1, 0, 0, 1].

   Based on the pattern and hand type:

   - Right hand → Mapped to digits `0–9`
   - Left hand → Mapped to operators: `+`, `-`, `\*`, `/`, `^`, `=`, `(`, `)`, `E`, `X`
   - Uses Python dictionaries for fast lookup and clear mapping logic.
   - If the gesture doesn't match a known pattern → returns `-1`.

5. **Thumbs Up Detection:**
   - Detects activation gesture:
   - Both thumbs must be up:
     - Right thumb is considered `up` if tip is to the right of the joint.
     - Left thumb is considered `up` if tip is to the left of the joint.
   - Returns `True` only when both thumbs are up.
   - Used to activate the main interface/menu of the system.

### Main

1. **Webcam Initialization:**

   - Opens a video stream.
   - Sets resolution and prepares the frame capture loop.

2. **Hand Detection & Landmark Tracking:**

   - Process each frame and extract hand landmarks.
   - Landmarks are visualized in real-time on the frame for feedback.

3. **Activation Trigger:**

   - System starts in an idle state showing a welcome message.
   - Activation occurs via a specific gesture (e.g., double thumbs up), after which the system enters interaction mode.

4. **Main Menu Navigation (Gesture-Driven):**

   - `1` → Arithmetic Mode
   - `2` → Matrix Mode
   - `3` → Complex Mode
   - `0` → Deactivate and return to idle state

5. **Visual Feedback:**

   - Displays current mode and frame rate (FPS) on screen.

6. **Debounce and Cooldown Handling:**

   - Ensures that gestures are not registered multiple times too quickly.
   - Prevents mode switching or symbol detection until a safe interval has passed.

7. **Exit Condition:**

   - Pressing the 'q' key gracefully exits the program.
   - Releases webcam resources and closes all OpenCV windows.

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
   - Prompts user with Proceed any numeric gesture" if empty
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

#### Featues

1.  Gesture-Driven Input:

    - Uses hand landmarks to detect digits (0–9) via a `Detector` class.
    - Controls all matrix actions through gestures:
      - 0–4 → Mode selection (Dimension, Input, Select, Operation, Exit)
      - 0–9 → Input matrix IDs, values, dimensions, etc.
      - 0 (within modes) → Return to main menu

2.  Matrix Management:

    - Create matrices with custom dimensions.
    - Fill matrices using gesture-based number input.
    - View matrix contents.
    - Supports storing multiple matrices (`M1`, `M2`, ..., `M9`).

3.  Matrix Operations:

    - Binary Operations: Addition, Subtraction, Multiplication
    - Unary Operations: Transpos, Inverse (only for square and non-singular matrices), Determinant (only for square matrices)

4.  Visual Feedback with OpenCV:

    - Real-time frame rendering using `cv2.putText()`.
    - Prompts user for inputs, shows selected matrices.
    - Renders matrix values in structured format.
    - Shows result matrices inline with labels.

#### Control Flow

1. Class Initialization

   - Initializes detector for gesture recognition
   - Initializes interface for menus
   - Initializes state variables

2. Process the frame with landmarks:

   - Display “Matrix Calculation” header.
   - Detect gesture using `detector.detect_symbol()`.
   - If no mode selected:
     - Show mode selection menu.
     - Wait for valid gesture (1–4).
   - If mode is selected:
     - Display mode label.
     - Dispatch control to respective handler: `handle_dimension_mode`, `handle_input_mode`, `handle_selection_mode`, `handle_operation_mode`

3. Dimension Mode

   - Prompt user to input matrix ID (1–9).
   - Prompt number of rows (1–9).
   - Prompt number of columns (1–9).
   - Initialize matrix with `np.zeros((row, col))`.
   - Confirm matrix creation and return to main menu.

4. Input Mode
   - Select matrix ID (must already exist).
   - Display current matrix visually.
   - Fill values one-by-one using digit gestures (0–9).
   - Automatically proceeds cell-wise row by row.
   - Mark as complete after filling all cells.
5. Selection Mode

   - Choose existing matrix by ID.
   - Display matrix visually.
   - Return to main menu with gesture `0`.

6. Operation Mode
   - 1 → Addition
   - 2 → Subtraction
   - 3 → Multiplication
   - 4 → Transpose
   - 5 → Determinant
   - 6 → Inverse
   - 0 → Exit

#### Matrix Operation Logic

**Binary Operation Flow (+, -, \*):**

- Prompt user to select two matrix IDs.
- Check compatibility:
  - Add/Sub: shapes must match
  - Multiply: inner dimensions must match
- Perform operation using NumPy:
  - `+`, `-`: element-wise
  - `*`: matrix multiplication via `np.matmul()`
- Store result in `self.matrices["R"]`
- Display result visually

**Unary Operation Flow (Transpose, Inverse, Determinant) :**

- Prompt user to select one matrix ID.
- For Transpose:
  - Use `.T`
- For Inverse:
  - Check if matrix is square and non-singular
  - Use `np.linalg.inv()`
- For Deteminant:
  - Validate square matrix
  - use `np.linalg.det()`
- Display result matrix

### Complex

$$
Upcoming...
$$

## Contribution

1. Thumbs-Up Gesture Detection
2. Reduce code size
   - Make a common function for `putText`, Matrix Selection etc
   - Immediate if converted to `and` operator
3. Audio feedback for symbol detection and menu showing

### Arithmatic

1. Floating-Point Precision Handling
2. Support for Unary and Partial Operators (`+2` or `3\*` or `-2+5` or `(-2+0)`)
3. Operator Associativity and Precedence (e.g., exponentiation is right-associative: `2 ** 3 ** 2 = 512`)
4. Exponentiation(`^`) Support

### Matrix

1. Multi-Digit Gesture Input
2. Matrix Cursor Navigation
3. Matrix data type should be Integer
