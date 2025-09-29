import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class ThemeSwitcher:
    def __init__(self):
        """Menginisialisasi aplikasi GUI."""
        self.root = tk.Tk()
        self.root.title("Theme Switcher Demo")
        self.root.geometry("600x500")

        # Inisialisasi style
        self.style = ttk.Style()
        self.current_theme = tk.StringVar(value=self.style.theme_use())
        self.current_font = tk.StringVar()

        self._buat_interface()
        self._setup_themes()

    def _buat_interface(self):
        """Membuat seluruh layout dan widget aplikasi."""
        # Frame utama
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill='both', expand=True)

        # Header
        ttk.Label(main_frame, text="Theme Switcher Demo",
                 font=('Arial', 16, 'bold')).pack(pady=(0,20))

        # --- Frame untuk theme dan font selection ---
        selection_frame = ttk.Frame(main_frame)
        selection_frame.pack(fill='x', pady=(0,20))

        # Frame untuk theme selection
        theme_frame = ttk.LabelFrame(selection_frame, text="Pilih Theme", padding="10")
        theme_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))

        # Combobox untuk memilih theme
        ttk.Label(theme_frame, text="Theme:").pack(anchor='w')
        self.theme_combo = ttk.Combobox(theme_frame, textvariable=self.current_theme,
                                       values=self.style.theme_names(), state="readonly")
        self.theme_combo.pack(fill='x', pady=(5,10))
        self.theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        
        # Frame untuk font selection
        font_frame = ttk.LabelFrame(selection_frame, text="Pilih Font", padding="10")
        font_frame.pack(side='right', fill='x', expand=True)

        # Combobox untuk memilih font
        ttk.Label(font_frame, text="Font:").pack(anchor='w')
        self.font_combo = ttk.Combobox(font_frame, textvariable=self.current_font, state="readonly")
        self.font_combo.pack(fill='x', pady=(5,10))
        self.font_combo.bind('<<ComboboxSelected>>', self.change_font)

        # --- Frame untuk demo widgets ---
        demo_frame = ttk.LabelFrame(main_frame, text="Demo Widgets", padding="10")
        demo_frame.pack(fill='both', expand=True)

        # Entry widget
        ttk.Label(demo_frame, text="Entry Widget:").pack(anchor='w')
        self.demo_entry = ttk.Entry(demo_frame)
        self.demo_entry.pack(fill='x', pady=(5,10))
        self.demo_entry.insert(0, "Contoh text...")

        # Button widgets
        button_frame = ttk.Frame(demo_frame)
        button_frame.pack(fill='x', pady=(0,10))

        ttk.Button(button_frame, text="Normal Button").pack(side='left', padx=(0,5))
        ttk.Button(button_frame, text="Disabled Button", state='disabled').pack(side='left')

        # Progressbar
        ttk.Label(demo_frame, text="Progress Bar:").pack(anchor='w')
        self.progress = ttk.Progressbar(demo_frame, mode='determinate', value=70)
        self.progress.pack(fill='x', pady=(5,10))

        # Scale
        ttk.Label(demo_frame, text="Scale Widget:").pack(anchor='w')
        self.scale = ttk.Scale(demo_frame, from_=0, to=100, orient='horizontal')
        self.scale.pack(fill='x', pady=(5,10))
        self.scale.set(50)

    def _setup_themes(self):
        """Mengisi daftar tema dan font yang tersedia."""
        # Menyiapkan Combobox tema
        available_themes = self.style.theme_names()
        print(f"Available themes: {available_themes}")
        
        # Menyiapkan Combobox font
        font_families = tkFont.families()
        self.font_combo['values'] = sorted(list(font_families))
        # Tetapkan font awal
        default_font = 'Arial'
        if default_font in self.font_combo['values']:
            self.current_font.set(default_font)
        else:
            self.current_font.set(self.font_combo['values'][0])
        self.change_font()


    def change_theme(self, event=None):
        """Mengubah tema aplikasi saat combobox dipilih."""
        selected_theme = self.current_theme.get()
        try:
            self.style.theme_use(selected_theme)
            print(f"Theme changed to: {selected_theme}")
            # Terapkan kembali font setelah tema diubah
            self.change_font()
        except tk.TclError as e:
            print(f"Error changing theme: {e}")

    def change_font(self, event=None):
        """Mengubah font aplikasi saat combobox dipilih."""
        selected_font = self.current_font.get()
        if not selected_font:
            return
        
        try:
            # Konfigurasi style font untuk Label dan Entry
            self.style.configure('TLabel', font=(selected_font, 10))
            self.style.configure('TEntry', font=(selected_font, 10))
            print(f"Font changed to: {selected_font}")
        except tk.TclError as e:
            print(f"Error changing font: {e}")

    def run(self):
        """Memulai loop utama aplikasi."""
        self.root.mainloop()

# Jalankan aplikasi
if __name__ == "__main__":
    app = ThemeSwitcher()
    app.run()
