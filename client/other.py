import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
root.withdraw()

prompt_value = simpledialog.askstring("Input", "Please enter a value:", parent=root)

if prompt_value is not None:
    print("You entered:", prompt_value)
else:
    print("No value entered.")

root.mainloop()
