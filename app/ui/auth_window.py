from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from app.database.db import DB

from app.ui.main_window import MainWindow


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Авторизация')
        self.setMinimumSize()

        layout = QVBoxLayout()
        self.setLayout(layout)

        label_email = QLabel('Почта')
        self.email_edit = QLineEdit()
        label_password = QLabel('Пароль')
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        auth_button = QPushButton('Войти')
        auth_button.clicked.connect(self.auth)

        layout.addWidget(label_email)
        layout.addWidget(self.email_edit)
        layout.addWidget(label_password)
        layout.addWidget(self.password_edit)
        layout.addWidget(auth_button)

    def auth(self):
        email = self.email_edit.text()
        password = self.password_edit.text()
        user = DB.auth(email, password)
        if user:
            self.window = MainWindow()
            self.window.show()
            self.close()
            print('Успешно')
        else:
            print('Ошибка')
