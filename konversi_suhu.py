import tkinter as tk
from tkinter import messagebox
import math # Walaupun math tidak digunakan di konversi dasar, ini tetap dipertahankan

class KonverterSuhu:
    """
    Aplikasi Konverter Suhu Universal menggunakan Tkinter.
    Menunjukkan konsep Data Binding dan Trace untuk manajemen state reaktif.
    """
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Konverter Suhu - State Management Demo")
        self.window.geometry("500x400")
        self.window.configure(bg="lightblue")

        # Variabel kontrol (State Management)
        self.celsius_var = tk.DoubleVar()
        self.fahrenheit_var = tk.DoubleVar()
        self.kelvin_var = tk.DoubleVar()
        self.rankine_var = tk.DoubleVar()

        # Flag untuk mencegah infinite loop saat update (Kunci utama)
        self.updating = False

        self.buat_interface()
        self.setup_traces()
        self.update_info() # Tampilkan info awal

    def buat_interface(self):
        """Membuat dan menata semua komponen antarmuka grafis."""
        
        # Judul
        title_label = tk.Label(
            self.window,
            text="KONVERTER SUHU UNIVERSAL",
            font=("Arial", 16, "bold"),
            bg="lightblue"
        )
        title_label.pack(pady=20)

        # Frame utama untuk input
        main_frame = tk.Frame(self.window, bg="lightblue")
        main_frame.pack(fill=tk.BOTH, expand=False, padx=20)
        
        # --- Bagian Input Suhu (Celsius, Fahrenheit, Kelvin, Rankine) ---

        # Helper function untuk membuat baris input
        def create_temp_row(parent, label_text, var):
            frame = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=2)
            frame.pack(fill=tk.X, pady=5)

            tk.Label(
                frame,
                text=label_text,
                font=("Arial", 12, "bold"),
                bg="white",
                width=15,
                anchor="w"
            ).pack(side=tk.LEFT, padx=10, pady=10)

            entry = tk.Entry(
                frame,
                textvariable=var,
                font=("Arial", 12),
                width=20,
                justify="center"
            )
            entry.pack(side=tk.RIGHT, padx=10, pady=10)
            return entry
        
        # Buat semua baris input
        create_temp_row(main_frame, "Celsius (°C):", self.celsius_var)
        create_temp_row(main_frame, "Fahrenheit (°F):", self.fahrenheit_var)
        create_temp_row(main_frame, "Kelvin (K):", self.kelvin_var)
        create_temp_row(main_frame, "Rankine (°R):", self.rankine_var)

        # --- Tombol Reset ---
        btn_reset = tk.Button(
            main_frame,
            text="Reset Semua",
            font=("Arial", 12, "bold"),
            bg="red",
            fg="white",
            command=self.reset_all
        )
        btn_reset.pack(pady=15)

        # --- Bagian Informasi Tambahan ---
        info_frame = tk.Frame(self.window, bg="lightyellow", relief=tk.GROOVE, bd=2)
        info_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            info_frame,
            text="INFORMASI SUHU",
            font=("Arial", 12, "bold"),
            bg="lightyellow"
        ).pack(pady=5)

        self.info_label = tk.Label(
            info_frame,
            text="Masukkan nilai suhu di salah satu field",
            font=("Arial", 10),
            bg="lightyellow",
            justify=tk.LEFT
        )
        self.info_label.pack(pady=5)
    
    def setup_traces(self):
        """Menghubungkan variabel kontrol dengan event handler."""
        # Menambahkan 'trace' ke event "write" (perubahan nilai)
        self.celsius_var.trace_add("write", self.from_celsius)
        self.fahrenheit_var.trace_add("write", self.from_fahrenheit)
        self.kelvin_var.trace_add("write", self.from_kelvin)
        self.rankine_var.trace_add("write", self.from_rankine)
        
    # --- EVENT HANDLERS (Konversi) ---

    def from_celsius(self, *args):
        """Konversi dari Celsius ke skala lain."""
        if self.updating: return

        try:
            celsius = self.celsius_var.get()
            self.updating = True

            fahrenheit = (celsius * 9/5) + 32
            kelvin = celsius + 273.15
            rankine = (celsius + 273.15) * 9/5

            self.fahrenheit_var.set(round(fahrenheit, 2))
            self.kelvin_var.set(round(kelvin, 2))
            self.rankine_var.set(round(rankine, 2))
            
            self.update_info()

        except tk.TclError:
            # Terjadi saat input kosong atau tidak valid (non-angka)
            pass
        finally:
            self.updating = False

    def from_fahrenheit(self, *args):
        """Konversi dari Fahrenheit ke skala lain."""
        if self.updating: return

        try:
            fahrenheit = self.fahrenheit_var.get()
            self.updating = True

            celsius = (fahrenheit - 32) * 5/9
            kelvin = celsius + 273.15
            rankine = fahrenheit + 459.67

            self.celsius_var.set(round(celsius, 2))
            self.kelvin_var.set(round(kelvin, 2))
            self.rankine_var.set(round(rankine, 2))
            
            self.update_info()

        except tk.TclError:
            pass
        finally:
            self.updating = False

    def from_kelvin(self, *args):
        """Konversi dari Kelvin ke skala lain."""
        if self.updating: return

        try:
            kelvin = self.kelvin_var.get()
            self.updating = True

            celsius = kelvin - 273.15
            fahrenheit = (celsius * 9/5) + 32
            rankine = kelvin * 9/5

            self.celsius_var.set(round(celsius, 2))
            self.fahrenheit_var.set(round(fahrenheit, 2))
            self.rankine_var.set(round(rankine, 2))
            
            self.update_info()

        except tk.TclError:
            pass
        finally:
            self.updating = False

    def from_rankine(self, *args):
        """Konversi dari Rankine ke skala lain."""
        if self.updating: return

        try:
            rankine = self.rankine_var.get()
            self.updating = True

            kelvin = rankine * 5/9
            celsius = kelvin - 273.15
            fahrenheit = rankine - 459.67

            self.kelvin_var.set(round(kelvin, 2))
            self.celsius_var.set(round(celsius, 2))
            self.fahrenheit_var.set(round(fahrenheit, 2))
            
            self.update_info()

        except tk.TclError:
            pass
        finally:
            self.updating = False
            
    # --- UTILITY METHODS ---

    def reset_all(self):
        """Mereset semua field ke 0."""
        self.updating = True
        try:
            # Gunakan set() pada variabel kontrol
            self.celsius_var.set(0)
            self.fahrenheit_var.set(32) # Fahrenheit 0C
            self.kelvin_var.set(273.15) # Kelvin 0C
            self.rankine_var.set(491.67) # Rankine 0C
            self.update_info()
        finally:
            self.updating = False

    def update_info(self):
        """Memperbarui informasi kontekstual berdasarkan nilai Celsius."""
        try:
            celsius = self.celsius_var.get()
            info_text = f"Suhu saat ini: {celsius}°C\n"

            if celsius == 0:
                info_text += "• Titik beku air (kondisi normal)"
            elif celsius == 100:
                info_text += "• Titik didih air (kondisi normal)"
            elif abs(celsius - (-273.15)) < 0.01: # Toleransi untuk Absolut Nol
                info_text += "• Suhu absolut nol (0 K)"
            elif celsius < 0:
                info_text += "• Di bawah titik beku air"
            elif celsius > 100:
                info_text += "• Di atas titik didih air"
            else:
                info_text += "• Suhu umum"

            self.info_label.config(text=info_text)
        except tk.TclError:
            # Jika field kosong atau non-angka, tampilkan pesan error
            self.info_label.config(text="Masukkan nilai suhu yang valid")

    def jalankan(self):
        """Method untuk menjalankan aplikasi."""
        self.window.mainloop()

# Untuk menjalankan aplikasi
if __name__ == "__main__":
    app = KonverterSuhu()
    app.jalankan()