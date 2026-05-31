import sys
import math
from PySide6.QtWidgets import (QApplication, QComboBox, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox)

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.field1 = QLineEdit()
        self.field2 = QLineEdit()
        self.res_line = QLabel()

        self.btn = QPushButton('Рассчитать')
        self.btn.clicked.connect(self.PrintResult)

        layout.addWidget(QLabel('Введите число элементов n:'))
        layout.addWidget(self.field1)
        layout.addWidget(QLabel('Введите выборку k:'))
        layout.addWidget(self.field2)

        combobox = QComboBox()
        combobox.addItem("Число перестановок")
        combobox.addItem("Число размещений")
        combobox.addItem("Число сочетаний")
        combobox.currentIndexChanged.connect(self.on_combobox_changed)
        layout.addWidget(combobox)
        self.setLayout(layout)
        self.setWindowTitle("Калькулятор")

        cb = QCheckBox('С повторениями', self)
        cb.stateChanged.connect(self.cb_choice)
        layout.addWidget(cb)
        layout.addWidget(self.btn)
        layout.addWidget(QLabel('Результат:'))
        layout.addWidget(self.res_line)
        
        self.resize(300, 200)
        self.show()

        combo_choice = 0
        check_choice = 0
    def on_combobox_changed(self, index):
        global combo_choice
        combo_choice = index
        print(f'Combo = {combo_choice}')

    def cb_choice(self, state):
        global check_choice
        check_choice = state
        print(f"Check: {check_choice}")

    def PrintResult(self):
        global check_choice, combo_choice
        insert = self.field1.text()
        n = insert.split()
        k = self.field2.text()
        if check_choice == 0:
            if combo_choice == 0:
                self.res_line.setText(f'Результат: {math.factorial(int(n[0]))}')
            if combo_choice == 1:
                self.res_line.setText(f'Результат: {math.factorial(int(n[0]))/math.factorial(int(n[0])-int(k))}')
            if combo_choice == 2:
                self.res_line.setText(f'Результат: {math.factorial(int(n[0]))/(math.factorial(int(k))*math.factorial(int(n[0])-int(k)))}')
        if check_choice == 2:
            if combo_choice == 0:
                print(n)
                self.res_line.setText(f'Результат: {math.factorial(int(n[0]) + int(n[1]) + int(n[2])) /(math.factorial(int(n[0]))*math.factorial(int(n[1]))* math.factorial(int(n[2]))) }')
            if combo_choice == 1:
                self.res_line.setText(f'Результат: {int(n[0])**int(k)}')
            if combo_choice == 2:
                self.res_line.setText(f'Результат: {math.factorial(int(n[0])+int(k)-1)/(math.factorial(int(n[0])-1)*math.factorial(int(k)))}')

        
    

class FirstWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.second_window = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Регистрация')
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.field1 = QLineEdit()

        self.field2 = QLineEdit()
        self.field2.setEchoMode(QLineEdit.Password)

        self.btn = QPushButton('Войти')
        self.btn.clicked.connect(self.openSecondWindow)

        layout.addWidget(QLabel('Логин:'))
        layout.addWidget(self.field1)
        layout.addWidget(QLabel('Пароль:'))
        layout.addWidget(self.field2)
        layout.addWidget(self.btn)

        self.setLayout(layout)

    def openSecondWindow(self):
        if self.field1.text() and self.field2.text():
            self.second_window = SecondWindow()
            self.second_window.show()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = FirstWindow()
    w.show()
    sys.exit(app.exec_())
