"""Evaluate arithmetic expressions from input.txt using stacks.

The expression parser converts infix notation to postfix notation with the
shunting-yard algorithm. A second stack then evaluates the postfix tokens.
"""

import math
import re
from typing import List, Union


Number = Union[int, float]


class Stack:
    """A small last-in, first-out stack backed by a Python list."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item, or raise an error if empty."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")
        return self._items[-1]

    def is_empty(self):
        """Return True when the stack contains no items."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self._items)


TOKEN_PATTERN = re.compile(r"\d+(?:\.\d*)?|\.\d+|[()+*/-]")
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "u+": 3, "u-": 3}


def tokenize(expression: str, verbose=False) -> List[str]:
    """Split an expression into numbers and supported operator tokens."""
    tokens = []
    position = 0

    while position < len(expression):
        if expression[position].isspace():
            position += 1
            continue

        match = TOKEN_PATTERN.match(expression, position)
        if match is None:
            character = expression[position]
            raise ValueError(f"Invalid character {character!r} in expression.")

        tokens.append(match.group())
        position = match.end()

    if not tokens:
        raise ValueError("Expression is empty.")
    if verbose:
        print(f"  Tokens: {tokens}")
    return tokens


def to_postfix(tokens: List[str], verbose=False) -> List[str]:
    """Convert infix tokens to postfix tokens using the shunting-yard method."""
    output = []
    operators = Stack()
    expecting_operand = True

    for token in tokens:
        if token[0].isdigit() or token[0] == ".":
            if not expecting_operand:
                raise ValueError("Missing operator between numbers.")
            output.append(token)
            if verbose:
                print(f"    Output append number: {token}")
            expecting_operand = False
        elif token == "(":
            if not expecting_operand:
                raise ValueError("Missing operator before '('.")
            operators.push(token)
            if verbose:
                print(f"    Push '(': stack now {operators._items}")
        elif token == ")":
            if expecting_operand:
                raise ValueError("Missing operand before ')'.")
            while not operators.is_empty() and operators.peek() != "(":
                popped = operators.pop()
                output.append(popped)
                if verbose:
                    print(f"    Pop operator {popped} to output")
            if operators.is_empty():
                raise ValueError("Mismatched parentheses: missing '('.")
            operators.pop()
            if verbose:
                print(f"    Pop '('")
            while not operators.is_empty() and operators.peek() in ("u+", "u-"):
                popped = operators.pop()
                output.append(popped)
                if verbose:
                    print(f"    Pop unary {popped} to output")
            expecting_operand = False
        elif token in ("+", "-", "*", "/"):
            if expecting_operand:
                if token not in ("+", "-"):
                    raise ValueError(f"Operator {token!r} is missing a left operand.")
                operators.push("u" + token)
                if verbose:
                    print(f"    Push unary {token}")
                continue

            while (
                not operators.is_empty()
                and operators.peek() != "("
                and PRECEDENCE[operators.peek()] >= PRECEDENCE[token]
            ):
                popped = operators.pop()
                output.append(popped)
                if verbose:
                    print(f"    Pop operator {popped} to output (precedence)")
            operators.push(token)
            if verbose:
                print(f"    Push operator {token}: stack now {operators._items}")
            expecting_operand = True

    if expecting_operand:
        raise ValueError("Expression ends with an operator or an opening parenthesis.")

    while not operators.is_empty():
        operator = operators.pop()
        if operator == "(":
            raise ValueError("Mismatched parentheses: missing ')'.")
        output.append(operator)
        if verbose:
            print(f"    Pop operator {operator} to output (end)")

    if verbose:
        print(f"  Postfix: {output}")
    return output


def evaluate_postfix(tokens: List[str], verbose=False) -> Number:
    """Evaluate postfix tokens with an operand stack."""
    values = Stack()

    for token in tokens:
        if token[0].isdigit() or token[0] == ".":
            values.push(float(token) if "." in token else int(token))
            if verbose:
                print(f"    Push {token} onto value stack: {values._items}")
        elif token in ("u+", "u-"):
            if values.size() < 1:
                raise ValueError("Unary operator is missing an operand.")
            value = values.pop()
            result = value if token == "u+" else -value
            values.push(result)
            if verbose:
                print(f"    Apply {token} to {value}: push {result} (stack: {values._items})")
        else:
            if values.size() < 2:
                raise ValueError(f"Operator {token!r} is missing an operand.")
            right = values.pop()
            left = values.pop()
            if token == "+":
                result = left + right
            elif token == "-":
                result = left - right
            elif token == "*":
                result = left * right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero.")
                result = left / right
            values.push(result)
            if verbose:
                print(f"    Apply {token} to {left} and {right}: push {result} (stack: {values._items})")

    if values.size() != 1:
        raise ValueError("Malformed expression: extra or missing operands.")

    result = values.pop()
    if isinstance(result, float) and not math.isfinite(result):
        raise ValueError("Result is outside the supported numeric range.")
    if verbose:
        print(f"  Final result: {result}")
    return result


def evaluate_expression(expression: str, verbose=False) -> Number:
    """Parse and evaluate one infix arithmetic expression."""
    tokens = tokenize(expression, verbose=verbose)
    postfix = to_postfix(tokens, verbose=verbose)
    return evaluate_postfix(postfix, verbose=verbose)


def format_result(result: Number) -> str:
    """Format whole-valued floats without an unnecessary decimal suffix."""
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)


def _split_line_ending(line: str):
    """Return a line's body and its original newline sequence."""
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith(("\n", "\r")):
        return line[:-1], line[-1:]
    return line, ""


def process_file(input_path="input.txt", output_path="output.txt", verbose=False):
    """Evaluate each expression line and write a format-matched output file.

    Blank lines remain blank, and lines containing only dashes remain as
    separators. Errors are written for the affected expression only.
    """
    with open(input_path, "r", encoding="utf-8", newline="") as input_file:
        lines = input_file.readlines()

    output_lines = []
    for line in lines:
        body, line_ending = _split_line_ending(line)
        stripped = body.strip()

        if not stripped or re.fullmatch(r"-+", stripped):
            output_lines.append(body + line_ending)
            continue

        try:
            if verbose:
                print(f"\nEvaluating: {stripped}")
            result_value = evaluate_expression(stripped, verbose=verbose)
            result_text = f"{stripped} = {format_result(result_value)}"
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            result_text = f"{stripped} = ERROR: {error}"
            if verbose:
                print(f"  ERROR: {error}")

        output_lines.append(result_text + line_ending)

    with open(output_path, "w", encoding="utf-8", newline="") as output_file:
        output_file.writelines(output_lines)


def main():
    """Run the file-based evaluator using the assignment's default filenames."""
    import sys
    verbose = True
    try:
        process_file(verbose=verbose)
    except OSError as error:
        print(f"File error: {error}")


if __name__ == "__main__":
    main()