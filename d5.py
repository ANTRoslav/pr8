import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
import requests


# =========================================================
# ЛОГИКА ОТПРАВКИ
# =========================================================

def send_email(to_addr, subject, body, login, password):
    """Реальная отправка Email через SMTP (например, Яндекс или Mail.ru)"""
    try:
        # Для примера используем SMTP Яндекс (можно заменить на Gmail/Mail.ru)
        smtp_server = "smtp.yandex.ru"
        port = 465

        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = login
        msg["To"] = to_addr

        # Подключение по SSL
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(login, password)  # Пароль должен быть "паролем приложения", а не от входа!
            server.send_message(msg)
        return True, "Email отправлен успешно!"
    except Exception as e:
        return False, f"Ошибка Email: {e}"


def send_telegram(chat_id, token, text):
    """Реальная отправка в Telegram через Bot API"""
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            return True, "Сообщение в Telegram отправлено!"
        else:
            return False, f"Ошибка Telegram: {response.text}"
    except Exception as e:
        return False, f"Ошибка Telegram: {e}"


def send_sms_simulated(phone, text):
    """Симуляция отправки SMS (так как нужен платный шлюз типа Twilio)"""
    print(f"[SMS] На номер {phone} отправлено: {text}")
    return True, "SMS отправлено (Симуляция: реальный шлюз не подключен)."


def send_push_simulated(device_token, text):
    """Симуляция Push-уведомления (нужен Firebase/APNs)"""
    print(f"[PUSH] На устройство {device_token} отправлено: {text}")
    return True, "Push отправлен (Симуляция)."


# =========================================================
# ИНТЕРФЕЙС
# =========================================================

def on_send():
    channel = var_channel.get()
    text = entry_message.get("1.0", tk.END).strip()
    target = entry_target.get().strip()

    if not text:
        messagebox.showwarning("Внимание", "Введите текст сообщения!")
        return

    success = False
    msg = ""

    if channel == "Email":
        login = entry_login.get().strip()
        password = entry_password.get().strip()
        subject = entry_subject.get().strip()
        success, msg = send_email(target, subject, text, login, password)

    elif channel == "Telegram":
        token = entry_login.get().strip()  # Для Telegram логин = токен бота
        success, msg = send_telegram(target, token, text)

    elif channel == "SMS":
        success, msg = send_sms_simulated(target, text)

    elif channel == "Push":
        success, msg = send_push_simulated(target, text)

    if success:
        messagebox.showinfo("Успех", msg)
    else:
        messagebox.showerror("Ошибка", msg)


root = tk.Tk()
root.title("Универсальный мессенджер (Multi-Channel Sender)")
root.geometry("600x600")
root.configure(bg="#1E1E24")

bg_c = "#1E1E24"
fg_c = "#E0E0E0"
accent = "#00E5FF"
entry_bg = "#2C3E50"

font_title = ("Arial", 12, "bold")

# --- Выбор канала ---
tk.Label(root, text="1. Выберите канал связи:", font=font_title, bg=bg_c, fg=accent).pack(anchor="w", padx=20,
                                                                                          pady=(15, 5))

var_channel = tk.StringVar(value="Email")
frame_channels = tk.Frame(root, bg=bg_c)
frame_channels.pack(anchor="w", padx=20)

for ch in ["Email", "Telegram", "SMS", "Push"]:
    tk.Radiobutton(frame_channels, text=ch, variable=var_channel, value=ch, bg=bg_c, fg=fg_c, selectcolor=entry_bg,
                   activebackground=bg_c, activeforeground=accent, font=("Arial", 10)).pack(side="left", padx=10)

# --- Поля авторизации (Логин/Токен) ---
tk.Label(root, text="2. Данные авторизации (Логин/Токен):", font=font_title, bg=bg_c, fg=accent).pack(anchor="w",
                                                                                                      padx=20,
                                                                                                      pady=(15, 5))
entry_login = tk.Entry(root, bg=entry_bg, fg=fg_c, insertbackground="white", relief="flat")
entry_login.pack(fill="x", padx=20, pady=2, ipady=3)

tk.Label(root, text="Пароль (для Email):", bg=bg_c, fg=fg_c).pack(anchor="w", padx=20)
entry_password = tk.Entry(root, bg=entry_bg, fg=fg_c, insertbackground="white", relief="flat", show="*")
entry_password.pack(fill="x", padx=20, pady=2, ipady=3)

# --- Поля получателя ---
tk.Label(root, text="3. Получатель (Email/ID/Номер):", font=font_title, bg=bg_c, fg=accent).pack(anchor="w", padx=20,
                                                                                                 pady=(15, 5))
entry_target = tk.Entry(root, bg=entry_bg, fg=fg_c, insertbackground="white", relief="flat")
entry_target.pack(fill="x", padx=20, pady=2, ipady=3)

# --- Тема (для Email) ---
tk.Label(root, text="Тема (для Email):", bg=bg_c, fg=fg_c).pack(anchor="w", padx=20)
entry_subject = tk.Entry(root, bg=entry_bg, fg=fg_c, insertbackground="white", relief="flat")
entry_subject.pack(fill="x", padx=20, pady=2, ipady=3)

# --- Текст сообщения ---
tk.Label(root, text="4. Текст сообщения:", font=font_title, bg=bg_c, fg=accent).pack(anchor="w", padx=20, pady=(15, 5))
entry_message = tk.Text(root, height=6, bg=entry_bg, fg=fg_c, insertbackground="white", relief="flat")
entry_message.pack(fill="x", padx=20, pady=2)

# --- Кнопка ---
btn_send = tk.Button(root, text="ОТПРАВИТЬ СООБЩЕНИЕ", font=("Arial", 12, "bold"), bg="#27AE60", fg="white",
                     activebackground="#2ECC71", command=on_send, relief="flat")
btn_send.pack(fill="x", padx=20, pady=(20, 10), ipady=10)

root.mainloop()