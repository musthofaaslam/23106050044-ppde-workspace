import tkinter as tk
from tkinter import ttk

class ResponsiveApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Responsive Design dengan ttk")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Variabel untuk tracking ukuran window
        self.current_width = 800
        self.current_height = 600

        self._setup_styles()
        self._buat_interface()
        self._bind_events()

    def _setup_styles(self):
        """
        Menyiapkan style ttk yang berbeda untuk ukuran window yang berbeda.
        """
        self.style = ttk.Style()

        # Style untuk desktop (lebar > 700px)
        self.style.configure('Desktop.TLabel',
                           font=('Arial', 12),
                           padding=(10, 5))
        self.style.configure('Desktop.TButton',
                           padding=(15, 8),
                           font=('Arial', 11))

        # Style untuk tablet (lebar 500px - 700px)
        self.style.configure('Tablet.TLabel',
                           font=('Arial', 10),
                           padding=(8, 4))
        self.style.configure('Tablet.TButton',
                           padding=(12, 6),
                           font=('Arial', 10))

        # Style untuk mobile (lebar < 500px)
        self.style.configure('Mobile.TLabel',
                           font=('Arial', 9),
                           padding=(5, 3))
        self.style.configure('Mobile.TButton',
                           padding=(8, 4),
                           font=('Arial', 9))

    def _buat_interface(self):
        """
        Membuat seluruh antarmuka pengguna dengan widget demo.
        """
        # Main container dengan scrollable frame
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Header section
        self.header_frame = ttk.Frame(self.scrollable_frame)
        self.header_frame.pack(fill='x', padx=20, pady=20)

        self.title_label = ttk.Label(self.header_frame, text="Responsive Design Demo",
                                    style='Desktop.TLabel')
        self.title_label.pack()

        self.size_label = ttk.Label(self.header_frame, text=f"Window Size: {self.current_width}x{self.current_height}",
                                   style='Desktop.TLabel')
        self.size_label.pack(pady=(5,0))

        # Content grid yang akan berubah layout
        self.content_frame = ttk.Frame(self.scrollable_frame)
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=(0,20))

        # Cards yang akan di-reposition berdasarkan ukuran window
        self.cards = []
        for i in range(6):
            card = ttk.LabelFrame(self.content_frame, text=f"Card {i+1}", padding="15")

            ttk.Label(card, text=f"Content untuk card {i+1}",
                     style='Desktop.TLabel').pack()
            ttk.Button(card, text=f"Action {i+1}",
                      style='Desktop.TButton').pack(pady=(10,0))

            self.cards.append(card)

        # Control panel
        self.control_frame = ttk.LabelFrame(self.scrollable_frame, text="Controls", padding="15")
        self.control_frame.pack(fill='x', padx=20, pady=(0,20))

        ttk.Button(self.control_frame, text="Simulate Mobile (400x600)",
                  command=lambda: self.resize_window(400, 600),
                  style='Desktop.TButton').pack(side='left', padx=(0,10))

        ttk.Button(self.control_frame, text="Simulate Tablet (600x800)",
                  command=lambda: self.resize_window(600, 800),
                  style='Desktop.TButton').pack(side='left', padx=(0,10))

        ttk.Button(self.control_frame, text="Simulate Desktop (800x600)",
                  command=lambda: self.resize_window(800, 600),
                  style='Desktop.TButton').pack(side='left')

        # Pack canvas dan scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Initial layout
        self._update_layout()

    def _bind_events(self):
        """
        Mengikat event resize window ke method _on_window_resize.
        """
        self.root.bind('<Configure>', self._on_window_resize)

    def _on_window_resize(self, event):
        """
        Memperbarui layout dan style saat ukuran window berubah.
        """
        if event.widget == self.root:
            self.current_width = self.root.winfo_width()
            self.current_height = self.root.winfo_height()
            self.size_label.config(text=f"Window Size: {self.current_width}x{self.current_height}")
            self._update_layout()

    def _update_layout(self):
        """
        Menentukan dan menerapkan layout berdasarkan lebar window saat ini.
        """
        # Hapus layout yang ada
        for card in self.cards:
            card.pack_forget()

        # Tentukan layout berdasarkan lebar window
        if self.current_width < 500:  # Mobile
            self._apply_mobile_layout()
        elif self.current_width < 700:  # Tablet
            self._apply_tablet_layout()
        else:  # Desktop
            self._apply_desktop_layout()

    def _apply_mobile_layout(self):
        """
        Menerapkan layout satu kolom untuk tampilan mobile.
        """
        # Layout satu kolom
        for card in self.cards:
            card.pack(fill='x', pady=(0,10))
        self._update_styles('Mobile')

    def _apply_tablet_layout(self):
        """
        Menerapkan layout dua kolom untuk tampilan tablet.
        """
        # Layout dua kolom
        for i, card in enumerate(self.cards):
            if i % 2 == 0:
                card.pack(side='left', fill='both', expand=True, padx=(0,5), pady=(0,10))
            else:
                card.pack(side='right', fill='both', expand=True, padx=(5,0), pady=(0,10))
        self._update_styles('Tablet')

    def _apply_desktop_layout(self):
        """
        Menerapkan layout tiga kolom untuk tampilan desktop.
        """
        # Layout tiga kolom
        for i, card in enumerate(self.cards):
            card.pack_configure(side='left', fill='both', expand=True, padx=(5,5) if i%3 == 1 else (0,5) if i%3 == 0 else (5,0), pady=(0,10))
        self._update_styles('Desktop')

    def _update_styles(self, size):
        """
        Mengubah style widget berdasarkan ukuran layar yang dipilih.
        """
        style_suffix = f'{size}.TLabel'
        button_style = f'{size}.TButton'

        self.title_label.config(style=style_suffix)
        self.size_label.config(style=style_suffix)

        # Perbarui semua label dan tombol di dalam cards
        for card in self.cards:
            for child in card.winfo_children():
                if isinstance(child, ttk.Label):
                    child.config(style=style_suffix)
                elif isinstance(child, ttk.Button):
                    child.config(style=button_style)

    def resize_window(self, width, height):
        """
        Mengubah ukuran window secara paksa untuk simulasi.
        """
        self.root.geometry(f"{width}x{height}")

    def run(self):
        """
        Memulai loop utama aplikasi.
        """
        self.root.mainloop()

# Jalankan aplikasi
if __name__ == "__main__":
    app = ResponsiveApp()
    app.run()
