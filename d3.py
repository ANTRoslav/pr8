import tkinter as tk
from tkinter import messagebox, filedialog
import random
import os
import zipfile


# =========================================================
# ГЕНЕРАЦИЯ WORD (.docx) БЕЗ БИБЛИОТЕК
# =========================================================
def create_docx_manually(filename, data):
    doc_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:body>
    <w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="32"/></w:rPr><w:t>Результаты измерений</w:t></w:r></w:p>
    <w:tbl>
    <w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/><w:tblBorders>
    <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
    <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
    <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
    </w:tblBorders></w:tblPr>
    <w:tblGrid><w:gridCol w:w="3000"/><w:gridCol w:w="3000"/></w:tblGrid>
    """
    doc_xml += """<w:tr><w:tc><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/></w:rPr><w:t>Номер измерения</w:t></w:r></w:p></w:tc>
    <w:tc><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/></w:rPr><w:t>Результат</w:t></w:r></w:p></w:tc></w:tr>"""

    for i, val in enumerate(data):
        doc_xml += f"""<w:tr><w:tc><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:t>{i + 1}</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:t>{val}</w:t></w:r></w:p></w:tc></w:tr>"""

    doc_xml += """</w:tbl>
    <w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>
    </w:body></w:document>"""

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
    </Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
    </Relationships>"""

    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr('[Content_Types].xml', content_types)
        zipf.writestr('_rels/.rels', rels)
        zipf.writestr('word/document.xml', doc_xml)


# =========================================================
# ГЕНЕРАЦИЯ EXCEL (.xlsx) БЕЗ БИБЛИОТЕК
# =========================================================
def create_xlsx_manually(filename, data):
    # Формируем XML для таблицы Excel
    sheet_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheetData>
    <row r="1">
        <c r="A1" t="inlineStr"><is><t>Номер измерения</t></is></c>
        <c r="B1" t="inlineStr"><is><t>Результат</t></is></c>
    </row>
    """

    for i, val in enumerate(data):
        row_num = i + 2
        sheet_xml += f"""<row r="{row_num}">
            <c r="A{row_num}"><v>{i + 1}</v></c>
            <c r="B{row_num}"><v>{val}</v></c>
        </row>"""

    sheet_xml += """</sheetData></worksheet>"""

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
    <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    </Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
    </Relationships>"""

    workbook_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <sheets><sheet name="Измерения" sheetId="1" r:id="rId1"/></sheets>
    </workbook>"""

    workbook_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
    </Relationships>"""

    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr('[Content_Types].xml', content_types)
        zipf.writestr('_rels/.rels', rels)
        zipf.writestr('xl/workbook.xml', workbook_xml)
        zipf.writestr('xl/_rels/workbook.xml.rels', workbook_rels)
        zipf.writestr('xl/worksheets/sheet1.xml', sheet_xml)


