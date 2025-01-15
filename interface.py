# Importy niezbędnych bibliotek
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


class KrzywaUI:
    def __init__(self, root, calculations):
        # Inicjalizacja głównego okna i obiektu z obliczeniami
        self.root = root
        self.calculations = calculations
        self.root.title("Wizualizacja krzywej łańcuchowej")
        self.root.geometry("1200x800")
        
        # Definicja kolorów używanych w interfejsie
        self.colors = {
            'bg': '#f0f2f5',
            'frame_bg': '#ffffff',
            'accent': '#2962ff',
            'text': '#1a1a1a',
            'success': '#4caf50'
        }
        
        # Konfiguracja stylów 
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Main.TFrame', background=self.colors['bg'])
        style.configure('Card.TLabelframe', background=self.colors['frame_bg'], padding=15, relief='flat', borderwidth=0)
        style.configure('Card.TLabelframe.Label', font=('Segoe UI', 12, 'bold'), foreground=self.colors['accent'], background=self.colors['frame_bg'])
        style.configure('TLabel', font=('Segoe UI', 10), background=self.colors['frame_bg'], foreground=self.colors['text'])
        style.configure('TEntry', padding=5, relief='flat')
        style.configure('Generate.TButton', padding=10, font=('Segoe UI', 10, 'bold'))

        # Tworzenie głównego kontenera
        self.main_container = ttk.Frame(root, style='Main.TFrame')
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Tworzenie panelu wejściowego
        self.input_panel = ttk.Frame(self.main_container, style='Main.TFrame')
        self.input_panel.pack(fill=tk.X, padx=5, pady=5)
        self.create_input_panel()

        self.canvas = tk.Canvas(self.main_container, background=self.colors['bg'])
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.plot_panel = ttk.Frame(self.canvas, style='Main.TFrame')
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.plot_panel.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.plot_panel, anchor="nw")
        
        # Dodanie obsługi scrollowania
        self.root.bind("<MouseWheel>", self._on_mousewheel)
        
        # Tworzenie przycisków i kontenerów dla wykresu i wyników
        self.new_plot_btn = ttk.Button(self.plot_panel, text="Rysuj nowy wykres", style='Generate.TButton', command=self.show_input_panel)
        
        self.plot_container = ttk.LabelFrame(self.plot_panel, text="Wizualizacja", style='Card.TLabelframe')
        self.plot_frame = ttk.Frame(self.plot_container)
        
        self.results_container = ttk.LabelFrame(self.plot_panel, text="Siła", style='Card.TLabelframe')
        self.max_force_label = ttk.Label(self.results_container, text="Maksymalna siła: -", font=('Segoe UI', 11))
        self.max_force_label.pack(pady=10)
        
        self.equation_frame = ttk.Labelframe(self.plot_panel, text="Równanie krzywej", style='Card.TLabelframe')
        self.equation_label = ttk.Label(self.equation_frame, text="Równanie pojawi się tutaj.", font=('Segoe UI', 11))
        self.equation_label.pack(pady=10)

    def _configure_canvas(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    # Scroll
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Panel wejściowy
    def create_input_panel(self):
        param_frame = ttk.LabelFrame(self.input_panel, text="Parametry wejściowe", style='Card.TLabelframe')
        param_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # Definicja parametrów wejściowych
        self.params = {
            "distance": ("Odległość między podporami (m):", "10"),
            "height": ("Wysokość podpór (m):", "2"),
            "chain_length": ("Długość łańcucha (m):", "15"),
            "chain_weight": ("Waga liny (kg/m):", "0.05")
        }
        
        # Tworzenie pól wejściowych dla parametrów
        self.entries = {}
        for i, (key, (label_text, default_value)) in enumerate(self.params.items()):
            frame = ttk.Frame(param_frame, style='Main.TFrame')
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=label_text).pack(side=tk.LEFT, padx=5)
            entry = ttk.Entry(frame, width=15)
            entry.pack(side=tk.RIGHT, padx=5)
            entry.insert(0, default_value)
            self.entries[key] = entry

        # Przycisk do generowania wykresu
        generate_btn = ttk.Button(param_frame, text="Generuj wykres", style='Generate.TButton', command=self.plot)
        generate_btn.pack(pady=15)

    # Panel wejściowy
    def show_input_panel(self):
        self.canvas.pack_forget()
        self.scrollbar.pack_forget()
        self.input_panel.pack(fill=tk.X, padx=5, pady=5)

    # Panel z wykresem
    def show_plot_panel(self):
        self.input_panel.pack_forget()
        
        self.new_plot_btn.pack(pady=(0, 10))
        self.plot_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)
        self.results_container.pack(fill=tk.X, padx=5, pady=5)
        self.equation_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.plot_panel.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Metoda generująca wykres
    def plot(self):
        try:
            # Pobieranie wartości z pól wejściowych
            L = float(self.entries["distance"].get())
            h = float(self.entries["height"].get())
            s = float(self.entries["chain_length"].get())
            w = float(self.entries["chain_weight"].get())

            # Sprawdzenie poprawności danych wejściowych
            if s <= L:
                messagebox.showerror("Błąd", "Długość łańcucha musi być większa niż odległość między podporami!")
                return

            # Obliczenia
            a = self.calculations.find_a(L, s)
            T_max = self.calculations.calculate_forces(a, L, w)
            
            # Aktualizacja etykiet z wynikami
            self.max_force_label.config(text=f"Maksymalna siła, działająca w najniższym punkcie łańcucha: {T_max:.2f} N", foreground=self.colors['success'])

            # Generowanie punktów krzywej
            x = self.calculations.generate_x(L)
            y = self.calculations.generate_y(a, L, h, x)

            # Aktualizacja równania krzywej
            equation_text = f"y = {a:.4f} * cosh((x - {L/2:.4f}) / {a:.4f}) - {a * np.cosh(L / (2 * a)):.4f} + {h:.4f}"
            self.equation_label.config(text=equation_text)

            # Wyświetlenie panelu z wykresem 
            self.show_plot_panel()
            self._draw_plot(x, y, L, h, T_max,)

        except ValueError:
            messagebox.showerror("Błąd", "Wprowadź poprawne wartości liczbowe!")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił nieoczekiwany błąd: {str(e)}")

    # Wykres
    def _draw_plot(self, x, y, L, h, T_max):
        plt.clf()
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        
        # Ustawienie kolorów tła
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('#ffffff')
        
        # Rysowanie krzywej łańcuchowej
        ax.plot(x, y, color=self.colors['accent'], label='Krzywa łańcuchowa', linewidth=2.5)
        ax.plot([0, L], [h, h], 'r--', label='Linia między podporami', linewidth=1.5)
        ax.scatter([0, L], [h, h], color='red', s=100, label='Podpory', zorder=5)
        

        # Konfiguracja wykresu
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none')
        ax.set_title('Wizualizacja krzywej łańcuchowej', pad=20, fontsize=12, fontweight='bold')
        ax.set_xlabel('Odległość [m]', labelpad=10)
        ax.set_ylabel('Wysokość [m]', labelpad=10)

        plt.tight_layout()
        y_min, y_max = ax.get_ylim()
        margin = (y_max - y_min) * 0.1
        ax.set_ylim(y_min - margin, y_max + margin)

        # Usunięcie poprzedniego wykresu i dodanie nowego
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Funkcja dostosowująca rozmiar wykresu do rozmiaru okna
        def on_resize(event):
            width = event.width
            height = event.height
            fig.set_size_inches(width/fig.dpi, height/fig.dpi)
            canvas.draw()
        
        canvas_widget.bind("<Configure>", on_resize)

