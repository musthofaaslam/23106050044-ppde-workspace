import tkinter as tk
from tkinter import messagebox

class KalkulatorEventDriven:
    """
    Kelas untuk membuat Kalkulator dengan Antarmuka Grafis (GUI)
    menggunakan Tkinter, yang beroperasi berdasarkan peristiwa (event-driven).
    """
    def __init__(self):
        # 1. Inisialisasi Window
        self.window = tk.Tk()
        self.window.title("Kalkulator Event-Driven")
        self.window.geometry("300x400")
        self.window.configure(bg="lightgray")

        # 2. Variabel State (Penyimpanan Data)
        self.current_input = ""  # Angka yang sedang diketik
        self.operator = ""       # Operator yang dipilih (+, -, *, /)
        self.first_number = 0    # Angka pertama untuk perhitungan

        # 3. Bangun Antarmuka
        self.buat_interface()

    def buat_interface(self):
        """Membuat dan menata komponen GUI (display dan tombol)."""
        # Display untuk menampilkan angka
        self.display = tk.Entry(
            self.window, 
            font=("Arial", 16), 
            justify="right",
            state="readonly", # Agar user tidak bisa mengetik langsung
            bg="white",
            bd=5
        )
        self.display.pack(fill=tk.X, padx=10, pady=10)

        # Frame untuk tombol
        button_frame = tk.Frame(self.window, bg="lightgray")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Penempatan Tombol Angka (1-9)
        for i in range(3): # Baris
            for j in range(3): # Kolom
                angka = i * 3 + j + 1
                btn = tk.Button(
                    button_frame,
                    text=str(angka),
                    font=("Arial", 14),
                    width=5,
                    height=2,
                    # Binding event (klik) ke method input_angka
                    command=lambda n=angka: self.input_angka(n)
                )
                btn.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")

        # Tombol 0
        btn_0 = tk.Button(
            button_frame,
            text="0",
            font=("Arial", 14),
            width=5,
            height=2,
            command=lambda: self.input_angka(0)
        )
        btn_0.grid(row=3, column=1, padx=2, pady=2, sticky="nsew")
        
        # Tombol operator
        operators = ['+', '-', '*', '/']
        for i, op in enumerate(operators):
            btn_op = tk.Button(
                button_frame,
                text=op,
                font=("Arial", 14),
                width=5,
                height=2,
                bg="#FFA500", # Orange
                command=lambda o=op: self.input_operator(o)
            )
            btn_op.grid(row=i, column=3, padx=2, pady=2, sticky="nsew")

        # Tombol sama dengan (=)
        btn_equals = tk.Button(
            button_frame,
            text="=",
            font=("Arial", 14),
            width=5,
            height=2,
            bg="#ADD8E6", # Light Blue
            command=self.hitung_hasil
        )
        btn_equals.grid(row=3, column=2, padx=2, pady=2, sticky="nsew")

        # Tombol clear (C)
        btn_clear = tk.Button(
            button_frame,
            text="C",
            font=("Arial", 14),
            width=5,
            height=2,
            bg="#FF4D4D", # Merah
            fg="white",
            command=self.clear_all
        )
        btn_clear.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")
        
        # Konfigurasi agar tombol menyesuaikan ukuran frame
        for i in range(4): # 4 baris (0-3)
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4): # 4 kolom (0-3)
            button_frame.grid_columnconfigure(j, weight=1)

    # --- EVENT HANDLERS ---
    
    def input_angka(self, angka):
        """Menambahkan angka ke input saat ini."""
        self.current_input += str(angka)
        self.update_display()

    def input_operator(self, op):
        """Memproses operator yang dipilih dan menyimpan angka pertama."""
        if self.current_input:
            try:
                self.first_number = float(self.current_input)
                self.operator = op
                self.current_input = "" # Clear input untuk angka kedua
                self.update_display()
            except ValueError:
                messagebox.showerror("Error", "Input angka tidak valid.")
                self.clear_all()

    def hitung_hasil(self):
        """Menghitung hasil operasi dan menampilkannya."""
        if self.current_input and self.operator:
            try:
                second_number = float(self.current_input)
                result = 0

                if self.operator == '+':
                    result = self.first_number + second_number
                elif self.operator == '-':
                    result = self.first_number - second_number
                elif self.operator == '*':
                    result = self.first_number * second_number
                elif self.operator == '/':
                    if second_number != 0:
                        result = self.first_number / second_number
                    else:
                        messagebox.showerror("Error", "Pembagian dengan nol!")
                        self.clear_all()
                        return

                # Tampilkan hasil
                self.current_input = str(result)
                self.operator = ""
                self.first_number = 0
                self.update_display()

            except ValueError:
                messagebox.showerror("Error", "Input tidak valid!")
                self.clear_all()

    def clear_all(self):
        """Mereset semua state kalkulator."""
        self.current_input = ""
        self.operator = ""
        self.first_number = 0
        self.update_display()

    def update_display(self):
        """Memperbarui tampilan display GUI."""
        # Agar dapat diubah (karena state="readonly")
        self.display.config(state="normal") 
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_input)
        self.display.config(state="readonly") # Kembali ke readonly

    def jalankan(self):
        """Method untuk menjalankan aplikasi GUI."""
        self.window.mainloop()

# --- BLOK UTAMA UNTUK MENJALANKAN KALKULATOR EVENT-DRIVEN ---
if __name__ == "__main__":
    kalkulator = KalkulatorEventDriven()
    kalkulator.jalankan()

