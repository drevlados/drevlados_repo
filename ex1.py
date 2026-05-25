from tkinter import *
from tkinter import ttk
window = Tk()
window.title("Индивидуальное задание")
window.geometry("400x250")
tab_control=ttk.Notebook(window)

tab1=ttk.Frame(tab_control)
tab2=ttk.Frame(tab_control)
tab3=ttk.Frame(tab_control)

tab_control.add(tab1,text="Первая")
tab_control.add(tab2,text="Вторая")
tab_control.add(tab3,text="Третья")

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
btn1=Button(tab1,text="0 1",bg="black", fg="red",command=clicked1)
btn1.grid(column=1,row=0)

#второе окно с двумя текстовыми полями, паролем, кнопкой
text_start = Text(tab2, width=60, height=5, wrap='word')

tab_control.pack(expand=1,fill="both")
window.mainloop()
