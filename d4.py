import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import sounddevice as sd
import soundfile as sf
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import queue


# =========================================================
# КЛАСС ГЕНЕРАТОРА ЗВУКА
# =========================================================
class SoundGenerator:
    def __init__(self):
        self.fs = 44100  # Частота дискретизации
        self.freq = 440.0  # Частота сигнала (Гц)
        self.amp = 0.5  # Амплитуда (0.0 - 1.0)
        self.wave_type = 'sine'
        self.is_playing = False
        self.pulse_mode = False  # Режим пакетов импульсов
        self.stream = None

    def generate_audio(self, frame):
        t = np.arange(frame, dtype=np.float32) / self.fs

        if self.wave_type == 'sine':
            wave = np.sin(2 * np.pi * self.freq * t)
        elif self.wave_type == 'square':
            wave = np.sign(np.sin(2 * np.pi * self.freq * t))
        elif self.wave_type == 'sawtooth':
            wave = 2 * (t * self.freq - np.floor(0.5 + t * self.freq))
        elif self.wave_type == 'triangle':
            wave = 2 * np.abs(2 * (t * self.freq - np.floor(0.5 + t * self.freq))) - 1
        else:
            wave = np.sin(2 * np.pi * self.freq * t)

        # Режим пакетов импульсов (например, 0.5 сек звук, 0.5 сек тишина)
        if self.pulse_mode:
            cycle_time = t % 1.0  # Период пакета 1 секунда
            envelope = np.where(cycle_time < 0.5, 1.0, 0.0)
            wave = wave * envelope

        return (wave * self.amp).astype(np.float32)

    def start(self):
        if not self.is_playing:
            self.is_playing = True
            self.stream = sd.OutputStream(callback=self.callback, channels=1, samplerate=self.fs)
            self.stream.start()

    def stop(self):
        if self.is_playing:
            self.is_playing = False
            if self.stream:
                self.stream.stop()
                self.stream.close()

    def callback(self, outdata, frames, time, status):
        if status:
            print(status)
        outdata[:] = self.generate_audio(frames).reshape(-1, 1)


gen = SoundGenerator()

# =========================================================
# ИНТЕРФЕЙС (TKINTER)
# =========================================================
root = tk.Tk()
root.title("Звуковая студия (Генератор + Осциллограф)")
root.geometry("1100x700")
root.configure(bg="#1E1E24")

# --- ЛЕВАЯ ПАНЕЛЬ УПРАВЛЕНИЯ ---
left_frame = tk.Frame(root, bg="#1E1E24", width=300, padx=15, pady=15)
left_frame.pack(side="left", fill="y")

# 1. Генератор
tk.Label(left_frame, text="1. Генератор сигналов", font=("Arial", 12, "bold"), bg="#1E1E24", fg="#00E5FF").pack(
    anchor="w", pady=(0, 10))

# Частота
tk.Label(left_frame, text="Частота (Гц):", bg="#1E1E24", fg="#E0E0E0").pack(anchor="w")
slider_freq = tk.Scale(left_frame, from_=20, to=2000, orient="horizontal", bg="#2C3E50", fg="white",
                       highlightthickness=0)
slider_freq.set(440)
slider_freq.pack(fill="x", pady=5)

# Амплитуда
tk.Label(left_frame, text="Амплитуда (0-1):", bg="#1E1E24", fg="#E0E0E0").pack(anchor="w")
slider_amp = tk.Scale(left_frame, from_=0, to=1, resolution=0.05, orient="horizontal", bg="#2C3E50", fg="white",
                      highlightthickness=0)
slider_amp.set(0.5)
slider_amp.pack(fill="x", pady=5)

# Форма волны
tk.Label(left_frame, text="Форма волны:", bg="#1E1E24", fg="#E0E0E0").pack(anchor="w")
var_wave = tk.StringVar(value="sine")
waves = [("Синус", "sine"), ("Меандр", "square"), ("Пила", "sawtooth"), ("Треугольник", "triangle")]
for text, val in waves:
    tk.Radiobutton(left_frame, text=text, variable=var_wave, value=val, bg="#1E1E24", fg="#E0E0E0",
                   selectcolor="#2C3E50").pack(anchor="w")

# Пакеты импульсов
var_pulse = tk.BooleanVar(value=False)
tk.Checkbutton(left_frame, text="Пакеты импульсов (0.5с/0.5с)", variable=var_pulse, bg="#1E1E24", fg="#E0E0E0",
               selectcolor="#2C3E50").pack(anchor="w", pady=10)


