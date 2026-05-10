import tkinter as tk

#!/usr/bin/env python3

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Calculator")
        root.resizable(False, False)

        self.expr = ""
        self.display_var = tk.StringVar(value="0")

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        display = tk.Entry(self.root, textvariable=self.display_var, font=("Segoe UI", 24),
                           bd=0, relief=tk.FLAT, justify="right", state="readonly", readonlybackground="white")
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=8, pady=(8,4))

        btn_cfg = {"font": ("Segoe UI", 18), "width":4, "height":2, "bd":0, "relief":tk.RAISED}
        buttons = [
            ("C", 1, 0, self.clear),
            ("⌫", 1, 1, self.backspace),
            ("%", 1, 2, lambda: self.append("%")),
            ("÷", 1, 3, lambda: self.append("÷")),

            ("7", 2, 0, lambda: self.append("7")),
            ("8", 2, 1, lambda: self.append("8")),
            ("9", 2, 2, lambda: self.append("9")),
            ("×", 2, 3, lambda: self.append("×")),

            ("4", 3, 0, lambda: self.append("4")),
            ("5", 3, 1, lambda: self.append("5")),
            ("6", 3, 2, lambda: self.append("6")),
            ("−", 3, 3, lambda: self.append("−")),

            ("1", 4, 0, lambda: self.append("1")),
            ("2", 4, 1, lambda: self.append("2")),
            ("3", 4, 2, lambda: self.append("3")),
            ("+", 4, 3, lambda: self.append("+")),

            ("±", 5, 0, self.negate),
            ("0", 5, 1, lambda: self.append("0")),
            (".", 5, 2, lambda: self.append(".")),
            ("=", 5, 3, self.evaluate),
        ]

        for (text, r, c, cmd) in buttons:
            b = tk.Button(self.root, text=text, command=cmd, **btn_cfg)
            b.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def _bind_keys(self):
        self.root.bind("<Return>", lambda e: self.evaluate())
        self.root.bind("<KP_Enter>", lambda e: self.evaluate())
        self.root.bind("<BackSpace>", lambda e: self.backspace())
        self.root.bind("<Escape>", lambda e: self.clear())
        for key in "0123456789.+-*/()%":
            self.root.bind(key, lambda e, k=key: self.append(k))
        # Map common keyboard symbols to calculator symbols
        self.root.bind("/", lambda e: self.append("÷"))
        self.root.bind("*", lambda e: self.append("×"))
        self.root.bind("-", lambda e: self.append("−"))

    def append(self, ch):
        if self.display_var.get() == "Error":
            self.expr = ""
        # Prevent multiple leading zeros
        if self.expr == "" and ch == "0":
            self.expr = "0"
        else:
            self.expr += ch
        self._update_display(self.expr)

    def clear(self):
        self.expr = ""
        self._update_display("0")

    def backspace(self):
        if self.expr:
            self.expr = self.expr[:-1]
            self._update_display(self.expr if self.expr else "0")

    def negate(self):
        try:
            # Try to evaluate current expression and negate result
            val = self._safe_eval(self._to_python(self.expr))
            val = -val
            self.expr = str(val)
            self._update_display(self.expr)
        except Exception:
            self._update_display("Error")
            self.expr = ""

    def evaluate(self):
        try:
            py_expr = self._to_python(self.expr)
            result = self._safe_eval(py_expr)
            # Strip trailing .0 for integers
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expr = str(result)
            self._update_display(self.expr)
        except Exception:
            self._update_display("Error")
            self.expr = ""

    def _update_display(self, text):
        self.display_var.set(text)

    def _to_python(self, expr):
        # Translate calculator symbols to Python operators
        return expr.replace("×", "*").replace("÷", "/").replace("−", "-").replace("%", "/100")

    def _safe_eval(self, expr):
        # Evaluate arithmetic expressions only
        # No builtins, no names — only literals and operators allowed
        return eval(expr, {"__builtins__": None}, {})

def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()