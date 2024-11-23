import tkinter as tk
from tkinter import messagebox

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Máy tính của Tâm")
        self.geometry("400x550")
        self.configure(bg="#2c3e50")

        self.display = tk.Entry(self, font=("Arial", 24), justify="right", bd=10, relief="flat", fg="white", bg="#34495e")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.create_buttons()

    def create_buttons(self):
        # Các nút của máy tính
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
            ('C', 5, 0), ('(', 5, 1), (')', 5, 2), ('^', 5, 3)
        ]

        for (text, row, col) in buttons:
            self.create_button(text, row, col)

    def create_button(self, text, row, col):
        button = tk.Button(self, text=text, font=("Arial", 18), width=5, height=2, command=lambda: self.on_button_click(text),
                           relief="flat", fg="white", bg="#16a085", activebackground="#1abc9c", activeforeground="white")
        button.grid(row=row, column=col, padx=10, pady=10)

    def on_button_click(self, char):
        current = self.display.get()
        if char == 'C':
            self.display.delete(0, tk.END)
        elif char == '=':
            try:
                result = eval(current)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Lỗi")
                messagebox.showerror("Lỗi", "Có lỗi xảy ra trong phép toán.")
        else:
            self.display.insert(tk.END, char)

if __name__ == "__main__":
    calculator = Calculator()
    calculator.mainloop()
