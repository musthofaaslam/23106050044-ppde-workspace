import tkinter as tk
import math
import time

class StopwatchApp:
    """
    Aplikasi Stopwatch lengkap dengan tampilan waktu digital, 
    kontrol Start/Stop/Reset/Lap, dan animasi jam analog di Canvas.
    """
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Stopwatch dengan Animasi")
        self.window.geometry("600x650") # Ukuran disesuaikan agar lap times terlihat
        self.window.configure(bg="black")

        # Variabel State Stopwatch
        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False
        self.timer_job = None
        
        # Variabel State Lap Times
        self.lap_times = []
        self.lap_count = 0

        # Variabel State Animasi
        self.animation_job = None
        self.rotation_angle = 0

        self.buat_interface()
        self.start_animation() # Mulai animasi latar belakang secara terpisah

    def buat_interface(self):
        """Membuat dan menata semua komponen GUI."""
        
        # --- 1. DISPLAY WAKTU (Digital) ---
        time_frame = tk.Frame(self.window, bg="black")
        time_frame.pack(pady=20)

        # Waktu (HH:MM:SS)
        self.time_label = tk.Label(
            time_frame,
            text="00:00:00",
            font=("Digital-7", 48, "bold"),
            fg="lime",
            bg="black"
        )
        self.time_label.pack()

        # Milidetik (MS)
        self.ms_label = tk.Label(
            time_frame,
            text="000",
            font=("Digital-7", 24),
            fg="yellow",
            bg="black"
        )
        self.ms_label.pack()

        # --- 2. CANVAS ANIMASI (Jam Analog) ---
        self.canvas = tk.Canvas(
            self.window,
            width=300,
            height=300,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack(pady=20)

        # Gambar lingkaran luar (static/animasi border)
        self.canvas.create_oval(
            50, 50, 250, 250,
            outline="white",
            width=3,
            tags="outer_circle"
        )

        # Jarum detik (akan diupdate)
        self.jarum_detik = self.canvas.create_line(
            150, 150, 150, 70,
            fill="red",
            width=3,
            tags="second_hand"
        )

        # Titik tengah
        self.canvas.create_oval(
            145, 145, 155, 155,
            fill="white",
            outline="white"
        )
        
        # Penanda waktu (detik/menit)
        self.buat_penanda_waktu()

        # --- 3. KONTROL TOMBOL ---
        control_frame = tk.Frame(self.window, bg="black")
        control_frame.pack(pady=20)

        self.start_stop_btn = tk.Button(
            control_frame,
            text="START",
            font=("Arial", 14, "bold"),
            bg="green",
            fg="white",
            width=10,
            command=self.toggle_stopwatch
        )
        self.start_stop_btn.pack(side=tk.LEFT, padx=10)

        self.reset_btn = tk.Button(
            control_frame,
            text="RESET",
            font=("Arial", 14, "bold"),
            bg="red",
            fg="white",
            width=10,
            command=self.reset_stopwatch
        )
        self.reset_btn.pack(side=tk.LEFT, padx=10)

        self.lap_btn = tk.Button(
            control_frame,
            text="LAP",
            font=("Arial", 14, "bold"),
            bg="blue",
            fg="white",
            width=10,
            command=self.record_lap,
            state=tk.DISABLED # Lap hanya aktif saat stopwatch berjalan
        )
        self.lap_btn.pack(side=tk.LEFT, padx=10)

        # --- 4. AREA LAP TIMES ---
        lap_frame = tk.LabelFrame(
            self.window,
            text="Lap Times",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="black"
        )
        lap_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.lap_listbox = tk.Listbox(
            lap_frame,
            font=("Courier", 11),
            bg="black",
            fg="lime",
            selectbackground="gray",
            height=5 # Batasan tinggi awal
        )
        self.lap_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    # --- UTILITY DAN ANIMASI CANVAS ---

    def buat_penanda_waktu(self):
        """Membuat penanda waktu di sekeliling lingkaran"""
        center_x, center_y = 150, 150
        radius = 90

        for i in range(60):
            # Sudut dalam radian, disesuaikan agar 0 detik ada di atas
            angle = math.radians(i * 6 - 90)

            if i % 5 == 0:  # Penanda jam (lebih panjang dan tebal)
                inner_radius = radius - 15
                width = 3
                color = "white"
            else:  # Penanda detik
                inner_radius = radius - 8
                width = 1
                color = "gray"

            # Hitung koordinat titik luar (x1, y1)
            x1 = center_x + radius * math.cos(angle)
            y1 = center_y + radius * math.sin(angle)

            # Hitung koordinat titik dalam (x2, y2)
            x2 = center_x + inner_radius * math.cos(angle)
            y2 = center_y + inner_radius * math.sin(angle)

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=width
            )

    def update_second_hand(self, seconds):
        """Update posisi jarum detik (jarum) berdasarkan waktu yang berlalu."""
        # Setiap detik adalah 6 derajat (360/60)
        angle = math.radians(seconds * 6 - 90)

        center_x, center_y = 150, 150
        length = 70

        end_x = center_x + length * math.cos(angle)
        end_y = center_y + length * math.sin(angle)

        # Update koordinat jarum
        self.canvas.coords(
            self.jarum_detik,
            center_x, center_y,
            end_x, end_y
        )
        
    def start_animation(self):
        """Memulai loop animasi latar belakang yang berjalan independen dari stopwatch."""
        self.animate_background()

    def animate_background(self):
        """Animasi latar belakang (warna border yang berkedip)."""
        self.rotation_angle = (self.rotation_angle + 1) % 360

        # Animasi warna berkedip saat berjalan (merah)
        if self.is_running:
            # Menggunakan fungsi sinus untuk perubahan warna yang halus
            brightness = int(127 + 127 * math.sin(math.radians(self.rotation_angle * 4)))
            color = f"#{brightness:02x}0000" 
        else:
            color = "white" # Warna solid saat berhenti

        self.canvas.itemconfig("outer_circle", outline=color)

        # Schedule frame animasi berikutnya (setiap 50ms)
        self.animation_job = self.window.after(50, self.animate_background)

    # --- FUNGSI UTAMA STOPWATCH ---

    def toggle_stopwatch(self):
        """Toggle (Start/Stop) stopwatch."""
        if not self.is_running:
            self.start_stopwatch()
        else:
            self.stop_stopwatch()

    def start_stopwatch(self):
        """Mulai stopwatch."""
        self.is_running = True
        # Atur start_time dari waktu saat ini dikurangi waktu yang sudah berlalu
        self.start_time = time.time() - self.elapsed_time

        # Update tampilan tombol
        self.start_stop_btn.config(text="STOP", bg="red")
        self.lap_btn.config(state=tk.NORMAL)

        # Mulai loop timer
        self.update_time()

    def stop_stopwatch(self):
        """Hentikan stopwatch."""
        self.is_running = False

        # Update tampilan tombol
        self.start_stop_btn.config(text="START", bg="green")
        self.lap_btn.config(state=tk.DISABLED)

        # Hentikan loop timer
        if self.timer_job:
            self.window.after_cancel(self.timer_job)

    def reset_stopwatch(self):
        """Reset semua variabel dan tampilan."""
        self.stop_stopwatch()
        self.elapsed_time = 0

        # Reset tampilan waktu
        self.time_label.config(text="00:00:00")
        self.ms_label.config(text="000")

        # Reset lap times
        self.lap_times.clear()
        self.lap_count = 0
        self.lap_listbox.delete(0, tk.END)

        # Reset jarum detik ke posisi atas
        self.update_second_hand(0)

    def record_lap(self):
        """Catat dan tampilkan waktu putaran (lap time)."""
        if self.is_running:
            self.lap_count += 1
            current_total_time = self.elapsed_time

            # Hitung waktu lap (selisih waktu total saat ini dengan lap terakhir)
            if self.lap_times:
                # lap_times[-1][1] adalah waktu total pada lap sebelumnya
                lap_time = current_total_time - self.lap_times[-1][1]
            else:
                # Lap pertama sama dengan waktu total saat itu
                lap_time = current_total_time

            # Simpan data lap: (Nomor Lap, Waktu Total, Waktu Lap)
            self.lap_times.append((self.lap_count, current_total_time, lap_time))

            # Format dan tampilkan di listbox
            total_formatted = self.format_time(current_total_time)
            lap_formatted = self.format_time(lap_time)

            lap_text = f"Lap {self.lap_count:2d}: {lap_formatted} (Total: {total_formatted})"
            self.lap_listbox.insert(tk.END, lap_text)

            # Scroll ke item lap terbaru
            self.lap_listbox.see(tk.END)

    def update_time(self):
        """Loop utama untuk update waktu setiap 10ms."""
        if self.is_running:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time

            # Update waktu digital (HH:MM:SS)
            time_str = self.format_time(self.elapsed_time)
            self.time_label.config(text=time_str)

            # Update milidetik
            ms = int((self.elapsed_time % 1) * 1000)
            self.ms_label.config(text=f"{ms:03d}")

            # Update jarum detik (animasi analog)
            seconds = self.elapsed_time % 60
            self.update_second_hand(seconds)

            # Schedule pembaruan berikutnya dalam 10 milidetik
            self.timer_job = self.window.after(10, self.update_time)

    def format_time(self, seconds):
        """Format waktu detik (float) ke string HH:MM:SS."""
        seconds = int(seconds) # Ambil bagian integer untuk HH:MM:SS
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def jalankan(self):
        """Method untuk menjalankan aplikasi."""
        self.window.mainloop()

# --- JALANKAN APLIKASI ---
if __name__ == "__main__":
    app = StopwatchApp()
    app.jalankan()