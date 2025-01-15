import tkinter as tk
from interface import KrzywaUI
from calculations import KrzywaCalculations

if __name__ == "__main__":
    root = tk.Tk()
    calculations = KrzywaCalculations()
    app = KrzywaUI(root, calculations)
    root.mainloop()