import tkinter as tk
from tkinter import ttk
import math
window = tk.Tk()
window.title("Индивидуальное задание")
window.geometry("750x750")
tab_control=ttk.Notebook(window)


tab2=ttk.Frame(tab_control)
tab4=ttk.Frame(tab_control)


tab_control.add(tab2,text="Password")



#второе окно с двумя текстовыми полями, паролем, кнопкой
def check_password():
    global pwd_entry, text_result, name_entry
    password = pwd_entry.get()
    name = name_entry.get()
    text_result.config(state='normal')
    text_result.delete('1.0', tk.END)
    if password == "0000" and name == "vlad":
        msg = "Успешный успех!"
        tab_control.add(tab4, text="Calculator")
    else:
        msg = "Неверный пароль."
    text_result.insert('1.0', msg)
    text_result.config(state='disabled')

tk.Label(tab2, text="Имя пользователя:").pack(anchor='w', padx=5)
name_entry = tk.Entry(tab2, width=30)
name_entry.pack(padx=5, pady=5)

tk.Label(tab2, text="Пароль:").pack(anchor='w', padx=5)
pwd_entry = tk.Entry(tab2, show='*', width=30)
pwd_entry.pack(padx=5, pady=5)

tk.Button(tab2, text="Продолжить", command=check_password).pack(pady=5)

text_result = tk.Text(tab2, width=60, height=4, wrap='word', state='disabled')
text_result.pack(padx=5, pady=5)


#калькулятор
tk.Label(tab4, text="Введите число элементов n:",font=("Arial", 10)).pack(anchor='w', padx=5, pady=5)
text_first = tk.Text(tab4, width=5, height=2, wrap='word')
text_first.pack()

tk.Label(tab4, text="Введите выборку k:",font=("Arial", 10)).pack(anchor='w', padx=5, pady=5)
text_second = tk.Text(tab4, width=5, height=2, wrap='word')
text_second.pack()



options = ["Чило перестановок", "Число размещений", "Число сочетаний"]
combo = ttk.Combobox(tab4, values=options, state="readonly")
combo.set("Выберите операций")
combo.pack(pady=20)

reply = tk.Radiobutton(tab4, text = "C повторениями")
reply.pack()

tk.Button(tab4, text="Выполнить", command=check_password).pack(pady=5)

tab_control.pack(expand=1,fill="both")
window.mainloop()

