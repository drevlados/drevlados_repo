import subprocess
import tkinter as tk
from tkinter import ttk
window = tk.Tk()
window.title("MAP_CENERATOR")
window.geometry("750x750")
tab_control=ttk.Notebook(window)

tab1=ttk.Frame(tab_control)
tab2=ttk.Frame(tab_control)
tab4=ttk.Frame(tab_control)

tab_control.add(tab1,text="Регистрация")
tab_control.add(tab2,text="Авторизация")

tk.Label(tab1, text="Придумайте имя пользователя:").pack(anchor='w', padx=5)
name_reg = tk.Entry(tab1, width=30)
name_reg.pack(padx=5, pady=5)

tk.Label(tab1, text="Придумайте пароль:").pack(anchor='w', padx=5)
pwd_reg = tk.Entry(tab1, show='*', width=30)
pwd_reg.pack(padx=5, pady=5)
right_password = '1'
right_name = '1'
def got_data():
    global pwd_reg, name_reg, right_password, right_name
    right_password = pwd_reg.get()
    right_name = name_reg.get()
    tk.Label(tab1, text = "Регистрация прошла успешно").pack()
tk.Button(tab1, text="Зарегистрироваться", command=got_data).pack(pady=5)





#второе окно с двумя текстовыми полями, паролем, кнопкой
def check_password():
    global pwd_entry, text_result, name_entry, right_password, right_name
    password = pwd_entry.get()
    name = name_entry.get()
    text_result.config(state='normal')
    text_result.delete('1.0', tk.END)
    if password == right_password and name == right_name:
        msg = "Успешный успех!"
        tab_control.add(tab4, text="MAP_GENERATOR")
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


#окно генератора tab4
def generate():
    with open('map_gen_file.txt', 'w', encoding='UTF-8') as file:
        file.write(town_w.get('1.0',tk.END))
        file.write(town_h.get('1.0',tk.END))
        file.write(population.get('1.0',tk.END))
        file.write(small_house.get('1.0',tk.END))
        file.write(big_house.get('1.0',tk.END))
        file.write(rings.get('1.0',tk.END))
        file.write(straight.get('1.0',tk.END))
        file.write(grid.get('1.0',tk.END))
        
        
    subprocess.run(["python", "map_gen_idle.py"])
tk.Label(tab4, text = "В этом окне приложения вы можете сгенерировать процедурную карту города по заданным Вами параметрам").pack()
tk.Label(tab4, text = "Задайте основные параметры карты:").pack()

tk.Label(tab4, text="Введите длину города(в метрах):").pack()
town_w = tk.Text(tab4, width=10, height = 1)
town_w.pack()

tk.Label(tab4, text="Введите ширину(в метрах):").pack()
town_h = tk.Text(tab4, width=10, height = 1)
town_h.pack()

tk.Label(tab4, text="Примерное население города:").pack()
population = tk.Text(tab4, width=10, height = 1)
population.pack()

tk.Label(tab4, text="Сколько человек проживает в малоквартирном доме?").pack(pady=5)
small_house = tk.Text(tab4, width=10, height = 1)
small_house.pack()

tk.Label(tab4, text="Сколько человек проживает в многоэтажке?").pack(pady=5)
big_house = tk.Text(tab4, width=10, height = 1)
big_house.pack()

tk.Label(tab4, text="Сколько кольцевых дорог в вашем городе?").pack(pady=5)
rings = tk.Text(tab4, width=10, height = 1)
rings.pack()

tk.Label(tab4, text="Сколько магистралей в вашем городе?").pack(pady=5)
straight = tk.Text(tab4, width=10, height = 1)
straight.pack()

tk.Label(tab4, text="Размер сетки карты(в метрах квадратных)").pack(pady=5)
grid = tk.Text(tab4, width=10, height = 1)
grid.pack()

tk.Button(tab4, text="Сгенерировать карту!", command=generate).pack(pady=15)

tab_control.pack(expand=1,fill="both")
window.mainloop()

