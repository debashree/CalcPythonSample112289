"""Basic desktop calculator built with Python's standard library."""

from __future__ import annotations

import ast
import operator
import tkinter as tk
from tkinter import messagebox


class CalculatorError(ValueError):
    """Raised when an expression cannot be evaluated safely."""


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression: str) -> float | int:
    """Evaluate a basic arithmetic expression without using eval()."""
    expression = expression.strip()
    if not expression:
        raise CalculatorError("Enter an expression first.")

    try:
        tree = ast.parse(expression, mode="eval")
        return _evaluate(tree.body)
    except (SyntaxError, TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        if isinstance(exc, CalculatorError):
            raise
        raise CalculatorError("Use numbers and +, -, *, /, %, or ** only.") from exc


def _evaluate(node: ast.AST) -> float | int:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.operand))

    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        return _OPERATORS[type(node.op)](left, right)

    raise CalculatorError("Only basic arithmetic expressions are supported.")


class CalculatorApp:
    """Tkinter user interface for the calculator."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Basic Calculator")
        self.root.resizable(False, False)
        self.expression = tk.StringVar()

        display = tk.Entry(
            root,
            textvariable=self.expression,
            font=("Segoe UI", 22),
            justify="right",
            width=16,
            relief="solid",
            bd=1,
        )
        display.grid(row=0, column=0, columnspan=4, padx=12, pady=(12, 8), ipady=8)
        display.focus_set()
        display.bind("<Return>", lambda _event: self.evaluate())
        display.bind("<Escape>", lambda _event: self.clear())

        buttons = [
            ("C", 1, 0, self.clear), ("⌫", 1, 1, self.backspace),
            ("(", 1, 2, lambda: self.insert("(")), (" )", 1, 3, lambda: self.insert(")")),
            ("7", 2, 0, lambda: self.insert("7")), ("8", 2, 1, lambda: self.insert("8")),
            ("9", 2, 2, lambda: self.insert("9")), ("/", 2, 3, lambda: self.insert("/")),
            ("4", 3, 0, lambda: self.insert("4")), ("5", 3, 1, lambda: self.insert("5")),
            ("6", 3, 2, lambda: self.insert("6")), ("*", 3, 3, lambda: self.insert("*")),
            ("1", 4, 0, lambda: self.insert("1")), ("2", 4, 1, lambda: self.insert("2")),
            ("3", 4, 2, lambda: self.insert("3")), ("-", 4, 3, lambda: self.insert("-")),
            ("0", 5, 0, lambda: self.insert("0")), (".", 5, 1, lambda: self.insert(".")),
            ("%", 5, 2, lambda: self.insert("%")), ("+", 5, 3, lambda: self.insert("+")),
        ]
        for label, row, column, command in buttons:
            tk.Button(root, text=label, command=command, font=("Segoe UI", 14), width=4, height=2).grid(
                row=row, column=column, padx=4, pady=4
            )

        tk.Button(root, text="=", command=self.evaluate, font=("Segoe UI", 14, "bold"), width=21, height=2,
                  bg="#2563eb", fg="white", activebackground="#1d4ed8").grid(
            row=6, column=0, columnspan=4, padx=8, pady=(4, 12)
        )

    def insert(self, value: str) -> None:
        self.expression.set(self.expression.get() + value)

    def clear(self) -> None:
        self.expression.set("")

    def backspace(self) -> None:
        self.expression.set(self.expression.get()[:-1])

    def evaluate(self) -> None:
        try:
            result = calculate(self.expression.get())
            self.expression.set(str(result))
        except CalculatorError as exc:
            messagebox.showerror("Calculator", str(exc))


def main() -> None:
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
