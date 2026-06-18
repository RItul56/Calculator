import tkinter as tk

# ---------- Colors & Fonts ----------
BG_COLOR = "#1e1e2e"
DISPLAY_BG = "#181825"
DISPLAY_FG = "#ffffff"
NUM_BTN_BG = "#313244"
NUM_BTN_FG = "#ffffff"
OP_BTN_BG = "#89b4fa"
OP_BTN_FG = "#1e1e2e"
EQUAL_BTN_BG = "#a6e3a1"
EQUAL_BTN_FG = "#1e1e2e"
CLEAR_BTN_BG = "#f38ba8"
CLEAR_BTN_FG = "#1e1e2e"

FONT_DISPLAY = ("Helvetica", 32, "bold")
FONT_BTN = ("Helvetica", 18)


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("360x520")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)

        self.expression = ""
        self._build_display()
        self._build_buttons()
        self._bind_keys()

    # ---------- Display ----------
    def _build_display(self):
        self.display_var = tk.StringVar(value="0")
        display = tk.Label(
            self,
            textvariable=self.display_var,
            anchor="e",
            bg=DISPLAY_BG,
            fg=DISPLAY_FG,
            font=FONT_DISPLAY,
            padx=20,
            pady=30,
        )
        display.pack(fill="both", expand=False)

    # ---------- Buttons ----------
    def _build_buttons(self):
        frame = tk.Frame(self, bg=BG_COLOR)
        frame.pack(fill="both", expand=True)

        for i in range(6):
            frame.rowconfigure(i, weight=1)
        for i in range(4):
            frame.columnconfigure(i, weight=1)

        buttons = [
            ("C", 0, 0, CLEAR_BTN_BG, CLEAR_BTN_FG), ("←", 0, 1, CLEAR_BTN_BG, CLEAR_BTN_FG),
            ("%", 0, 2, OP_BTN_BG, OP_BTN_FG), ("÷", 0, 3, OP_BTN_BG, OP_BTN_FG),

            ("7", 1, 0, NUM_BTN_BG, NUM_BTN_FG), ("8", 1, 1, NUM_BTN_BG, NUM_BTN_FG),
            ("9", 1, 2, NUM_BTN_BG, NUM_BTN_FG), ("×", 1, 3, OP_BTN_BG, OP_BTN_FG),

            ("4", 2, 0, NUM_BTN_BG, NUM_BTN_FG), ("5", 2, 1, NUM_BTN_BG, NUM_BTN_FG),
            ("6", 2, 2, NUM_BTN_BG, NUM_BTN_FG), ("-", 2, 3, OP_BTN_BG, OP_BTN_FG),

            ("1", 3, 0, NUM_BTN_BG, NUM_BTN_FG), ("2", 3, 1, NUM_BTN_BG, NUM_BTN_FG),
            ("3", 3, 2, NUM_BTN_BG, NUM_BTN_FG), ("+", 3, 3, OP_BTN_BG, OP_BTN_FG),

            ("±", 4, 0, NUM_BTN_BG, NUM_BTN_FG), ("0", 4, 1, NUM_BTN_BG, NUM_BTN_FG),
            (".", 4, 2, NUM_BTN_BG, NUM_BTN_FG), ("=", 4, 3, EQUAL_BTN_BG, EQUAL_BTN_FG),
        ]

        for (text, row, col, bg, fg) in buttons:
            btn = tk.Button(
                frame,
                text=text,
                font=FONT_BTN,
                bg=bg,
                fg=fg,
                bd=0,
                activebackground=bg,
                command=lambda t=text: self._on_button(t),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

    # ---------- Key bindings ----------
    def _bind_keys(self):
        for key in "0123456789.+-*/%":
            self.bind(key, lambda e, k=key: self._on_button(self._map_key(k)))
        self.bind("<Return>", lambda e: self._on_button("="))
        self.bind("<KP_Enter>", lambda e: self._on_button("="))
        self.bind("<BackSpace>", lambda e: self._on_button("←"))
        self.bind("<Escape>", lambda e: self._on_button("C"))

    @staticmethod
    def _map_key(key):
        return {"*": "×", "/": "÷"}.get(key, key)

    # ---------- Logic ----------
    def _on_button(self, text):
        if text == "C":
            self.expression = ""
        elif text == "←":
            self.expression = self.expression[:-1]
        elif text == "±":
            self._toggle_sign()
        elif text == "=":
            self._evaluate()
            return
        else:
            self.expression += text

        self._update_display()

    def _toggle_sign(self):
        if self.expression.startswith("-"):
            self.expression = self.expression[1:]
        else:
            self.expression = "-" + self.expression

    def _evaluate(self):
        safe_expr = (
            self.expression.replace("×", "*")
            .replace("÷", "/")
            .replace("%", "/100")
        )
        try:
            result = eval(safe_expr, {"__builtins__": {}})
            result = round(result, 10)
            self.expression = str(result)
        except ZeroDivisionError:
            self.expression = ""
            self.display_var.set("Error: ÷ by 0")
            return
        except Exception:
            self.expression = ""
            self.display_var.set("Error")
            return

        self._update_display()

    def _update_display(self):
        self.display_var.set(self.expression if self.expression else "0")


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()