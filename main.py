import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class CatenaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wizualizacja krzywej łańcuchowej")
        
        # Tworzenie ekranu na parametry
        param_frame = ttk.LabelFrame(root, text="Parametry", padding="10")
        param_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        # Etykiety i pola wprowadzania
        ttk.Label(param_frame, text="Odległość między podporami (m):").grid(row=0, column=0, padx=5, pady=5)
        self.distance = ttk.Entry(param_frame)
        self.distance.grid(row=0, column=1, padx=5, pady=5)
        self.distance.insert(0, "10")
        
        ttk.Label(param_frame, text="Wysokość lewej podpory (m):").grid(row=1, column=0, padx=5, pady=5)
        self.height_left = ttk.Entry(param_frame)
        self.height_left.grid(row=1, column=1, padx=5, pady=5)
        self.height_left.insert(0, "0")
        
        ttk.Label(param_frame, text="Wysokość prawej podpory (m):").grid(row=2, column=0, padx=5, pady=5)
        self.height_right = ttk.Entry(param_frame)
        self.height_right.grid(row=2, column=1, padx=5, pady=5)
        self.height_right.insert(0, "0")
        
        ttk.Label(param_frame, text="Długość łańcucha (m):").grid(row=3, column=0, padx=5, pady=5)
        self.chain_length = ttk.Entry(param_frame)
        self.chain_length.grid(row=3, column=1, padx=5, pady=5)
        self.chain_length.insert(0, "12")
        
        # Dodac pola do obciążeń


        # Przycisk do generowania wykresu
        ttk.Button(param_frame, text="Generuj wykres", command=self.plot_catenary).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Ramka na wykres
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        # Konfiguracja siatki
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        
    def plot_catenary(self):
        try:
            # Pobieranie parametrów
            L = float(self.distance.get())
            h1 = float(self.height_left.get())
            h2 = float(self.height_right.get())
            s = float(self.chain_length.get())
            
            # Sprawdzenie, czy długość łańcucha jest wystarczająca
            if s <= math.sqrt(L**2 + (h2-h1)**2):
                tk.messagebox.showerror("Błąd", "Długość łańcucha jest zbyt mała!")
                return
            
            # Obliczanie parametrów krzywej łańcuchowej
            def find_a(a_guess):
                # Funkcja pomocnicza do znalezienia parametru a
                return 2*a_guess*np.sinh(L/(2*a_guess)) - s
            
            # Znajdowanie parametru a metodą bisekcji
            a_min = 0.1
            a_max = 100
            while (a_max - a_min) > 0.0001:
                a = (a_min + a_max) / 2
                if find_a(a) > 0:
                    a_max = a
                else:
                    a_min = a
            
            a = (a_min + a_max) / 2
            
            # Generowanie punktów krzywej
            x = np.linspace(0, L, 1000)
            y = a * np.cosh((x - L/2)/a) + (h1 + h2)/2 - a * np.cosh(L/(2*a))
            
            # Tworzenie wykresu
            plt.clf()
            fig = plt.gcf()
            plt.plot(x, y, 'b-', label='Krzywa łańcuchowa')
            plt.plot([0, L], [h1, h2], 'r--', label='Linia między podporami')
            plt.scatter([0, L], [h1, h2], color='red', s=100, label='Podpory')
            
            plt.grid(True)
            plt.legend()
            plt.title('Wizualizacja krzywej łańcuchowej')
            plt.xlabel('Odległość [m]')
            plt.ylabel('Wysokość [m]')
            
            # Usuwanie starego wykresu jeśli istnieje
            for widget in self.plot_frame.winfo_children():
                widget.destroy()
            
            # Dodawanie nowego wykresu do interfejsu
            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except ValueError:
            tk.messagebox.showerror("Błąd", "Wprowadź poprawne wartości liczbowe!")
        except Exception as e:
            tk.messagebox.showerror("Błąd", f"Wystąpił błąd: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CatenaryApp(root)
    root.mainloop()
