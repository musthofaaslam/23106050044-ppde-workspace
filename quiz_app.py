import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

class QuizApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quiz Interaktif - Tugas Akhir")
        self.window.geometry("700x500")
        self.window.resizable(False, False)
        self.window.configure(bg="#f0f0f0")

        # Data pertanyaan
        self.questions = [
            {
                "question": "Apa itu event-driven programming?",
                "options": ["Program yang berjalan berurutan", "Program yang merespons kejadian", "Program tanpa GUI", "Program berbasis web"],
                "correct_option_index": 1
            },
            {
                "question": "Fungsi apa di Tkinter yang digunakan untuk menjadwalkan eksekusi fungsi setelah penundaan?",
                "options": ["window.wait()", "window.pause()", "window.after()", "window.schedule()"],
                "correct_option_index": 2
            },
            {
                "question": "Variabel apa yang paling cocok untuk menyimpan status ON/OFF di Tkinter?",
                "options": ["tk.StringVar", "tk.DoubleVar", "tk.IntVar", "tk.BooleanVar"],
                "correct_option_index": 3
            },
            {
                "question": "Apa perbedaan utama antara `pack()` dan `grid()` di Tkinter?",
                "options": ["Pack lebih fleksibel dari grid", "Grid bisa menata widget dalam tabel", "Pack lebih cepat dari grid", "Tidak ada perbedaan"],
                "correct_option_index": 1
            },
            {
                "question": "Mana yang bukan merupakan event handling di Tkinter?",
                "options": ["<Button-1>", "<Key-Up>", "<Enter>", "<Mouse-Move>"],
                "correct_option_index": 2
            },
            {
                "question": "Metode mana yang digunakan untuk mengaktifkan kembali tombol yang sebelumnya dinonaktifkan?",
                "options": ["config(state=tk.ENABLED)", "config(state=tk.NORMAL)", "enable()", "activate()"],
                "correct_option_index": 1
            },
            {
                "question": "Apa fungsi dari `trace_add()` pada variabel Tkinter?",
                "options": ["Mencatat riwayat perubahan nilai", "Menghubungkan variabel dengan event handling", "Menampilkan nilai variabel di terminal", "Mengunci nilai variabel agar tidak berubah"],
                "correct_option_index": 1
            },
            {
                "question": "Komponen GUI apa yang cocok untuk menampilkan daftar opsi yang dapat dipilih?",
                "options": ["Label", "Entry", "Button", "Radiobutton"],
                "correct_option_index": 3
            },
            {
                "question": "Apa tujuan dari `self.window.mainloop()`?",
                "options": ["Menutup jendela aplikasi", "Memulai aplikasi web", "Memulai event loop Tkinter", "Mereset semua widget"],
                "correct_option_index": 2
            },
            {
                "question": "Apa yang dilakukan oleh `self.window.destroy()`?",
                "options": ["Mengosongkan jendela", "Menutup jendela dan mengakhiri program", "Menyembunyikan jendela sementara", "Mereset semua widget di jendela"],
                "correct_option_index": 1
            }
        ]
        random.shuffle(self.questions) # Acak urutan pertanyaan

        # State management
        self.current_question_index = 0
        self.score = 0
        self.time_left = 15
        self.timer_job = None
        self.selected_answer = tk.IntVar()
        self.answer_submitted = False

        self.buat_interface()
        self.load_question()
        self.start_timer()
        self.window.bind("<Return>", lambda event: self.submit_answer())
        self.window.bind("<Escape>", lambda event: self.skip_question())

    def buat_interface(self):
        # Frame utama
        main_frame = tk.Frame(self.window, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Area header (skor, progress, timer)
        header_frame = tk.Frame(main_frame, bg="#f0f0f0")
        header_frame.pack(fill="x")

        # Label Skor
        self.score_label = tk.Label(header_frame, text=f"Skor: {self.score}", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333")
        self.score_label.pack(side="left")

        # Timer Countdown
        self.timer_label = tk.Label(header_frame, text=f"Waktu: {self.time_left}s", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#ff0000")
        self.timer_label.pack(side="right")
        
        # Progress Bar
        self.progress_label = tk.Label(main_frame, text=f"Soal {self.current_question_index + 1}/10", font=("Arial", 12), bg="#f0f0f0")
        self.progress_label.pack(pady=(10, 5))
        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=600, mode="determinate", maximum=10)
        self.progress_bar.pack(pady=5)
        self.progress_bar["value"] = self.current_question_index
        
        # Area Pertanyaan
        self.question_label = tk.Label(main_frame, text="", font=("Arial", 16, "bold"), wraplength=600, justify="center", bg="#f0f0f0")
        self.question_label.pack(pady=20)
        
        # Area Opsi Jawaban
        self.options_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.options_frame.pack(pady=10)
        self.radiobuttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.options_frame, text="", variable=self.selected_answer, value=i, font=("Arial", 12), bg="#f0f0f0", command=self.on_option_select)
            self.radiobuttons.append(rb)
            rb.pack(anchor="w", pady=5)
        
        # Area Tombol
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        self.submit_btn = tk.Button(button_frame, text="Submit (Enter)", font=("Arial", 12), command=self.submit_answer, state="disabled")
        self.submit_btn.pack(side="left", padx=10)
        
        self.skip_btn = tk.Button(button_frame, text="Lewati (Esc)", font=("Arial", 12), command=self.skip_question)
        self.skip_btn.pack(side="left", padx=10)

        # Area Feedback (Animasi)
        self.feedback_label = tk.Label(main_frame, text="", font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.feedback_label.pack(pady=10)

    def load_question(self):
        """Memuat pertanyaan dan opsi jawaban saat ini ke antarmuka."""
        if self.current_question_index >= len(self.questions):
            self.show_result()
            return
            
        self.reset_ui()
        
        question_data = self.questions[self.current_question_index]
        self.question_label.config(text=question_data["question"])
        
        # Set opsi jawaban
        for i, option_text in enumerate(question_data["options"]):
            self.radiobuttons[i].config(text=option_text, state="normal")
            
        self.progress_label.config(text=f"Soal {self.current_question_index + 1}/{len(self.questions)}")
        self.progress_bar["value"] = self.current_question_index
        
        # Reset timer dan jalankan
        self.time_left = 15
        self.start_timer()

    def reset_ui(self):
        """Mereset UI untuk soal berikutnya."""
        self.selected_answer.set(-1)
        self.answer_submitted = False
        self.submit_btn.config(state="disabled")
        self.skip_btn.config(state="normal")
        self.feedback_label.config(text="")
        
        for rb in self.radiobuttons:
            rb.config(fg="black")

    def start_timer(self):
        """Memulai timer hitung mundur."""
        if self.timer_job:
            self.window.after_cancel(self.timer_job)
        self.update_timer()

    def update_timer(self):
        """Memperbarui tampilan timer setiap detik."""
        if self.time_left > 0 and not self.answer_submitted:
            self.time_left -= 1
            self.timer_label.config(text=f"Waktu: {self.time_left}s")
            self.timer_job = self.window.after(1000, self.update_timer)
        elif self.time_left == 0 and not self.answer_submitted:
            self.submit_answer()

    def on_option_select(self):
        """Mengaktifkan tombol submit saat opsi dipilih."""
        self.submit_btn.config(state="normal")

    def submit_answer(self):
        """Memvalidasi jawaban yang dipilih, memperbarui skor, dan menampilkan umpan balik."""
        if self.answer_submitted:
            return

        self.answer_submitted = True
        if self.timer_job:
            self.window.after_cancel(self.timer_job)

        user_answer_index = self.selected_answer.get()
        correct_answer_index = self.questions[self.current_question_index]["correct_option_index"]

        # Logika feedback visual
        if user_answer_index == correct_answer_index:
            self.score += 1
            self.score_label.config(text=f"Skor: {self.score}")
            self.feedback_label.config(text="Jawaban Benar!", fg="green")
            self.radiobuttons[user_answer_index].config(fg="green")
        else:
            self.feedback_label.config(text="Jawaban Salah!", fg="red")
            if user_answer_index != -1:
                self.radiobuttons[user_answer_index].config(fg="red")
            self.radiobuttons[correct_answer_index].config(fg="green")

        # Menonaktifkan semua radiobutton dan tombol setelah submit
        self.submit_btn.config(state="disabled")
        self.skip_btn.config(state="disabled")
        for rb in self.radiobuttons:
            rb.config(state="disabled")
            
        # Pindah ke soal berikutnya setelah jeda
        self.window.after(2000, self.next_question)

    def next_question(self):
        """Mempersiapkan dan memuat soal berikutnya."""
        self.current_question_index += 1
        self.progress_bar["value"] = self.current_question_index
        self.load_question()
        
    def skip_question(self):
        """Melewati soal saat ini tanpa poin."""
        if self.answer_submitted:
            return
            
        self.answer_submitted = True
        if self.timer_job:
            self.window.after_cancel(self.timer_job)
        
        correct_answer_index = self.questions[self.current_question_index]["correct_option_index"]
        self.feedback_label.config(text="Soal Dilewati", fg="orange")
        self.radiobuttons[correct_answer_index].config(fg="green")
        
        self.submit_btn.config(state="disabled")
        self.skip_btn.config(state="disabled")
        for rb in self.radiobuttons:
            rb.config(state="disabled")
            
        self.window.after(2000, self.next_question)

    def show_result(self):
        """Menampilkan hasil akhir kuis."""
        messagebox.showinfo("Kuis Selesai", f"Anda telah menyelesaikan kuis!\nSkor akhir Anda adalah {self.score}/{len(self.questions)}")
        self.window.destroy()

    def jalankan(self):
        """Metode untuk menjalankan aplikasi."""
        self.window.mainloop()

if __name__ == "__main__":
    app = QuizApp()
    app.jalankan()
