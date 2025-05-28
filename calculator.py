import tkinter as tk
import random
import sys

try:
    import winsound  # Windows only
    def play_dolphin_sound():
        winsound.PlaySound("dolphin.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
except ImportError:
    try:
        from playsound import playsound
        def play_dolphin_sound():
            playsound("dolphin.wav", block=False)
    except ImportError:
        def play_dolphin_sound():
            pass  # No sound support

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator with Dolphin Sea")
        self.expression = ""
        self.text_input = tk.StringVar()

        # Calculator frame
        calc_frame = tk.Frame(root, bg="#0099cc")
        calc_frame.grid(row=0, column=0, sticky="nsew")

        entry = tk.Entry(
            calc_frame, font=('Arial', 20), textvariable=self.text_input,
            bd=10, insertwidth=2, width=14, borderwidth=4, justify='right',
            bg="#e0f7fa", fg="#005577", relief="sunken"
        )
        entry.grid(row=0, column=0, columnspan=4, pady=(10, 10))

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
            ('=', 5, 0, 4)
        ]

        button_style = {
            "font": ('Arial', 18, 'bold'),
            "bg": "#33ccff",
            "fg": "#003366",
            "activebackground": "#66d9ff",
            "activeforeground": "#003366",
            "relief": "raised",
            "bd": 6,
            "highlightbackground": "#0099cc"
        }

        for (text, row, col, *span) in buttons:
            colspan = span[0] if span else 1
            tk.Button(
                calc_frame, text=text, padx=20, pady=20,
                command=lambda t=text: self.on_button_click(t),
                **button_style
            ).grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

        for i in range(6):
            calc_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            calc_frame.grid_columnconfigure(i, weight=1)

        # Sea frame for dolphins and fish
        self.sea_frame = tk.Frame(root, bg="#b3e0ff", width=300, height=400)
        self.sea_frame.grid(row=0, column=1, sticky="nsew")
        self.sea_frame.grid_propagate(False)

        # Canvas for dolphins and fish
        self.dolphin_canvas = tk.Canvas(self.sea_frame, width=300, height=400, bg="#b3e0ff", highlightthickness=0)
        self.dolphin_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Draw some random fish in the sea background
        self.draw_fish_background()

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=0)
        root.grid_rowconfigure(0, weight=1)

    def draw_fish_background(self):
        # Draw 10 random fish in the background
        fish_colors = ["#ffb347", "#ff6961", "#fdfd96", "#77dd77", "#84b6f4", "#fdcae1"]
        for _ in range(10):
            x = random.randint(10, 270)
            y = random.randint(10, 370)
            color = random.choice(fish_colors)
            # Draw a simple fish shape using an oval and a triangle (tail)
            self.dolphin_canvas.create_oval(x, y, x+30, y+15, fill=color, outline="")
            self.dolphin_canvas.create_polygon(
                x-10, y+7, x, y, x, y+15, fill=color, outline=""
            )
            # Optionally add a small black eye
            self.dolphin_canvas.create_oval(x+22, y+5, x+26, y+9, fill="black", outline="")

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.text_input.set("")
            self.show_dolphins(0)
        elif char == '=':
            play_dolphin_sound()
            try:
                result = str(eval(self.expression))
                self.text_input.set(result)
                self.expression = result
                self.show_dolphins(result)
            except Exception:
                self.text_input.set("Error")
                self.expression = ""
                self.show_dolphins(0)
        else:
            self.expression += str(char)
            self.text_input.set(self.expression)

    def show_dolphins(self, value):
        # Clear dolphins, redraw fish background, then show dolphins in random positions/colors
        self.dolphin_canvas.delete("all")
        self.draw_fish_background()
        try:
            n = int(float(value))
            if n < 0:
                n = 0
            elif n > 100:
                n = 100  # Limit for display
        except Exception:
            n = 0
        for _ in range(n):
            x = random.randint(0, 250)
            y = random.randint(0, 350)
            color = random.choice([
                "#0074D9", "#39CCCC", "#3D85C6", "#1E90FF", "#00BFFF", "#4682B4",
                "#5DADE2", "#2980B9", "#76D7EA", "#40E0D0", "#6495ED", "#00CED1",
                "#ffb347", "#ff6961", "#fdfd96", "#77dd77", "#fdcae1"
            ])
            self.dolphin_canvas.create_text(x, y, text="🐬", font=("Arial", 28), fill=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

# Unit tests
import pytest

@pytest.mark.parametrize("x, y, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add(x, y, expected):
    assert add(x, y) == expected

@pytest.mark.parametrize("x, y, expected", [
    (5, 3, 2),
    (0, 1, -1),
    (-1, -1, 0),
])
def test_subtract(x, y, expected):
    assert subtract(x, y) == expected

@pytest.mark.parametrize("x, y, expected", [
    (2, 3, 6),
    (0, 5, 0),
    (-2, 3, -6),
])
def test_multiply(x, y, expected):
    assert multiply(x, y) == expected

@pytest.mark.parametrize("x, y, expected", [
    (6, 3, 2),
    (5, 2, 2.5),
    (-6, -2, 3),
])
def test_divide(x, y, expected):
    assert divide(x, y) == expected

def test_divide_by_zero():
    import pytest
    with pytest.raises(ValueError):
        divide(5, 0)