# Кнопки управления генератором
def update_gen_params(val=None):
    gen.freq = slider_freq.get()
    gen.amp = slider_amp.get()
    gen.wave_type = var_wave.get()
    gen.pulse_mode = var_pulse.get()


slider_freq.config(command=update_gen_params)
slider_amp.config(command=update_gen_params)
var_wave.trace("w", lambda *args: update_gen_params())
var_pulse.trace("w", lambda *args: update_gen_params())

btn_play = tk.Button(left_frame, text="ИГРАТЬ", bg="#27AE60", fg="white", font=("Arial", 10, "bold"),
                     command=lambda: (update_gen_params(), gen.start()))
btn_play.pack(fill="x", pady=5)
btn_stop = tk.Button(left_frame, text="СТОП", bg="#E74C3C", fg="white", font=("Arial", 10, "bold"), command=gen.stop)
btn_stop.pack(fill="x", pady=5)

# 2. Запись и Воспроизведение
tk.Label(left_frame, text="2. Запись и Воспроизведение", font=("Arial", 12, "bold"), bg="#1E1E24", fg="#00E5FF").pack(
    anchor="w", pady=(20, 10))


def record_audio():
    duration = 5  # Секунд
    messagebox.showinfo("Запись", f"Запись {duration} секунд... Говорите!")
    fs = 44100
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    filepath = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV файл", "*.wav")])
    if filepath:
        sf.write(filepath, recording, fs)
        messagebox.showinfo("Успех", "Запись сохранена!")


def play_file():
    filepath = filedialog.askopenfilename(filetypes=[("WAV файл", "*.wav")])
    if filepath:
        data, fs = sf.read(filepath, dtype='float32')
        sd.play(data, fs)


tk.Button(left_frame, text="ЗАПИСАТЬ (5 сек)", bg="#3498DB", fg="white", font=("Arial", 10, "bold"),
          command=record_audio).pack(fill="x", pady=5)
tk.Button(left_frame, text="ВОСПРОИЗВЕСТИ WAV", bg="#9B59B6", fg="white", font=("Arial", 10, "bold"),
          command=play_file).pack(fill="x", pady=5)

# 3. Онлайн-радио (заглушка, так как BASS требует DLL)
tk.Label(left_frame, text="3. Онлайн-радио", font=("Arial", 12, "bold"), bg="#1E1E24", fg="#00E5FF").pack(anchor="w",
                                                                                                          pady=(20, 10))
tk.Label(left_frame, text="(Требуется библиотека BASS)\nВ Python используйте VLC или Pygame", bg="#1E1E24",
         fg="#888888", font=("Arial", 8)).pack(anchor="w")

# --- ПРАВАЯ ПАНЕЛЬ (ВИЗУАЛИЗАЦИЯ) ---
right_frame = tk.Frame(root, bg="#1E1E24")
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

fig, (ax_osc, ax_spec) = plt.subplots(2, 1, figsize=(8, 6))
fig.patch.set_facecolor('#1E1E24')

ax_osc.set_facecolor('#121212')
ax_osc.set_title("Осциллограмма (Форма волны)", color="white")
ax_osc.set_ylim(-1.1, 1.1)
ax_osc.grid(True, color='#333333')

ax_spec.set_facecolor('#121212')
ax_spec.set_title("Спектр (Спектроанализатор)", color="white")
ax_spec.set_xlim(0, 2000)
ax_spec.set_ylim(0, 0.1)
ax_spec.grid(True, color='#333333')

line_osc, = ax_osc.plot([], [], color="#00E5FF", lw=1.5)
line_spec, = ax_spec.plot([], [], color="#FF4A4A", lw=1.5)

canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)


# --- ПОТОК ОБНОВЛЕНИЯ ГРАФИКОВ ---
def update_plots():
    if gen.is_playing:
        # Генерируем кусок звука для отображения
        t = np.linspace(0, 0.05, 1024)  # 50 мс
        wave = gen.generate_audio(1024)

        # Осциллограмма
        line_osc.set_data(t, wave)

        # Спектр (БПФ)
        fft_val = np.abs(np.fft.rfft(wave))
        fft_freq = np.fft.rfftfreq(len(wave), 1 / gen.fs)
        line_spec.set_data(fft_freq, fft_val)

        # Автомасштабирование графика спектра
        if max(fft_val) > 0:
            ax_spec.set_ylim(0, max(fft_val) * 1.1)

        canvas.draw()
    root.after(50, update_plots)  # Обновляем каждые 50 мс


update_plots()  # Запуск потока отрисовки
root.mainloop()