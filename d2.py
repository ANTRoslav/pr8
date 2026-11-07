import tkinter as tk
from tkinter import messagebox, filedialog
import random


def generate_ewb_file():
    try:
        dt = float(entry_dt.get())
        num_bits = int(entry_bits_count.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте ввод чисел (шаг времени и количество бит).")
        return

    if dt <= 0 or num_bits <= 0:
        messagebox.showerror("Ошибка", "Шаг и количество бит должны быть больше нуля.")
        return

    bits = []
    mode = var_mode.get()

    if mode == "Вручную":
        raw_bits = entry_manual_bits.get().strip().replace(" ", "").replace(",", "")
        if not raw_bits or not all(c in '01' for c in raw_bits):
            messagebox.showerror("Ошибка", "Строка должна содержать только 0 и 1.")
            return
        if len(raw_bits) != num_bits:
            messagebox.showerror("Ошибка", f"Вы указали {num_bits} бит, но ввели {len(raw_bits)}.")
            return
        bits = [int(c) for c in raw_bits]
    else:
        bits = [random.choice([0, 1]) for _ in range(num_bits)]

    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt")],
        title="Сохранить EWB файл как..."
    )
    if not filepath:
        return

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("ASCII output data for Electronics Workbench circuit untitled\n")
            f.write("        Time        V1\n")

            current_time = 0.0
            for bit in bits:
                voltage = 5 if bit == 1 else 0
                f.write(f"     {current_time:.4f}        {voltage}\n")
                current_time += dt

        messagebox.showinfo("Успех", f"Файл EWB успешно создан:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")


# =========================================================
# ИНТЕРФЕЙС (ПЛОТНАЯ КОМПОНОВКА PACK)
# =========================================================
root = tk.Tk()
root.title("Генератор EWB")
root.geometry("400x480")  # Компактный размер
root.configure(bg="#1E1E24")
root.resizable(False, False)

bg_c = "#1E1E24"
fg_c = "#E0E0E0"
accent = "#00E5FF"
entry_bg = "#2C3E50"

font_main = ("Arial", 10)
font_title = ("Arial", 10, "bold")

# Главный контейнер с небольшими отступами
main_frame = tk.Frame(root, bg=bg_c, padx=15, pady=15)
main_frame.pack(fill="both", expand=True)

# --- 1. Параметры ---
tk.Label(main_frame, text="1. Параметры сигнала", font=font_title, bg=bg_c, fg=accent).pack(anchor="w", pady=(0, 10))

# Поля ввода (используем вложенные фреймы, чтобы текст и поле были рядом)
f1 = tk.Frame(main_frame, bg=bg_c)
f1.pack(fill="x", pady=5)
tk.Label(f1, text="Шаг времени (с):", width=16, anchor="w", bg=bg_c, fg=fg_c, font=font_main).pack(side="left")
entry_dt = tk.Entry(f1, font=font_main, bg=entry_bg, fg=fg_c, insertbackground="white", relief="flat")
entry_dt.insert(0, "0.01")
entry_dt.pack(side="left", fill="x", expand=True, ipady=3)

f2 = tk.Frame(main_frame, bg=bg_c)
f2.pack(fill="x", pady=5)
tk.Label(f2, text="Длина (бит):", width=16, anchor="w", bg=bg_c, fg=fg_c, font=font_main).pack(side="left")
entry_bits_count = tk.Entry(f2, font=font_main, bg=entry_bg, fg=fg_c, insertbackground="white", relief="flat")
entry_bits_count.insert(0, "10")
entry_bits_count.pack(side="left", fill="x", expand=True, ipady=3)

# --- 2. Способ формирования ---
tk.Label(main_frame, text="2. Способ формирования", font=font_title, bg=bg_c, fg=accent).pack(anchor="w", pady=(15, 5))

var_mode = tk.StringVar(value="Случайно")
frame_radio = tk.Frame(main_frame, bg=bg_c)
frame_radio.pack(fill="x", pady=5)
tk.Radiobutton(frame_radio, text="Случайно", variable=var_mode, value="Случайно", bg=bg_c, fg=fg_c,
               selectcolor=entry_bg, activebackground=bg_c, activeforeground=accent, font=font_main).pack(side="left",
                                                                                                          padx=(0, 15))
tk.Radiobutton(frame_radio, text="Вручную", variable=var_mode, value="Вручную", bg=bg_c, fg=fg_c, selectcolor=entry_bg,
               activebackground=bg_c, activeforeground=accent, font=font_main).pack(side="left")

f3 = tk.Frame(main_frame, bg=bg_c)
f3.pack(fill="x", pady=5)
tk.Label(f3, text="Биты (0 и 1):", width=16, anchor="w", bg=bg_c, fg=fg_c, font=font_main).pack(side="left")
entry_manual_bits = tk.Entry(f3, font=font_main, bg=entry_bg, fg=fg_c, insertbackground="white", relief="flat")
entry_manual_bits.insert(0, "1010101010")
entry_manual_bits.pack(side="left", fill="x", expand=True, ipady=3)

# --- Кнопка (занимает всю ширину) ---
btn_generate = tk.Button(main_frame, text="СОЗДАТЬ ФАЙЛ EWB", font=("Arial", 12, "bold"),
                         bg="#27AE60", fg="white", activebackground="#2ECC71", activeforeground="white",
                         command=generate_ewb_file, cursor="hand2", relief="flat")
btn_generate.pack(fill="x", pady=(30, 0), ipady=8)

# Запуск
root.mainloop()