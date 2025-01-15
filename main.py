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
        self.root.geometry("1200x800")  
        
        # Konfiguracja kolorów i stylu
        self.colors = {
            'bg': '#f0f2f5',
            'frame_bg': '#ffffff',
            'accent': '#2962ff',
            'text': '#1a1a1a',
            'success': '#4caf50'
        }
        
        # Ustawienie stylu
        style = ttk.Style()
        style.theme_use('clam')  # Używamy motywu 'clam' jako bazy
        
        # Konfiguracja stylów
        style.configure('Main.TFrame', background=self.colors['bg'])
        style.configure('Card.TLabelframe', 
                       background=self.colors['frame_bg'],
                       padding=15,
                       relief='flat',
                       borderwidth=0)
        style.configure('Card.TLabelframe.Label', 
                       font=('Segoe UI', 12, 'bold'),
                       foreground=self.colors['accent'],
                       background=self.colors['frame_bg'])
        style.configure('TLabel', 
                       font=('Segoe UI', 10),
                       background=self.colors['frame_bg'],
                       foreground=self.colors['text'])
        style.configure('TEntry', 
                       padding=5,
                       relief='flat')
        style.configure('Generate.TButton',
                       padding=10,
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['accent'])
        
        # Główny kontener
        main_container = ttk.Frame(root, style='Main.TFrame', padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Górny panel (parametry i wyniki)
        top_panel = ttk.Frame(main_container, style='Main.TFrame')
        top_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Ramka parametrów
        param_frame = ttk.LabelFrame(top_panel, 
                                   text="Parametry wejściowe",
                                   style='Card.TLabelframe')
        param_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
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
            frame = ttk.Frame(param_frame, style='Main.TFrame')
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=label_text).pack(side=tk.LEFT, padx=5)
            entry = ttk.Entry(frame, width=15)
            entry.pack(side=tk.RIGHT, padx=5)
            entry.insert(0, default_value)
            self.entries[key] = entry

        # Przycisk generowania
        generate_btn = ttk.Button(param_frame, 
                                text="Generuj wykres",
                                style='Generate.TButton',
                                command=self.plot)
        generate_btn.pack(pady=15)
        
        # Ramka na wyniki obliczeń
        self.results_frame = ttk.LabelFrame(top_panel,
                                          text="Wyniki obliczeń",
                                          style='Card.TLabelframe')
        self.results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Etykiety na wyniki
        self.max_force_label = ttk.Label(self.results_frame, 
                                       text="Maksymalna siła: -",
                                       font=('Segoe UI', 11))
        self.max_force_label.pack(pady=10)
        
        self.force_components_label = ttk.Label(self.results_frame,
                                              text="Składowe wektora siły:\nFx: -\nFy: -",
                                              font=('Segoe UI', 11))
        self.force_components_label.pack(pady=10)
        
        # Ramka na wykres
        plot_container = ttk.LabelFrame(main_container,
                                      text="Wizualizacja",
                                      style='Card.TLabelframe')
        plot_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        self.plot_frame = ttk.Frame(plot_container)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Ramka na równanie
        equation_frame = ttk.LabelFrame(main_container,
                                      text="Równanie krzywej",
                                      style='Card.TLabelframe')
        equation_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.equation_label = ttk.Label(equation_frame,
                                      text="Równanie pojawi się tutaj.",
                                      font=('Segoe UI', 11))
        self.equation_label.pack(pady=10)

    def calculate_forces(self, a, L, w):
        """
        Oblicza siły działające na łańcuch
        """
        T_max = w * a
        angle = np.arcsinh(L / (2 * a))
        Fx = T_max * np.sinh(angle)
        Fy = T_max * np.cosh(angle)
        return T_max, Fx, Fy

    def plot(self):
        try:
            # Pobieranie i walidacja parametrów
            L = float(self.entries["distance"].get())
            h = float(self.entries["height"].get())
            s = float(self.entries["chain_length"].get())
            w = float(self.entries["chain_weight"].get())

            if s <= L:
                messagebox.showerror("Błąd", "Długość łańcucha musi być większa niż odległość między podporami!")
                return

            # Obliczanie parametru a
            def find_a(a_guess):
                return 2 * a_guess * np.sinh(L / (2 * a_guess)) - s

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
            
            # Aktualizacja wyników
            self.max_force_label.config(
                text=f"Maksymalna siła: {T_max:.2f} N",
                foreground=self.colors['success']
            )
            self.force_components_label.config(
                text=f"Składowe wektora siły:\nFx: {Fx:.2f} N\nFy: {Fy:.2f} N",
                foreground=self.colors['success']
            )

            # Generowanie punktów krzywej
            x = np.linspace(0, L, 1000)
            y = a * np.cosh((x - L / 2) / a) - a * np.cosh(L / (2 * a)) + h

            # Aktualizacja równania
            equation_text = f"y = {a:.4f} * cosh((x - {L/2:.4f}) / {a:.4f}) - {a * np.cosh(L / (2 * a)):.4f} + {h:.4f}"
            self.equation_label.config(text=equation_text)

            # Tworzenie nowego wykresu
            plt.clf()
            fig = plt.figure(figsize=(12, 6))  # Zwiększony rozmiar wykresu
            ax = fig.add_subplot(111)
            
            # Ustawienie stylu wykresu
            ax.set_facecolor('#f8f9fa')
            fig.patch.set_facecolor('#ffffff')
            
            # Rysowanie krzywej
            ax.plot(x, y, color=self.colors['accent'], 
                   label='Krzywa łańcuchowa', linewidth=2.5)
            ax.plot([0, L], [h, h], 'r--', 
                   label='Linia między podporami', linewidth=1.5)
            ax.scatter([0, L], [h, h], color='red', s=100, 
                      label='Podpory', zorder=5)
            
            # Rysowanie wektorów sił
            scale = L / 10
            arrow_props = dict(arrowstyle='->', color='green', 
                             lw=2, mutation_scale=15)
            
            angle_left = np.arctan2(Fy, -Fx)
            angle_right = np.arctan2(Fy, Fx)
            
            ax.annotate('', xy=(scale * np.cos(angle_left), 
                               h + scale * np.sin(angle_left)),
                       xytext=(0, h), arrowprops=arrow_props)
            ax.annotate('', xy=(L + scale * np.cos(angle_right), 
                               h + scale * np.sin(angle_right)),
                       xytext=(L, h), arrowprops=arrow_props)

            # Konfiguracja wykresu
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend(loc='upper right', frameon=True, 
                     facecolor='white', edgecolor='none')
            ax.set_title('Wizualizacja krzywej łańcuchowej', 
                        pad=20, fontsize=12, fontweight='bold')
            ax.set_xlabel('Odległość [m]', labelpad=10)
            ax.set_ylabel('Wysokość [m]', labelpad=10)

            # Dostosowanie marginesów i zakresu osi
            plt.tight_layout()
            
            # Dodanie małego marginesu do zakresu osi y
            y_min, y_max = ax.get_ylim()
            margin = (y_max - y_min) * 0.1
            ax.set_ylim(y_min - margin, y_max + margin)

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