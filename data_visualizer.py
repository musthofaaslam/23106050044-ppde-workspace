import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import pandas as pd # Import tambahan
import matplotlib.dates as mdates # Import tambahan
import threading # Import tambahan
import time # Import tambahan
from datetime import datetime, timedelta # Import tambahan

class DataVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Visualizer - Interaktif dan Real-time")
        self.root.geometry("1000x800")
        self.root.configure(bg="white")

        # --- Variabel Kontrol ---
        # Kontrol Fungsi Matematika
        self.frequency = tk.DoubleVar(value=1.0)
        self.amplitude = tk.DoubleVar(value=1.0)
        self.phase = tk.DoubleVar(value=0.0)
        self.function_type = tk.StringVar(value="sin")
        self.line_color = tk.StringVar(value="blue")
        self.line_style = tk.StringVar(value="-")
        self.line_width = tk.DoubleVar(value=2.0)
        
        # Kontrol Data (Praktikum 3.1 - 3.4)
        self.current_data = None
        self.plot_type = tk.StringVar(value="line")
        self.use_subplot = tk.BooleanVar(value=False)
        self.realtime_active = tk.BooleanVar(value=False)
        self.update_speed = tk.IntVar(value=500)
        self.realtime_data = []
        self.max_points = 50

        # --- Setup UI dan Logika ---
        self.setup_ui()
        self.setup_plot()
        self.setup_controls()       # Kontrol Fungsi Matematika (dari praktikum sebelumnya)
        self.setup_data_controls()  # Kontrol Data (Praktikum 3.1 & 3.2)
        self.setup_export_controls()
        self.setup_interactive_features()



    def setup_ui(self):
        """Membuat struktur dasar UI (Control Frame dan Plot Frame)"""
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame Kontrol dengan Scrollbar
        control_canvas = tk.Canvas(main_frame, bg="lightblue", width=250)
        control_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=control_canvas.yview)
        
        control_canvas.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        
        control_canvas.configure(yscrollcommand=control_scrollbar.set)
        control_canvas.bind('<Configure>', lambda e: control_canvas.configure(scrollregion = control_canvas.bbox("all")))
        
        self.control_frame = tk.Frame(control_canvas, bg="lightblue")
        control_canvas.create_window((0, 0), window=self.control_frame, anchor="nw", width=250)
        
        # Frame Plot
        self.plot_frame = tk.Frame(main_frame, bg="white")
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            self.control_frame, 
            text="KONTROL FUNGSI", 
            font=("Arial", 14, "bold"),
            bg="lightblue"
        )
        title_label.pack(pady=20)

    def setup_plot(self):
        """Membuat dan meng-embed plot Matplotlib"""
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()
        
        # Plot awal - Fungsi Sinus default
        self.update_math_plot()

    def setup_controls(self):
        """Menambahkan kontrol Fungsi Matematika (Praktikum 2.x)"""
        # Kontrol Frekuensi
        tk.Label(self.control_frame, text="Frekuensi (ω):", font=("Arial", 12, "bold"), bg="lightblue").pack(pady=(5, 5))
        tk.Scale(self.control_frame, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.frequency, command=self.on_parameter_change, length=200, bg="lightblue").pack(pady=5)
        self.freq_value_label = tk.Label(self.control_frame, text=f"Nilai: {self.frequency.get()}", font=("Arial", 10), bg="lightblue"); self.freq_value_label.pack()

        # Kontrol Amplitudo
        tk.Label(self.control_frame, text="Amplitudo (A):", font=("Arial", 12, "bold"), bg="lightblue").pack(pady=(15, 5))
        tk.Scale(self.control_frame, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.amplitude, command=self.on_parameter_change, length=200, bg="lightblue").pack(pady=5)
        self.amp_value_label = tk.Label(self.control_frame, text=f"Nilai: {self.amplitude.get()}", font=("Arial", 10), bg="lightblue"); self.amp_value_label.pack()

        # Kontrol Phase
        tk.Label(self.control_frame, text="Phase (φ):", font=("Arial", 12, "bold"), bg="lightblue").pack(pady=(15, 5))
        tk.Scale(self.control_frame, from_=0.0, to=6.28, resolution=0.1, orient=tk.HORIZONTAL, variable=self.phase, command=self.on_parameter_change, length=200, bg="lightblue").pack(pady=5)
        self.phase_value_label = tk.Label(self.control_frame, text=f"Nilai: {self.phase.get()}", font=("Arial", 10), bg="lightblue"); self.phase_value_label.pack()
        
        # Pemilihan Jenis Fungsi
        tk.Label(self.control_frame, text="Jenis Fungsi:", font=("Arial", 12, "bold"), bg="lightblue").pack(pady=(20, 5))
        function_combo = ttk.Combobox(self.control_frame, textvariable=self.function_type, values=["sin", "cos", "tan", "exp", "log"], state="readonly", width=18)
        function_combo.pack(pady=5)
        function_combo.bind("<<ComboboxSelected>>", self.on_parameter_change)

        # Pemilihan Warna dan Style
        tk.Label(self.control_frame, text="Warna Garis:", font=("Arial", 12, "bold"), bg="lightblue").pack(pady=(20, 5))
        color_combo = ttk.Combobox(self.control_frame, textvariable=self.line_color, values=["blue", "red", "green", "orange", "purple", "brown", "pink", "black"], state="readonly", width=18)
        color_combo.pack(pady=5)
        color_combo.bind("<<ComboboxSelected>>", self.on_parameter_change)

        tk.Label(self.control_frame, text="Style Garis:", font=("Arial", 12, "bold"), bg="lightblue").pack(pady=(15, 5))
        style_combo = ttk.Combobox(self.control_frame, textvariable=self.line_style, values=["-", "--", "-.", ":", "o-", "s-", "^-"], state="readonly", width=18)
        style_combo.pack(pady=5)
        style_combo.bind("<<ComboboxSelected>>", self.on_parameter_change)

        tk.Label(self.control_frame, text="Ketebalan Garis:", font=("Arial", 12, "bold"), bg="lightblue").pack(pady=(15, 5))
        tk.Scale(self.control_frame, from_=0.5, to=5.0, resolution=0.5, orient=tk.HORIZONTAL, variable=self.line_width, command=self.on_parameter_change, length=200, bg="lightblue").pack(pady=5)

    def setup_data_controls(self):
        """Menambahkan kontrol Data (Praktikum 3.1, 3.2, 3.3, 3.4)"""
        # Separator dan Judul
        separator = tk.Frame(self.control_frame, height=2, bg="darkblue")
        separator.pack(fill=tk.X, pady=20)
        data_label = tk.Label(self.control_frame, text="VISUALISASI DATA", font=("Arial", 14, "bold"), bg="lightblue")
        data_label.pack(pady=10)

        # Button Load/Generate Data (Praktikum 3.1)
        tk.Button(self.control_frame, text="Load Data CSV", font=("Arial", 11, "bold"), command=self.load_data, bg="orange", fg="white", width=20).pack(pady=5)
        tk.Button(self.control_frame, text="Generate Sample Data", font=("Arial", 11), command=self.generate_sample_data, bg="green", fg="white", width=20).pack(pady=5)

        # Info label untuk status data
        self.data_info_label = tk.Label(self.control_frame, text="Belum ada data dimuat", font=("Arial", 9), bg="lightblue", wraplength=200)
        self.data_info_label.pack(pady=10)

        # Pemilihan jenis plot untuk data (Praktikum 3.2)
        tk.Label(self.control_frame, text="Jenis Plot Data:", font=("Arial", 12, "bold"), bg="lightblue").pack(pady=(15, 5))
        plot_type_combo = ttk.Combobox(self.control_frame, textvariable=self.plot_type, values=["line", "scatter", "bar", "histogram", "box"], state="readonly", width=18)
        plot_type_combo.pack(pady=5)
        plot_type_combo.bind("<<ComboboxSelected>>", self.on_plot_type_change)
        
        # Checkbox untuk multiple subplot (Praktikum 3.3)
        self.use_subplot = tk.BooleanVar(value=False)
        subplot_check = tk.Checkbutton(self.control_frame, text="Gunakan Multiple Subplot", variable=self.use_subplot, command=self.toggle_subplot, font=("Arial", 10), bg="lightblue")
        subplot_check.pack(pady=10)

        # Real-time data simulation (Praktikum 3.4)
        separator2 = tk.Frame(self.control_frame, height=1, bg="gray"); separator2.pack(fill=tk.X, pady=10)
        tk.Label(self.control_frame, text="Real-time Simulation:", font=("Arial", 12, "bold"), bg="lightblue").pack(pady=(5, 5))
        self.realtime_btn = tk.Button(self.control_frame, text="Start Real-time", font=("Arial", 11), command=self.toggle_realtime, bg="red", fg="white", width=20)
        self.realtime_btn.pack(pady=5)
        tk.Label(self.control_frame, text="Update Speed (ms):", font=("Arial", 10), bg="lightblue").pack(pady=(10, 2))
        tk.Scale(self.control_frame, from_=100, to=2000, resolution=100, orient=tk.HORIZONTAL, variable=self.update_speed, length=180, bg="lightblue").pack(pady=5)
    
    ## --- Callback untuk Fungsi Matematika ---
    def on_parameter_change(self, value=None):
        """Dipanggil saat kontrol fungsi matematika berubah."""
        # Update label nilai
        self.freq_value_label.config(text=f"Nilai: {round(self.frequency.get(), 2)}")
        self.amp_value_label.config(text=f"Nilai: {round(self.amplitude.get(), 2)}")
        self.phase_value_label.config(text=f"Nilai: {round(self.phase.get(), 2)}")
        
        # Plot hanya jika tidak ada data dimuat atau real-time tidak aktif
        if self.current_data is None and not self.realtime_active.get():
            self.update_math_plot()

    def update_math_plot(self):
        """Plot fungsi matematika (sin, cos, exp, dll)."""
        self.ax.clear()
        
        # Parameter
        x = np.linspace(0, 10, 100)
        freq = self.frequency.get()
        amp = self.amplitude.get()
        phase = self.phase.get()
        func_type = self.function_type.get()
        color = self.line_color.get()
        style = self.line_style.get()
        width = self.line_width.get()

        # Hitung y
        try:
            if func_type == "sin":
                y = amp * np.sin(freq * x + phase)
                title = f"y = {amp} × sin({freq}x + {round(phase, 2)})"
            elif func_type == "cos":
                y = amp * np.cos(freq * x + phase)
                title = f"y = {amp} × cos({freq}x + {round(phase, 2)})"
            elif func_type == "tan":
                y = amp * np.tan(freq * x + phase)
                y = np.clip(y, -10, 10)
                title = f"y = {amp} × tan({freq}x + {round(phase, 2)})"
            elif func_type == "exp":
                y = amp * np.exp(freq * (x - 5) + phase)
                y = np.clip(y, 0, 100)
                title = f"y = {amp} × exp({freq}(x-5) + {round(phase, 2)})"
            elif func_type == "log":
                y = amp * np.log(freq * x + 1) + phase
                title = f"y = {amp} × log({freq}x + 1) + {round(phase, 2)}"
        except:
            y = np.zeros_like(x)
            title = "Error Plotting Function"

        self.ax.plot(x, y, linestyle=style, color=color, linewidth=width)
        self.ax.set_title(title, fontsize=14)
        self.ax.set_xlabel("X", fontsize=12)
        self.ax.set_ylabel("Y", fontsize=12)
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
        
    ## --- Callback dan Logika Data (Praktikum 3.1) ---
    def load_data(self):
        """Memuat data dari file CSV."""
        if self.realtime_active.get():
            self.toggle_realtime() # Stop real-time jika aktif
            
        file_path = filedialog.askopenfilename(title="Pilih file CSV", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            try:
                self.current_data = pd.read_csv(file_path)
                rows, cols = self.current_data.shape
                self.data_info_label.config(text=f"Data dimuat:\n{rows} baris, {cols} kolom\nFile: {file_path.split('/')[-1]}")
                
                # Coba konversi kolom 'Date' pertama menjadi datetime
                date_cols = self.current_data.columns[self.current_data.columns.str.contains('date', case=False)]
                if len(date_cols) > 0:
                    try:
                        self.current_data[date_cols[0]] = pd.to_datetime(self.current_data[date_cols[0]])
                    except:
                        pass # Biarkan jika gagal konversi

                self.plot_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membaca file:\n{str(e)}")

    def generate_sample_data(self):
        """Membuat data sample time series."""
        if self.realtime_active.get():
            self.toggle_realtime() # Stop real-time jika aktif
            
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        trend = np.linspace(100, 200, len(dates))
        seasonal = 30 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
        noise = np.random.normal(0, 15, len(dates))
        sales = trend + seasonal + noise
        temp_base = 25 + 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
        temp_noise = np.random.normal(0, 5, len(dates))
        temperature = temp_base + temp_noise
        
        self.current_data = pd.DataFrame({
            'Date': dates,
            'Sales': sales,
            'Temperature': temperature,
            'Category_A': sales * 0.6 + np.random.normal(0, 10, len(dates)),
            'Category_B': sales * 0.4 + np.random.normal(0, 8, len(dates))
        })

        rows, cols = self.current_data.shape
        self.data_info_label.config(text=f"Sample data dibuat:\n{rows} baris, {cols} kolom\nData penjualan tahunan")
        self.plot_data()

    def plot_data(self):
        """Pintasan ke plot_data_advanced, untuk menjaga konsistensi."""
        self.plot_data_advanced()

    ## --- Logika Plot Data (Praktikum 3.2 & 3.3) ---
    def on_plot_type_change(self, event=None):
        """Dipanggil saat jenis plot data berubah."""
        if self.current_data is not None:
            if self.use_subplot.get():
                 self.setup_subplot()
            else:
                 self.plot_data_advanced()
        else:
            messagebox.showwarning("Peringatan", "Muat data terlebih dahulu!")

    def plot_data_advanced(self):
        """Plot data yang dimuat ke single plot."""
        if self.current_data is None: return
        
        self.ax.clear()

        numeric_columns = self.current_data.select_dtypes(include=[np.number]).columns
        date_columns = self.current_data.select_dtypes(include=['datetime64']).columns
        plot_type = self.plot_type.get()

        if plot_type == "line":
            if len(date_columns) > 0 and len(numeric_columns) > 0:
                # Time Series Line Plot
                date_col = date_columns[0]
                colors = ['blue', 'red', 'green']
                for i, col in enumerate(numeric_columns[:3]):
                    self.ax.plot(self.current_data[date_col], self.current_data[col], color=colors[i % len(colors)], label=col, linewidth=2)
                self.ax.set_xlabel('Tanggal')
                self.ax.set_ylabel('Nilai')
                self.ax.legend()
                # Format tanggal
                self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                self.ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
                plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)
            elif len(numeric_columns) >= 1:
                col = numeric_columns[0]
                self.ax.plot(self.current_data[col], linewidth=2, color='blue')
                self.ax.set_xlabel('Index')
                self.ax.set_ylabel(col)

        elif plot_type == "scatter":
            if len(numeric_columns) >= 2:
                x_col, y_col = numeric_columns[0], numeric_columns[1]
                self.ax.scatter(self.current_data[x_col], self.current_data[y_col], alpha=0.6, s=50, c='blue')
                self.ax.set_xlabel(x_col)
                self.ax.set_ylabel(y_col)

        elif plot_type == "bar":
            if len(numeric_columns) >= 1:
                col = numeric_columns[0]
                data_sample = self.current_data[col].head(20)
                self.ax.bar(range(len(data_sample)), data_sample, color='skyblue')
                self.ax.set_xlabel('Index')
                self.ax.set_ylabel(col)

        elif plot_type == "histogram":
            if len(numeric_columns) >= 1:
                col = numeric_columns[0]
                self.ax.hist(self.current_data[col].dropna(), bins=30, alpha=0.7, color='lightgreen', edgecolor='black')
                self.ax.set_xlabel(col)
                self.ax.set_ylabel('Frekuensi')

        elif plot_type == "box":
            if len(numeric_columns) >= 1:
                data_to_plot = [self.current_data[col].dropna() for col in numeric_columns[:5]]
                labels = numeric_columns[:5].tolist()
                self.ax.boxplot(data_to_plot, labels=labels)
                self.ax.set_ylabel('Nilai')
                plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)

        self.ax.set_title(f'{plot_type.title()} Plot: Data Visualizer')
        self.ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
        self.canvas.draw()
        
    def toggle_subplot(self):
        """Mengganti antara single plot dan multiple subplot (Praktikum 3.3)."""
        if self.current_data is not None:
            if self.realtime_active.get():
                self.toggle_realtime()
                self.use_subplot.set(False)
                messagebox.showinfo("Info", "Simulasi Real-time harus dimatikan untuk menggunakan Subplot.")
                return
            
            self.setup_subplot() if self.use_subplot.get() else self.setup_single_plot()
        else:
            messagebox.showwarning("Peringatan", "Muat data terlebih dahulu!")
            self.use_subplot.set(False)

    def setup_single_plot(self):
        """Mempersiapkan figure untuk satu plot."""
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.plot_data_advanced()

    def setup_subplot(self):
        """Mempersiapkan figure untuk multiple subplot."""
        if self.current_data is None: return
        self.fig.clear()

        numeric_columns = self.current_data.select_dtypes(include=[np.number]).columns
        n_cols = len(numeric_columns)
        n_plots = min(n_cols, 6)

        if n_cols < 2:
            messagebox.showinfo("Info", "Minimal 2 kolom numerik diperlukan untuk subplot")
            self.use_subplot.set(False)
            self.setup_single_plot()
            return

        # Tentukan layout (saran: 2x2 atau 2x3)
        if n_plots <= 2: rows, cols = 1, n_plots
        elif n_plots <= 4: rows, cols = 2, 2
        else: rows, cols = 2, 3

        # Buat subplot
        for i in range(n_plots):
            ax = self.fig.add_subplot(rows, cols, i+1)
            col = numeric_columns[i]
            
            # Plot berbagai jenis untuk setiap subplot
            data_to_plot = self.current_data[col].dropna()

            if i % 4 == 0:  # Line plot
                ax.plot(data_to_plot.values, color='blue', linewidth=1.5)
                ax.set_title(f'Line: {col}', fontsize=10)
            elif i % 4 == 1:  # Histogram
                ax.hist(data_to_plot, bins=20, alpha=0.7, color='green')
                ax.set_title(f'Histogram: {col}', fontsize=10)
            elif i % 4 == 2:  # Box plot
                ax.boxplot(data_to_plot)
                ax.set_title(f'Box: {col}', fontsize=10)
            else:  # Scatter dengan kolom pertama (jika ada)
                if len(numeric_columns) > 1:
                    ax.scatter(self.current_data[numeric_columns[0]], self.current_data[col], alpha=0.6)
                    ax.set_title(f'Scatter: {col} vs {numeric_columns[0]}', fontsize=10)
                else:
                    ax.plot(data_to_plot.values, color='red', linewidth=1.5)
                    ax.set_title(f'Line: {col}', fontsize=10)

            ax.grid(True, alpha=0.3)

        self.fig.tight_layout()
        self.canvas.draw()

    ## --- Logika Real-time (Praktikum 3.4) ---
    def toggle_realtime(self):
        """Memulai atau menghentikan simulasi data real-time."""
        if self.current_data is not None:
             self.current_data = None # Kosongkan data statis
             self.data_info_label.config(text="Real-time data aktif")
        if self.use_subplot.get():
             self.use_subplot.set(False)
             self.setup_single_plot() # Kembali ke single plot jika subplot aktif
             
        if not self.realtime_active.get():
            # Start real-time
            self.realtime_active.set(True)
            self.realtime_btn.config(text="Stop Real-time", bg="green")
            self.realtime_data = [] # Reset data
            self.start_realtime_thread()
        else:
            # Stop real-time
            self.realtime_active.set(False)
            self.realtime_btn.config(text="Start Real-time", bg="red")
            self.data_info_label.config(text="Belum ada data dimuat")
            self.update_math_plot() # Kembali ke plot fungsi matematika

    def start_realtime_thread(self):
        """Membuat thread untuk menghasilkan data baru."""
        def update_loop():
            timestamp_counter = 0
            while self.realtime_active.get():
                # Generate new data point
                value1 = 50 + 20 * np.sin(timestamp_counter * 0.1) + np.random.normal(0, 5)
                value2 = 30 + 15 * np.cos(timestamp_counter * 0.15) + np.random.normal(0, 3)
                value3 = 40 + 10 * np.sin(timestamp_counter * 0.08) + np.random.normal(0, 4)

                self.realtime_data.append({
                    'timestamp': timestamp_counter,
                    'sensor1': value1,
                    'sensor2': value2,
                    'sensor3': value3
                })

                # Keep only last max_points
                if len(self.realtime_data) > self.max_points:
                    self.realtime_data.pop(0)

                # Update plot in main thread
                self.root.after(0, self.update_realtime_plot)
                
                timestamp_counter += 1

                # Sleep based on update speed
                time.sleep(self.update_speed.get() / 1000.0)

        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()

    def update_realtime_plot(self):
        """Menggambar ulang plot dengan data real-time terbaru."""
        if not self.realtime_data or not self.realtime_active.get():
            return

        timestamps = [d['timestamp'] for d in self.realtime_data]
        sensor1 = [d['sensor1'] for d in self.realtime_data]
        sensor2 = [d['sensor2'] for d in self.realtime_data]
        sensor3 = [d['sensor3'] for d in self.realtime_data]

        if hasattr(self, 'ax'):
            self.ax.clear()
            self.ax.plot(timestamps, sensor1, 'b-', label='Sensor 1', linewidth=2)
            self.ax.plot(timestamps, sensor2, 'r-', label='Sensor 2', linewidth=2)
            self.ax.plot(timestamps, sensor3, 'g-', label='Sensor 3', linewidth=2)

            self.ax.set_title('Real-time Sensor Data')
            self.ax.set_xlabel('Time Index')
            self.ax.set_ylabel('Value')
            self.ax.legend(loc='upper left')
            self.ax.grid(True, alpha=0.3)

            # Set axis limits for smooth scrolling effect
            if len(timestamps) > 10:
                self.ax.set_xlim(timestamps[0], timestamps[-1])

            self.canvas.draw()
    def setup_export_controls(self):
        # Separator
        export_separator = tk.Frame(self.control_frame, height=2, bg="darkblue")
        export_separator.pack(fill=tk.X, pady=20)

        # Export section label
        export_label = tk.Label(
            self.control_frame, 
            text="EXPORT & SAVE", 
            font=("Arial", 14, "bold"),
            bg="lightblue"
        )
        export_label.pack(pady=10)

        # Save plot button
        save_btn = tk.Button(
            self.control_frame,
            text="Save Plot",
            font=("Arial", 11, "bold"),
            command=self.save_plot,
            bg="purple",
            fg="white",
            width=20
        )
        save_btn.pack(pady=5)

        # Export format
        format_label = tk.Label(
            self.control_frame, 
            text="Format:", 
            font=("Arial", 10),
            bg="lightblue"
        )
        format_label.pack(pady=(10, 2))

        self.export_format = tk.StringVar(value="png")
        format_combo = ttk.Combobox(
            self.control_frame,
            textvariable=self.export_format,
            values=["png", "jpg", "pdf", "svg", "eps"],
            state="readonly",
            width=18
        )
        format_combo.pack(pady=5)

        # DPI setting
        dpi_label = tk.Label(
            self.control_frame, 
            text="Resolusi (DPI):", 
            font=("Arial", 10),
            bg="lightblue"
        )
        dpi_label.pack(pady=(10, 2))

        self.dpi_setting = tk.IntVar(value=300)
        dpi_scale = tk.Scale(
            self.control_frame,
            from_=100,
            to=600,
            resolution=50,
            orient=tk.HORIZONTAL,
            variable=self.dpi_setting,
            length=180,
            bg="lightblue"
        )
        dpi_scale.pack(pady=5)
        
        # Export data button
        export_data_btn = tk.Button(
            self.control_frame,
            text="Export Data CSV",
            font=("Arial", 11),
            command=self.export_data_csv,
            bg="brown",
            fg="white",
            width=20
        )
        export_data_btn.pack(pady=5)


    def save_plot(self):
        format_ext = self.export_format.get()
        dpi = self.dpi_setting.get()

        # File dialog untuk save
        file_path = filedialog.asksaveasfilename(
            title="Simpan Plot",
            defaultextension=f".{format_ext}",
            filetypes=[
                (f"{format_ext.upper()} files", f"*.{format_ext}"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                # Simpan dengan DPI yang dipilih
                self.fig.savefig(
                    file_path, 
                    dpi=dpi, 
                    bbox_inches='tight',
                    facecolor='white',
                    edgecolor='none'
                )
                messagebox.showinfo(
                    "Berhasil", 
                    f"Plot berhasil disimpan ke:\n{file_path}\nResolusi: {dpi} DPI"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan plot:\n{str(e)}")

    def export_data_csv(self):
        if self.current_data is None:
            messagebox.showwarning("Peringatan", "Tidak ada data untuk diekspor!")
            return

        file_path = filedialog.asksaveasfilename(
            title="Export Data ke CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            try:
                self.current_data.to_csv(file_path, index=False)
                messagebox.showinfo(
                    "Berhasil", 
                    f"Data berhasil diekspor ke:\n{file_path}"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengekspor data:\n{str(e)}")

    def setup_interactive_features(self):
        # Enable interactive mode
        self.annotations = []
        self.interactive_mode = tk.BooleanVar(value=False)

        # Interactive checkbox
        interactive_check = tk.Checkbutton(
            self.control_frame,
            text="Mode Interaktif (Click to Annotate)",
            variable=self.interactive_mode,
            command=self.toggle_interactive,
            font=("Arial", 10),
            bg="lightblue",
            wraplength=200
        )
        interactive_check.pack(pady=10)

        # Clear annotations button
        clear_btn = tk.Button(
            self.control_frame,
            text="Clear Annotations",
            font=("Arial", 10),
            command=self.clear_annotations,
            bg="gray",
            fg="white",
            width=20
        )
        clear_btn.pack(pady=5)

    def toggle_interactive(self):
        if self.interactive_mode.get():
            # Connect click event
            self.click_cid = self.canvas.mpl_connect('button_press_event', self.on_plot_click)
        else:
            # Disconnect click event
            if hasattr(self, 'click_cid'):
                self.canvas.mpl_disconnect(self.click_cid)

    def on_plot_click(self, event):
        if not self.interactive_mode.get() or event.inaxes != self.ax:
            return

        # Get click coordinates
        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return

        # Create annotation
        annotation_text = f'({x:.2f}, {y:.2f})'
        annotation = self.ax.annotate(
            annotation_text,
            xy=(x, y),
            xytext=(10, 10),
            textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
        )

        # Store annotation for later removal
        self.annotations.append(annotation)

        # Redraw canvas
        self.canvas.draw()

    def clear_annotations(self):
        # Remove all annotations
        for annotation in self.annotations:
            annotation.remove()
        self.annotations = []
        self.canvas.draw()
    def setup_theme_controls(self):
        # Theme section
        theme_label = tk.Label(
            self.control_frame, 
            text="TEMA & STYLE", 
            font=("Arial", 14, "bold"),
            bg="lightblue"
        )
        theme_label.pack(pady=(20, 10))

        # Plot style
        style_label = tk.Label(
            self.control_frame, 
            text="Plot Style:", 
            font=("Arial", 10),
            bg="lightblue"
        )
        style_label.pack(pady=(5, 2))

        self.plot_style = tk.StringVar(value="default")
        style_combo = ttk.Combobox(
            self.control_frame,
            textvariable=self.plot_style,
            values=["default", "ggplot", "seaborn", "classic", "dark_background"],
            state="readonly",
            width=18
        )
        style_combo.pack(pady=5)
        style_combo.bind("<<ComboboxSelected>>", self.on_style_change)

        # Color scheme
        color_scheme_label = tk.Label(
            self.control_frame, 
            text="Color Scheme:", 
            font=("Arial", 10),
            bg="lightblue"
        )
        color_scheme_label.pack(pady=(10, 2))

        self.color_scheme = tk.StringVar(value="default")
        color_combo = ttk.Combobox(
            self.control_frame,
            textvariable=self.color_scheme,
            values=["default", "viridis", "plasma", "inferno", "cool", "warm"],
            state="readonly",
            width=18
        )
        color_combo.pack(pady=5)
        color_combo.bind("<<ComboboxSelected>>", self.on_color_scheme_change)

        # Grid style
        self.show_grid = tk.BooleanVar(value=True)
        grid_check = tk.Checkbutton(
            self.control_frame,
            text="Show Grid",
            variable=self.show_grid,
            command=self.update_grid,
            font=("Arial", 10),
            bg="lightblue"
        )
        grid_check.pack(pady=5)

    def on_style_change(self, event=None):
        style = self.plot_style.get()
        try:
            plt.style.use(style)
            # Replot to apply new style
            if hasattr(self, 'current_data') and self.current_data is not None:
                self.plot_data_advanced()
            else:
                self.update_plot()
        except:
            messagebox.showerror("Error", f"Style '{style}' tidak tersedia")
            self.plot_style.set("default")
            plt.style.use("default")

    def on_color_scheme_change(self, event=None):
        # This will be applied in next plot update
        if hasattr(self, 'current_data') and self.current_data is not None:
            self.plot_data_advanced()
        else:
            self.update_plot()

    def update_grid(self):
        if hasattr(self, 'ax'):
            self.ax.grid(self.show_grid.get(), alpha=0.3)
            self.canvas.draw()

    # Update plot methods to use color scheme
    def get_colors(self, n_colors):
        scheme = self.color_scheme.get()
        if scheme == "default":
            return ['blue', 'red', 'green', 'orange', 'purple', 'brown'][:n_colors]
        else:
            try:
                cmap = plt.cm.get_cmap(scheme)
                return [cmap(i / max(1, n_colors - 1)) for i in range(n_colors)]
            except:
                return ['blue', 'red', 'green', 'orange', 'purple', 'brown'][:n_colors]



# Membuat dan menjalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizer(root)
    root.mainloop()