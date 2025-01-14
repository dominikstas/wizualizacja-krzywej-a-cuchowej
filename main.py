import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class Krzywa:
    def __init__(self, root):
        # Konfiguracja głównego okna
        self.root = root
        self.root.title("Wizualizacja krzywej łańcuchowej")
        
        # Ustawienie stylu
        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10, 'bold'))
        style.configure('TLabelframe', font=('Helvetica', 11, 'bold'))
        
        # Główny kontener
        main_container = ttk.Frame(root, padding="10")
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Ramka parametrów
        param_frame = ttk.LabelFrame(main_container, text="Parametry wejściowe", padding="10")
        param_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        # Słownik parametrów
        self.params = {
            "distance": ("Odległość między podporami (m):", "10"),
            "height": ("Wysokość podpór (m):", "0"),
            "chain_length": ("Długość łańcucha (m):", "12"),
            "chain_weight": ("Waga liny (kg/m):", "1")
        }
        
        # Tworzenie pól wprowadzania
        self.entries = {}
        for i, (key, (label_text, default_value)) in enumerate(self.params.items()):
            ttk.Label(param_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(param_frame, width=15)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            entry.insert(0, default_value)
            self.entries[key] = entry

        # Przycisk generowania
        generate_btn = ttk.Button(param_frame, text="Generuj wykres", command=self.plot)
        generate_btn.grid(row=len(self.params), column=0, columnspan=2, pady=10)
        
        # Ramka na wyniki obliczeń
        self.results_frame = ttk.LabelFrame(main_container, text="Wyniki obliczeń", padding="10")
        self.results_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        
        # Etykiety na wyniki
        self.max_force_label = ttk.Label(self.results_frame, text="Maksymalna siła: -")
        self.max_force_label.pack(pady=5)
        
        self.force_components_label = ttk.Label(self.results_frame, text="Składowe wektora siły:\nFx: -\nFy: -")
        self.force_components_label.pack(pady=5)
        
        # Ramka na wykres
        plot_container = ttk.LabelFrame(main_container, text="Wizualizacja", padding="10")
        plot_container.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        self.plot_frame = ttk.Frame(plot_container)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ramka na równanie
        equation_frame = ttk.LabelFrame(main_container, text="Równanie krzywej", padding="10")
        equation_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        self.equation_label = ttk.Label(equation_frame, text="Równanie pojawi się tutaj.", anchor="center")
        self.equation_label.pack(fill="both", expand=True)
        
        # Konfiguracja siatki
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)

    def calculate_forces(self, a, L, w):
        """
        Oblicza siły działające na łańcuch
        a: parametr krzywej łańcuchowej
        L: odległość między podporami
        w: waga liny na metr
        """
        # Obliczanie maksymalnej siły (występuje w najniższym punkcie)
        T_max = w * a
        
        # Obliczanie składowych siły w podporach
        angle = np.arcsinh(L / (2 * a))  # kąt nachylenia w podporach
        Fx = T_max * np.sinh(angle)  # składowa pozioma
        Fy = T_max * np.cosh(angle)  # składowa pionowa
        
        return T_max, Fx, Fy

    def plot(self):
        try:
            # Pobieranie parametrów z pól wprowadzania
            L = float(self.entries["distance"].get())
            h = float(self.entries["height"].get())
            s = float(self.entries["chain_length"].get())
            w = float(self.entries["chain_weight"].get())

            # Sprawdzenie długości łańcucha
            if s <= L:
                messagebox.showerror("Błąd", "Długość łańcucha musi być większa niż odległość między podporami!")
                return

            # Funkcja do znalezienia parametru a
            def find_a(a_guess):
                return 2 * a_guess * np.sinh(L / (2 * a_guess)) - s

            # Metoda bisekcji do znalezienia parametru a
            a_min, a_max = 0.1, 100
            while (a_max - a_min) > 0.0001:
                a = (a_min + a_max) / 2
                if find_a(a) > 0:
                    a_max = a
                else:
                    a_min = a

            a = (a_min + a_max) / 2

            # Obliczanie sił
            T_max, Fx, Fy = self.calculate_forces(a, L, w)
            
            # Aktualizacja etykiet z wynikami
            self.max_force_label.config(text=f"Maksymalna siła: {T_max:.2f} N")
            self.force_components_label.config(
                text=f"Składowe wektora siły:\nFx: {Fx:.2f} N\nFy: {Fy:.2f} N"
            )

            # Generowanie punktów krzywej
            x = np.linspace(0, L, 1000)
            y = a * np.cosh((x - L / 2) / a) - a * np.cosh(L / (2 * a)) + h

            # Aktualizacja równania
            equation_text = f"y = {a:.4f} * cosh((x - {L/2:.4f}) / {a:.4f}) - {a * np.cosh(L / (2 * a)):.4f} + {h:.4f}"
            self.equation_label.config(text=equation_text)

            # Tworzenie wykresu
            plt.clf()
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111)
            
            # Rysowanie krzywej
            ax.plot(x, y, 'b-', label='Krzywa łańcuchowa', linewidth=2)
            ax.plot([0, L], [h, h], 'r--', label='Linia między podporami')
            ax.scatter([0, L], [h, h], color='red', s=100, label='Podpory')
            
            # Dodawanie wektorów sił w podporach
            scale = L / 10  # Skalowanie długości wektorów
            arrow_props = dict(arrowstyle='->', color='green', lw=2)
            
            # Rysowanie wektorów sił
            angle_left = np.arctan2(Fy, -Fx)
            angle_right = np.arctan2(Fy, Fx)
            
            ax.annotate('', xy=(scale * np.cos(angle_left), h + scale * np.sin(angle_left)),
                       xytext=(0, h), arrowprops=arrow_props)
            ax.annotate('', xy=(L + scale * np.cos(angle_right), h + scale * np.sin(angle_right)),
                       xytext=(L, h), arrowprops=arrow_props)

            ax.grid(True)
            ax.legend()
            ax.set_title('Wizualizacja krzywej łańcuchowej')
            ax.set_xlabel('Odległość [m]')
            ax.set_ylabel('Wysokość [m]')

            # Aktualizacja wykresu w interfejsie
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except ValueError:
            messagebox.showerror("Błąd", "Wprowadź poprawne wartości liczbowe!")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił nieoczekiwany błąd: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Krzywa(root)
    root.mainloop()