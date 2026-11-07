import tkinter as tk
from tkinter import messagebox, filedialog
import random
import math


# =========================================================
# ЛОГИКА ПРИЛОЖЕНИЯ
# =========================================================
def generate_file():
    user_text = text_input.get("1.0", tk.END).strip()

    try:
        num_count = int(entry_numbers.get())
        math_start = float(entry_math_start.get())
        math_end = float(entry_math_end.get())
        math_step = float(entry_math_step.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте правильность ввода чисел!\nВводите только цифры.")
        return

    if num_count < 0 or math_step <= 0 or math_start >= math_end:
        messagebox.showerror("Ошибка", "Некорректные параметры!\nШаг должен быть > 0, а начало < конца.")
        return

    func_name = var_func.get()

    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt")],
        title="Сохранить файл как..."
    )

    if not filepath:
        return

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write("ОТЧЕТ О ГЕНЕРАЦИИ ДАННЫХ\n")
            f.write("=" * 50 + "\n\n")

            f.write("1. ПРОИЗВОЛЬНЫЙ ТЕКСТ:\n")
            f.write(user_text + "\n\n")

            f.write(f"2. МАССИВ СЛУЧАЙНЫХ ЧИСЕЛ (Количество: {num_count}):\n")
            random_numbers = [random.randint(1, 100) for _ in range(num_count)]
            for i in range(0, len(random_numbers), 10):
                chunk = random_numbers[i:i + 10]
                f.write(" ".join(str(x).rjust(3) for x in chunk) + "\n")
            f.write("\n")

            f.write(f"3. МАССИВ ЗНАЧЕНИЙ ФУНКЦИИ ({func_name}):\n")
            f.write(f"Диапазон: от {math_start} до {math_end}, шаг {math_step}\n")

            x = math_start
            while x <= math_end + 1e-9:
                if func_name == "sin(x)":
                    y = math.sin(x)
                elif func_name == "cos(x)":
                    y = math.cos(x)
                elif func_name == "exp(x)":
                    y = math.exp(x)
                elif func_name == "x^2":
                    y = x ** 2
                f.write(f"x = {x:6.2f}  |  y = {y:8.4f}\n")
                x += math_step

            f.write("\n" + "=" * 50 + "\n")
            f.write("Успешно сгенерировано приложением.\n")

        messagebox.showinfo("Успех", f"Файл успешно создан и сохранен:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить:\n{e}")


# =========================================================
# НАСТРОЙКА ИНТЕРФЕЙСА (ПЛОТНАЯ КОМПОНОВКА)
# =========================================================
root = tk.Tk()
root.title("Генератор данных")
root.geometry("450x480")  # Уменьшили окно, чтобы не было пустоты
root.configure(bg="#1E1E24")
root.resizable(False, False)  # Запрещаем растягивать (чтобы не было пустот)

# Цвета
bg_c = "#1E1E24"
fg_c = "#E0E0E0"
accent = "#00E5FF"
entry_bg = "#2C3E50"

font_main = ("Arial", 10)
font_bold = ("Arial", 10, "bold")
font_title = ("Arial", 11, "bold")

# --- Главный контейнер с отступами ---
main_frame = tk.Frame(root, bg=bg_c, padx=20, pady=15)
main_frame.pack(fill="both", expand=True)

# =========================================================
# БЛОК 1: Текст
# =========================================================
tk.Label(main_frame, text="1. Произвольный текст:", font=font_title, bg=bg_c, fg=accent).grid(row=0, column=0,
                                                                                              sticky="w", pady=(0, 5))
text_input = tk.Text(main_frame, height=4, width=50, font=font_main, bg=entry_bg, fg=fg_c, insertbackground="white",
                     relief="flat", padx=5, pady=5)
text_input.grid(row=1, column=0, columnspan=2, sticky="we", pady=(0, 15))

# =========================================================
# БЛОК 2: Случайные числа
# =========================================================
tk.Label(main_frame, text="2. Количество случайных чисел:", font=font_title, bg=bg_c, fg=accent).grid(row=2, column=0,
                                                                                                      sticky="w",
                                                                                                      pady=(0, 5))
entry_numbers = tk.Entry(main_frame, width=10, font=font_main, bg=entry_bg, fg=fg_c, insertbackground="white",
                         relief="flat")
entry_numbers.insert(0, "20")
entry_numbers.grid(row=3, column=0, sticky="w", pady=(0, 15), ipady=3)

# =========================================================
# БЛОК 3: Математическая функция
# =========================================================
tk.Label(main_frame, text="3. Математическая функция:", font=font_title, bg=bg_c, fg=accent).grid(row=4, column=0,
                                                                                                  columnspan=2,
                                                                                                  sticky="w",
                                                                                                  pady=(0, 5))

# Выпадающий список
var_func = tk.StringVar(value="sin(x)")
opt_menu = tk.OptionMenu(main_frame, var_func, "sin(x)", "cos(x)", "exp(x)", "x^2")
opt_menu.config(bg=entry_bg, fg=fg_c, highlightbackground=bg_c, relief="flat", activebackground="#3E5065",
                activeforeground="white")
opt_menu["menu"].config(bg=entry_bg, fg=fg_c)
opt_menu.grid(row=5, column=0, sticky="w", pady=(0, 10))

# Параметры (От, До, Шаг) в одну линию
frame_params = tk.Frame(main_frame, bg=bg_c)
frame_params.grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 20))

tk.Label(frame_params, text="От:", bg=bg_c, fg=fg_c, font=font_main).grid(row=0, column=0, padx=(0, 5))
entry_math_start = tk.Entry(frame_params, width=5, font=font_main, bg=entry_bg, fg=fg_c, insertbackground="white",
                            relief="flat")
entry_math_start.insert(0, "0")
entry_math_start.grid(row=0, column=1, padx=(0, 10), ipady=2)

tk.Label(frame_params, text="До:", bg=bg_c, fg=fg_c, font=font_main).grid(row=0, column=2, padx=(0, 5))
entry_math_end = tk.Entry(frame_params, width=5, font=font_main, bg=entry_bg, fg=fg_c, insertbackground="white",
                          relief="flat")
entry_math_end.insert(0, "10")
entry_math_end.grid(row=0, column=3, padx=(0, 10), ipady=2)

tk.Label(frame_params, text="Шаг:", bg=bg_c, fg=fg_c, font=font_main).grid(row=0, column=4, padx=(0, 5))
entry_math_step = tk.Entry(frame_params, width=5, font=font_main, bg=entry_bg, fg=fg_c, insertbackground="white",
                           relief="flat")
entry_math_step.insert(0, "1.0")
entry_math_step.grid(row=0, column=5, ipady=2)

# =========================================================
# КНОПКА ГЕНЕРАЦИИ (ШИРОКАЯ)
# =========================================================
btn_generate = tk.Button(main_frame, text="СОЗДАТЬ ФАЙЛ", font=("Arial", 12, "bold"),
                         bg="#27AE60", fg="white", activebackground="#2ECC71", activeforeground="white",
                         command=generate_file, cursor="hand2", relief="flat")
btn_generate.grid(row=7, column=0, columnspan=2, sticky="we", ipady=8)

# Запуск приложения
root.mainloop()