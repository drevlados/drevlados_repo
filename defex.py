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
def example():
    global choice, selected_var, text_first, text_second, result
    choice1 = combo.get()
    choice2 = selected_var.get()
    n = text_first.get("1.0","1.10")
    n2 = text_first.get("2.0","2.10")
    n3 = text_first.get("3.0","3.10")
    k = text_second.get("1.0","1.10")
    if choice2 == "Без повторений":
        if choice1 == "Число перестановок":
            result.config(text = f'Результат: {math.factorial(int(n))}')
        if choice1 == "Число размещений":
            result.config(text = f'Результат: {math.factorial(int(n))/math.factorial(int(n)-int(k))}')
        if choice1 == "Число сочетаний":
            result.config(text = f'Результат: {math.factorial(int(n))/(math.factorial(int(k))*math.factorial(int(n)-int(k)))}')
    if choice2 == "С повторениями":
        if choice1 == "Число перестановок":
            result.config(text = f'Результат: {math.factorial(int(n) + int(n2) + int(n3)) /(math.factorial(int(n))*math.factorial(int(n2))* math.factorial(int(n3))) }')
        if choice1 == "Число размещений":
            result.config(text = f'Результат: {int(n)**int(k)}')
        if choice1 == "Число сочетаний":
            result.config(text = f'Результат: {math.factorial(int(n)+int(k)-1)/(math.factorial(int(n)-1)*math.factorial(int(k)))}')
        


tk.Label(tab4, text="Введите число элементов n:",font=("Arial", 10)).pack(anchor='w', padx=5, pady=10)
text_first = tk.Text(tab4, width=5, height=2, wrap='word')
text_first.pack()

tk.Label(tab4, text="Введите выборку k:",font=("Arial", 10)).pack(anchor='w', padx=5, pady=5)
text_second = tk.Text(tab4, width=5, height=2, wrap='word')
text_second.pack()

options = ["Число перестановок", "Число размещений", "Число сочетаний"]
combo = ttk.Combobox(tab4, values=options, state="readonly")
combo.set("Выберите операцию")
combo.pack(pady=20)

selected_var = tk.StringVar()
selected_var.set("Без повторений")  
replies = ["Без повторений", "С повторениями"]
for var in replies:
    tk.Radiobutton(tab4, text=var, variable=selected_var, value=var).pack()




tk.Button(tab4, text="Выполнить", command=example).pack(pady=5)
result = tk.Label(tab4, text = "Результат")
result.pack(pady = 10)

tab_control.pack(expand=1,fill="both")
window.mainloop()

