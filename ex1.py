import tkinter as tk
from tkinter import ttk
window = tk.Tk()
window.title("Индивидуальное задание")
window.geometry("400x400")
tab_control=ttk.Notebook(window)

tab1=ttk.Frame(tab_control)
tab2=ttk.Frame(tab_control)
tab3=ttk.Frame(tab_control)
tab4=ttk.Frame(tab_control)

tab_control.add(tab1,text="Button")
tab_control.add(tab2,text="Password")
tab_control.add(tab3,text="Checkbox")
tab_control.add(tab4,text="Radiobutton")

#кнопка с номером щелчка и цифрой
click_number = 1
check_pr_ch = [1, 2, 3]
k = 0
for i in range(1000):
    for j in range(1000):
        if j != 0 and i > 3:
            if i%j == 0:
                k += 1
    if k == 2: check_pr_ch.append(i)
    else: k = 0
def clicked1():
    global click_number
    btn1.configure(text =(f"щелчок {click_number} простое число {check_pr_ch[click_number]}"))
    click_number += 1
btn1=tk.Button(tab1,text="0 1",bg="black", fg="red",command=clicked1)
btn1.grid(column=1,row=0)

#второе окно с двумя текстовыми полями, паролем, кнопкой
def check_password():
    global pwd_entry, text_result
    password = pwd_entry.get()
    text_result.config(state='normal')
    text_result.delete('1.0', tk.END)
    if password == "0000":
        msg = "и мы его грохнули"
    else:
        msg = "Неверный пароль."
    text_result.insert('1.0', msg)
    text_result.config(state='disabled')

text_start = tk.Text(tab2, width=60, height=5, wrap='word')
text_start.pack()
text_start.insert("1.0", "Леня Воронин был опом")

tk.Label(tab2, text="Пароль:").pack(anchor='w', padx=5)
pwd_entry = tk.Entry(tab2, show='*', width=30)
pwd_entry.pack(padx=5, pady=5)
tk.Button(tab2, text="Продолжить", command=check_password).pack(pady=5)

text_result = tk.Text(tab2, width=60, height=4, wrap='word', state='disabled')
text_result.pack(padx=5, pady=5)

#окно с флажками
def update_word():
    global var1, var2, var3, var4, var5, word_label
    word = ' '
    if var1.get(): word += 'a'
    if var2.get(): word += 'p'
    if var3.get(): word += 'p'
    if var4.get(): word += 'l'
    if var5.get(): word += 'e'
    word_label.config(text=f"Word: {word}")
var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()
var4 = tk.IntVar()
var5 = tk.IntVar()
tk.Label(tab3, text="Выберите буквы:",font=("Arial", 10)).pack(anchor='w', padx=5, pady=5)
tk.Checkbutton(tab3, text='a', variable=var1, command=update_word).pack(anchor='w', padx=20)
tk.Checkbutton(tab3, text='p', variable=var2, command=update_word).pack(anchor='w', padx=20)
tk.Checkbutton(tab3, text='p', variable=var3, command=update_word).pack(anchor='w', padx=20)
tk.Checkbutton(tab3, text='l', variable=var4, command=update_word).pack(anchor='w', padx=20)
tk.Checkbutton(tab3, text='e', variable=var5, command=update_word).pack(anchor='w', padx=20)

#переключатели
def show_example():
    global posled_var, example_label
    choice = posled_var.get()
    examples = {
        "list": "[1, 2, 3]",
        "tuple": "(1, 2, 3)",
        "str": "text",
        "range": "range(start, stop, step)"
        }
    example_label.config(text=examples.get(choice, ""))

def create_radiobutton_tab():
    global posled_var, example_label
    tk.Label(tab4, text="Выберите тип последовательности:",font=("Arial", 10)).pack(anchor='w', padx=5, pady=5)
    posled_var = tk.StringVar(value="list")
    posleds = [
        ("Список (list)", "list"),
        ("Кортеж (tuple)", "tuple"),
        ("Строка (str)", "str"),
        ("Range", "range"),
        ]
    for text, value in posleds:
        tk.Radiobutton(tab4, text=text, variable=posled_var, value=value, command=show_example).pack(anchor='w', padx=20)
        example_label = tk.Label(tab4, text="", font=("Courier", 12, "bold"), fg="blue")
        example_label.pack(pady=15)
        
create_radiobutton_tab()





word_label = tk.Label(tab3, text="Word", font=("Arial", 12, "bold"))
word_label.pack(pady=10)

tab_control.pack(expand=1,fill="both")
window.mainloop()

