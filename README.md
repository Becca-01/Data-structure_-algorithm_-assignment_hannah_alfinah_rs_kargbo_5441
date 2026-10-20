# Stack Expression Evaluator

Course assignment: DCOMP320 - Data Structures and Algorithm, Stacks Implementation, Limkokwing University of Creative Technology, Sierra Leone.

## Requirements

- Python 3.8 or later
- No third-party packages

## Run

Place `input.txt` in the same folder as `stack_evaluator.py`, then run:

```text
python stack_evaluator.py
```

The program reads `input.txt` and creates or replaces `output.txt` in that folder.

## Input and output format

Put one expression on each line. A line containing only dashes is a separator; its exact dash text is copied to the output. Blank lines are also preserved. The output has the same line layout, with each expression shown as `expression = result` or `expression = ERROR: message`. A trailing separator and the original line endings are preserved.

For example:

```text
3 + 5 * 2
-----
(8 / 4) + 7 * 2
-----
10 - (2 + 3) * 4
```

produces:

```text
3 + 5 * 2 = 13
-----
(8 / 4) + 7 * 2 = 16
-----
10 - (2 + 3) * 4 = -10
```

## Design and assumptions

- `Stack` implements `push`, `pop`, `peek`, `is_empty`, and `size` with a Python list.
- The shunting-yard algorithm converts infix expressions to postfix notation. A second stack evaluates the postfix tokens.
- Supported binary operators are `+`, `-`, `*`, and `/`, with normal precedence and left-to-right associativity. Parentheses and unary `+`/`-` are supported.
- Integer literals remain integers for exact addition, subtraction, and multiplication. Division uses Python floating-point division; whole-valued results are printed without `.0`.
- Decimal literals are supported, but scientific notation, implicit multiplication (such as `2(3)`), and operators other than the listed ones are not.
- Each nonblank, non-separator line is processed independently. Invalid expressions, mismatched parentheses, and division by zero produce a clear error on that line; processing continues.
- A separator is any nonempty line made only of dashes. A line consisting of a single negative number is an expression, not a separator.

## Report outline

See [REPORT_OUTLINE.md](REPORT_OUTLINE.md) for a ready-to-complete printed-report outline and formatting requirements.