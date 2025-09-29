import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class AnimatedApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Animasi dan Transisi dengan ttk")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')

        # Animation variables
        self.animation_running = False
        self.progress_value = 0
        self.fade_steps = 20  # Jumlah langkah untuk animasi fade

        self._setup_styles()
        self._buat_interface()

    def _setup_styles(self):
        self.style = ttk.Style()

        # Dark theme styles
        self.style.configure('Dark.TFrame',
                           background='#2d2d2d',
                           relief='flat')

        self.style.configure('Dark.TLabel',
                           background='#2d2d2d',
                           foreground='#ffffff',
                           font=('Arial', 11))

        self.style.configure('Title.TLabel',
                           background='#2d2d2d',
                           foreground='#00ff88',
                           font=('Arial', 16, 'bold'))

        self.style.configure('Animated.TButton',
                           background='#00ff88',
                           foreground='#1a1a1a',
                           borderwidth=0,
                           focuscolor='none',
                           padding=(20, 10),
                           font=('Arial', 10, 'bold'))

        self.style.map('Animated.TButton',
                      background=[('active', '#00cc6a'),
                                ('pressed', '#009954')])

    def _buat_interface(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header dengan animasi fade
        self.header_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.header_frame.pack(fill='x', pady=(0,30))

        self.title_label = ttk.Label(self.header_frame, text="🎬 Animation Demo",
                                    style='Title.TLabel')
        self.title_label.pack()

        # Progress animation section
        self.progress_frame = ttk.LabelFrame(self.main_frame, text="Progress Animation", padding="20")
        self.progress_frame.pack(fill='x', pady=(0,20))

        ttk.Label(self.progress_frame, text="Animated Progress Bar:",
                 style='Dark.TLabel').pack(anchor='w', pady=(0,10))

        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate',
                                          length=400, style='TProgressbar')
        self.progress_bar.pack(fill='x', pady=(0,15))

        # Control buttons untuk progress
        progress_controls = ttk.Frame(self.progress_frame, style='Dark.TFrame')
        progress_controls.pack(fill='x')

        ttk.Button(progress_controls, text="Start Animation",
                  style='Animated.TButton', command=self.start_progress_animation).pack(side='left', padx=(0,10))
        ttk.Button(progress_controls, text="Stop Animation",
                  style='Animated.TButton', command=self.stop_animation).pack(side='left', padx=(0,10))
        ttk.Button(progress_controls, text="Reset",
                  style='Animated.TButton', command=self.reset_progress).pack(side='left')

        # Sliding panel animation
        self.slide_frame = ttk.LabelFrame(self.main_frame, text="Sliding Panel", padding="20")
        self.slide_frame.pack(fill='x', pady=(0,20))

        # Container untuk sliding panel
        self.slide_container = ttk.Frame(self.slide_frame, style='Dark.TFrame', height=200)
        self.slide_container.pack(fill='x', pady=(0,15))
        self.slide_container.pack_propagate(False)

        # Panel yang akan slide
        self.sliding_panel = ttk.Frame(self.slide_container, style='Dark.TFrame')
        self.sliding_panel.place(x=-300, y=0, width=300, height=200)

        # Content dalam sliding panel
        panel_content = ttk.Frame(self.sliding_panel, style='Dark.TFrame')
        panel_content.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(panel_content, text="🎯 Sliding Panel Content",
                 style='Title.TLabel').pack()
        ttk.Label(panel_content, text="Panel ini dapat slide masuk dan keluar",
                 style='Dark.TLabel').pack(pady=(10,0))

        # Controls untuk sliding
        slide_controls = ttk.Frame(self.slide_frame, style='Dark.TFrame')
        slide_controls.pack(fill='x')

        ttk.Button(slide_controls, text="Slide In",
                  style='Animated.TButton', command=self.slide_in).pack(side='left', padx=(0,10))
        ttk.Button(slide_controls, text="Slide Out",
                  style='Animated.TButton', command=self.slide_out).pack(side='left')

        # Fade animation section
        self.fade_frame = ttk.LabelFrame(self.main_frame, text="Fade Animation", padding="20")
        self.fade_frame.pack(fill='both', expand=True)
        
        # Content yang akan fade
        # Gunakan tk.Frame agar bisa mengubah background untuk efek "fade"
        self.fade_content = tk.Frame(self.fade_frame, bg='#00ff88') 
        self.fade_content.pack(fill='both', expand=True, pady=(0,15))

        tk.Label(self.fade_content, text="✨ Fade Content",
                 bg='#00ff88', fg='#1a1a1a', font=('Arial', 16, 'bold')).pack(pady=20)
        tk.Label(self.fade_content, text="Content ini dapat fade in/out dengan smooth transition",
                 bg='#00ff88', fg='#1a1a1a', font=('Arial', 11)).pack()

        # Fade controls
        fade_controls = ttk.Frame(self.fade_frame, style='Dark.TFrame')
        fade_controls.pack(fill='x')

        ttk.Button(fade_controls, text="Fade Out",
                  style='Animated.TButton', command=self.start_fade_out).pack(side='left', padx=(0,10))
        ttk.Button(fade_controls, text="Fade In",
                  style='Animated.TButton', command=self.start_fade_in).pack(side='left')

    # Animation methods
    def start_progress_animation(self):
        if not self.animation_running:
            self.animation_running = True
            self._animate_progress()

    def _animate_progress(self):
        if self.animation_running and self.progress_value < 100:
            self.progress_value += 1
            self.progress_bar['value'] = self.progress_value
            self.root.after(50, self._animate_progress)
        elif self.progress_value >= 100:
            self.animation_running = False

    def stop_animation(self):
        self.animation_running = False

    def reset_progress(self):
        self.animation_running = False
        self.progress_value = 0
        self.progress_bar['value'] = 0

    def slide_in(self):
        self._animate_slide(start_x=-300, end_x=0)

    def slide_out(self):
        self._animate_slide(start_x=0, end_x=-300)

    def _animate_slide(self, start_x, end_x, step=0):
        if step > 30:
            return

        current_x = start_x + (end_x - start_x) * (step / 30)
        self.sliding_panel.place(x=current_x, y=0, width=300, height=200)
        
        self.root.after(20, lambda: self._animate_slide(start_x, end_x, step + 1))

    def start_fade_out(self):
        self._animate_fade(step=0, direction=-1)

    def start_fade_in(self):
        self.fade_content.pack(fill='both', expand=True, pady=(0,15))
        self._animate_fade(step=0, direction=1)

    def _animate_fade(self, step, direction):
        if step > self.fade_steps:
            if direction == -1:
                self.fade_content.pack_forget()
            return
        
        # Hitung nilai warna baru untuk simulasi fade
        r_start, g_start, b_start = (0, 255, 136) # #00ff88
        r_end, g_end, b_end = (45, 45, 45) # #2d2d2d (warna background)

        if direction == 1: # Fade In
            r_new = r_end + (r_start - r_end) * (step / self.fade_steps)
            g_new = g_end + (g_start - g_end) * (step / self.fade_steps)
            b_new = b_end + (b_start - b_end) * (step / self.fade_steps)
        else: # Fade Out
            r_new = r_start + (r_end - r_start) * (step / self.fade_steps)
            g_new = g_start + (g_end - g_start) * (step / self.fade_steps)
            b_new = b_start + (b_end - b_start) * (step / self.fade_steps)

        new_color = f'#{int(r_new):02x}{int(g_new):02x}{int(b_new):02x}'
        self.fade_content.configure(bg=new_color)
        
        for child in self.fade_content.winfo_children():
            child.configure(bg=new_color)

        self.root.after(25, lambda: self._animate_fade(step + 1, direction))

    def run(self):
        self.root.mainloop()

# Jalankan aplikasi
if __name__ == "__main__":
    app = AnimatedApp()
    app.run()