# =========================================================
# ЛОГИКА ПРИЛОЖЕНИЯ
# =========================================================
def generate_files():
    try:
        num_rows = int(entry_count.get())
        min_val = int(entry_min.get())
        max_val = int(entry_max.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте ввод чисел.")
        return

    if num_rows <= 0 or min_val > max_val:
        messagebox.showerror("Ошибка", "Количество строк > 0, а минимум <= максимума.")
        return

    manual_data = []
    mode = var_mode.get()

    if mode == "Вручную":
        raw_text = text_manual.get("1.0", tk.END).strip()
        try:
            manual_data = [int(x.strip()) for x in raw_text.replace(',', ' ').split() if x.strip()]
        except ValueError:
            messagebox.showerror("Ошибка", "В ручном вводе только целые числа.")
            return
        if len(manual_data) != num_rows:
            messagebox.showerror("Ошибка", f"Указано {num_rows} строк, а введено {len(manual_data)} чисел.")
            return
    else:
        manual_data = [random.randint(min_val, max_val) for _ in range(num_rows)]

    folder = filedialog.askdirectory(title="Выберите папку для сохранения")
    if not folder:
        return

    word_path = os.path.join(folder, "Отчет_Измерений.docx")
    excel_path = os.path.join(folder, "Данные_Измерений.xlsx")

    try:
        create_docx_manually(word_path, manual_data)
        create_xlsx_manually(excel_path, manual_data)
        messagebox.showinfo("Успех", f"Файлы успешно созданы!\n\n{word_path}\n{excel_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить:\n{e}")


# =========================================================
# ИНТЕРФЕЙС (TKINTER)
# =========================================================
root = tk.Tk()
root.title("Генератор Word/Excel")
root.geometry("500x520")
root.configure(bg="#1E1E24")
root.resizable(False, False)

bg_c = "#1E1E24"
fg_c = "#E0E0E0"
accent = "#00E5FF"
entry_bg = "#2C3E50"

font_main = ("Arial", 10)
font_title = ("Arial", 10, "bold")

main_frame = tk.Frame(root, bg=bg_c, padx=20, pady=15)
main_frame.pack(fill="both", expand=True)

tk.Label(main_frame, text="1. Параметры таблицы", font=font_title, bg=bg_c, fg=accent).pack(anchor="w", pady=(0, 10))

f1 = tk.Frame(main_frame, bg=bg_c)
f1.pack(fill="x", pady=5)
tk.Label(f1, text="Количество строк:", width=18, anchor="w", bg=bg_c, fg=fg_c, font=font_main).pack(side="left")
entry_count = tk.Entry(f1, font=font_main, bg=entry_bg, fg=fg_c, insertbackground="white", relief="flat")
entry_count.insert(0, "10")
entry_count.pack(side="left", fill="x", expand=True, ipady=3)

f2 = tk.Frame(main_frame, bg=bg_c)
f2.pack(fill="x", pady=5)
tk.Label(f2, text="Диапазон (Мин - Макс):", width=18, anchor="w", bg=bg_c, fg=fg_c, font=font_main).pack(side="left")
entry_min = tk.Entry(f2, width=6, font=font_main, bg=entry_bg, fg=fg_c, insertbackground="white", relief="flat")
entry_min.insert(0, "0")
entry_min.pack(side="left", ipady=3)
tk.Label(f2, text="-", bg=bg_c, fg=fg_c).pack(side="left", padx=5)
entry_max = tk.Entry(f2, width=6, font=font_main, bg=entry_bg, fg=fg_c, insertbackground="white", relief="flat")
entry_max.insert(0, "100")
entry_max.pack(side="left", ipady=3)

tk.Label(main_frame, text="2. Способ заполнения", font=font_title, bg=bg_c, fg=accent).pack(anchor="w", pady=(15, 5))

var_mode = tk.StringVar(value="Автоматически")
frame_radio = tk.Frame(main_frame, bg=bg_c)
frame_radio.pack(fill="x", pady=5)
tk.Radiobutton(frame_radio, text="Автоматически", variable=var_mode, value="Автоматически", bg=bg_c, fg=fg_c,
               selectcolor=entry_bg, activebackground=bg_c, activeforeground=accent, font=font_main).pack(side="left",
                                                                                                          padx=(0, 20))
tk.Radiobutton(frame_radio, text="Вручную", variable=var_mode, value="Вручную", bg=bg_c, fg=fg_c, selectcolor=entry_bg,
               activebackground=bg_c, activeforeground=accent, font=font_main).pack(side="left")

tk.Label(main_frame, text="Числа через пробел (для 'Вручную'):", bg=bg_c, fg=fg_c, font=font_main).pack(anchor="w",
                                                                                                        pady=(10, 0))
text_manual = tk.Text(main_frame, height=4, font=font_main, bg=entry_bg, fg=fg_c, insertbackground="white",
                      relief="flat")
text_manual.pack(fill="x", pady=5)

btn_generate = tk.Button(main_frame, text="СОЗДАТЬ ФАЙЛЫ (WORD + EXCEL)", font=("Arial", 12, "bold"),
                         bg="#27AE60", fg="white", activebackground="#2ECC71", activeforeground="white",
                         command=generate_files, cursor="hand2", relief="flat")
btn_generate.pack(fill="x", pady=(20, 0), ipady=10)

root.mainloop()