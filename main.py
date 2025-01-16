import tkinter as tk
from interface import KrzywaUI
from calculations import Calculations

if __name__ == "__main__":
    root = tk.Tk()
    calculations = Calculations()
    app = KrzywaUI(root, calculations)
    root.mainloop()