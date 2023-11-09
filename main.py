import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox, QLineEdit
import sqlite3

connection = sqlite3.connect('results.db')  # Имя вашей базы данных
cursor = connection.cursor()

# Создайте таблицу для хранения результатов, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS calculations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        num1 TEXT,
        num2 TEXT,
        base1 INTEGER,
        base2 INTEGER,
        operation TEXT,
        result TEXT
    )
''')

connection.commit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Дейсвтия с числами')
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        self.open_calc_button = QPushButton('Открыть калькулятор')
        self.open_calc_button.clicked.connect(self.openCalculator)

        self.open_conversion_button = QPushButton('Перевод числа из различных ССЧ')
        self.open_conversion_button.clicked.connect(self.openConversion)

        self.layout.addWidget(self.open_calc_button)
        self.layout.addWidget(self.open_conversion_button)
        self.central_widget.setLayout(self.layout)

    def openCalculator(self):
        self.calculator = CalculatorWindow()
        self.calculator.show()

    def openConversion(self):
        self.conversion_window = ConversionWindow()
        self.conversion_window.show()

    def closeEvent(self, event):
        connection.close()
        event.accept()


class CalculatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Калькулятор')
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()

        self.num1_label = QLabel('Число 1:')
        self.num1_text = QLineEdit()

        self.num1_base_label = QLabel('Система счисления числа 1:')
        self.num1_base_combo = QComboBox()
        self.num1_base_combo.addItems(['2', '8', '10', '16'])

        self.num2_label = QLabel('Число 2:')
        self.num2_text = QLineEdit()

        self.num2_base_label = QLabel('Система счисления числа 2:')
        self.num2_base_combo = QComboBox()
        self.num2_base_combo.addItems(['2', '8', '10', '16'])

        self.operation_label = QLabel('Действие:')
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(['+', '-', '*', '/'])

        self.result_label = QLabel('Результат в 10 ССЧ:')

        self.calculate_button = QPushButton('Вычислить')
        self.calculate_button.clicked.connect(self.calculate)

        self.layout.addWidget(self.num1_label)
        self.layout.addWidget(self.num1_text)
        self.layout.addWidget(self.num1_base_label)
        self.layout.addWidget(self.num1_base_combo)
        self.layout.addWidget(self.num2_label)
        self.layout.addWidget(self.num2_text)
        self.layout.addWidget(self.num2_base_label)
        self.layout.addWidget(self.num2_base_combo)
        self.layout.addWidget(self.operation_label)
        self.layout.addWidget(self.operation_combo)
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.calculate_button)

        self.setLayout(self.layout)

    def calculate(self):
        num1 = int(self.num1_text.text(), int(self.num1_base_combo.currentText()))
        num2 = int(self.num2_text.text(), int(self.num2_base_combo.currentText()))
        operation = self.operation_combo.currentText()

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                result = 'Ошибка (деление на ноль)'
        else:
            result = None

        # Сохраните результат в базу данных
        cursor.execute('''
            INSERT INTO calculations (num1, num2, base1, base2, operation, result)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (str(num1), str(num2), int(self.num1_base_combo.currentText()), int(self.num2_base_combo.currentText()),
              operation, str(result)))

        connection.commit()

        self.result_label.setText(f'Результат в 10 ССЧ: {result}')


class ConversionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Перевод числа из различных ССЧ')
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()

        self.number_label = QLabel('Введите число:')
        self.number_text = QLineEdit()

        self.from_base_label = QLabel('Из системы счисления:')
        self.from_base_combo = QComboBox()
        self.from_base_combo.addItems(['2', '8', '10', '16'])

        self.to_base_label = QLabel('В систему счисления:')
        self.to_base_combo = QComboBox()
        self.to_base_combo.addItems(['2', '8', '10', '16'])

        self.result_label = QLabel('Результат перевода:')

        self.convert_button = QPushButton('Перевести')
        self.convert_button.clicked.connect(self.convert)

        self.layout.addWidget(self.number_label)
        self.layout.addWidget(self.number_text)
        self.layout.addWidget(self.from_base_label)
        self.layout.addWidget(self.from_base_combo)
        self.layout.addWidget(self.to_base_label)
        self.layout.addWidget(self.to_base_combo)
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.convert_button)

        self.setLayout(self.layout)

    def convert(self):
        number = int(self.number_text.text(), int(self.from_base_combo.currentText()))
        to_base = int(self.to_base_combo.currentText())
        result = format(number, f'0{to_base}b')  # Переводим число в выбранную систему счисления и форматируем как строку
        self.result_label.setText(f'Результат перевода: {result}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())