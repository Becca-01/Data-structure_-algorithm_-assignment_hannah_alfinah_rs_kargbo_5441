# DCOMP320 Assignment Report Outline

**Formatting for the printed report:** Tahoma, 10 pt; 1.15 line spacing; justified alignment. Apply these settings to the report after transferring the outline into a word processor.

## Title Page

- **Assignment:** Stacks Implementation - Mathematical Expression Evaluator
- **Student name:** [Enter student name]
- **Course:** DCOMP320 - Data Structures and Algorithm
- **Institution:** Limkokwing University of Creative Technology, Sierra Leone
- **Submission date:** [Enter submission date]

## 1. Introduction

This assignment implements a Python program that reads arithmetic expressions from `input.txt`, evaluates each expression using stacks, and writes the results to `output.txt`. The supported operations are addition, subtraction, multiplication, and division, along with parentheses and unary signs. The aim is to demonstrate how a stack can support operator precedence and expression evaluation.

## 2. Data Structures Used

### 2.1 Stack

A stack is a linear data structure that follows the last-in, first-out (LIFO) rule: the most recently pushed item is the first item popped. The program's `Stack` class uses a Python list and provides `push`, `pop`, `peek`, `is_empty`, and `size` operations. Push and pop operate at the end of the list, giving constant-time behavior in the usual case.

### 2.2 Use of Stacks in the Evaluator

The evaluator uses an operator stack while converting infix notation to postfix notation. Operators wait on the stack until precedence and parentheses determine when they should be emitted. It then uses an operand stack to evaluate postfix tokens: values are pushed, and an operator pops its operand or operands before pushing the computed value.

### 2.3 Importance in Computing

Stacks are useful whenever the most recent unfinished operation must be handled first. Common examples include function calls and recursion, undo histories, parsing, and expression evaluation. Parentheses naturally nest in last-in, first-out order, making a stack a suitable structure for processing them.

## 3. Program Design

### 3.1 Architecture

The program reads the input file one line at a time, preserves blank lines and separator lines, evaluates each expression independently, and writes the transformed lines to the output file. An invalid expression produces an error message for that line without stopping processing of subsequent expressions.

### 3.2 Key Functions

- `Stack`: provides the stack operations used by conversion and evaluation.
- `tokenize`: recognizes numeric literals, parentheses, and supported operators while ignoring whitespace.
- `to_postfix`: applies the shunting-yard algorithm to enforce precedence, associativity, and parentheses.
- `evaluate_postfix`: calculates the postfix expression using an operand stack and detects division by zero and malformed operands.
- `evaluate_expression`: coordinates tokenization, conversion, and evaluation.
- `process_file`: reads the input, preserves separators and blank lines, handles per-expression errors, and writes the output.
- `main`: runs the default `input.txt` to `output.txt` workflow.

### 3.3 Pseudocode

```text
FOR each line in input file:
    IF line is blank or contains only dashes:
        copy line to output
    ELSE:
        tokenize expression
        convert infix tokens to postfix using operator stack
        evaluate postfix using operand stack
        write result, or an error message if evaluation fails
```

## 4. Testing and Results

### 4.1 Test Approach

The supplied sample checks multiplication precedence, parentheses, division, and subtraction. Additional useful tests include expressions without spaces (`2+3*4`), nested parentheses, unary signs, decimal division (`1 / 2`), blank lines, a trailing separator, mismatched parentheses, malformed input, and division by zero. For invalid input, verify that an error appears on that line and that later expressions are still evaluated.

### 4.2 Sample Results

For the supplied `input.txt`:

| Input expression | Output |
| --- | ---: |
| `3 + 5 * 2` | `3 + 5 * 2 = 13` |
| `(8 / 4) + 7 * 2` | `(8 / 4) + 7 * 2 = 16` |
| `10 - (2 + 3) * 4` | `10 - (2 + 3) * 4 = -10` |

The separator lines in the output remain in the same positions as those in the input. In the second expression, multiplication is performed before addition, yielding $2 + 14 = 16$.

## 5. Conclusion

The program demonstrates stack-based expression processing through infix-to-postfix conversion and postfix evaluation. It preserves the input file's layout and continues after individual expression errors. For submission, push the source code and supporting files to a GitHub repository, then add the lecturer as a collaborator using the repository's access settings.

## 6. References

- DCOMP320 course materials on data structures and stacks, Limkokwing University of Creative Technology.
- Python Software Foundation, *Python 3 Documentation*, https://docs.python.org/3/.
- E. W. Dijkstra, the shunting-yard algorithm for parsing mathematical expressions (as discussed in standard algorithms references).