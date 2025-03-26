from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QRadioButton, QButtonGroup, QScrollArea, QFrame
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from app.database.db import DB  # Импорт базы данных


class BookWidget(QFrame):
    def __init__(self, book_id, title, price, photo, rating):
        super().__init__()
        self.book_id = book_id
        self.title = title
        self.price = price
        self.rating = rating

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Картинка книги
        self.image_label = QLabel()
        self.image_label.setFixedSize(200, 250)
        self.image_label.setScaledContents(True)
        if photo:
            book_pixmap = QPixmap()
            if book_pixmap.loadFromData(photo):
                self.image_label.setPixmap(book_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            else:
                self.image_label.setText("<h3>Фото не загрузилось</h3>")
                self.image_label.setStyleSheet("border: 1px solid #ccc")
        else:
            self.image_label.setText("<h3>Фото не загрузилось</h3>")
            self.image_label.setStyleSheet("border: 1px solid #ccc")

        self.info_label = QLabel(f"""
        <h2>{title}</h2>
        <p>Цена: {price}</p>
        <p>Рейтинг: {self.rating}</p>
        """)


        # Радиокнопка для выбора книги
        self.radio_button = QRadioButton()
        self.radio_button.setObjectName(str(book_id))
        self.radio_button.toggled.connect(self.update_style)

        # Добавляем всё в горизонтальный layout
        layout.addWidget(self.radio_button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.info_label)

        self.setLayout(layout)

    def update_style(self):
        if self.radio_button.isChecked():
            self.setStyleSheet("""
                BookWidget {border: 2px solid red;}
            """)
        else:
            self.setStyleSheet("""
                BookWidget {border: 2px solid #4f5b62;}
            """)

    def increment_rating(self):
        self.rating += 1
        self.info_label.setText(f"""
        <h2>{self.title}</h2>
        <p>Цена: {self.price}</p>
        <p>Рейтинг: {self.rating}</p>
        """)


class RatingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Рейтинг книг")
        self.setGeometry(300, 300, 400, 400)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.books = DB.get_books()
        if self.books:
            self.window_title = QLabel("<h1>Рейтинг книг</h1>")
            self.window_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.window_title)

            # Скроллбар для списка книг
            scroll_area = QScrollArea()
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_widget)

            self.books_button_group = QButtonGroup()

            self.book_widgets = {}  # Словарь для хранения виджетов книг

            for book in self.books:
                book_id, title, price, photo, rating = book
                book_widget = BookWidget(book_id, title, price, photo, rating)

                self.books_button_group.addButton(book_widget.radio_button)
                scroll_layout.addWidget(book_widget)

                self.book_widgets[book_id] = book_widget

            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(scroll_widget)
            layout.addWidget(scroll_area)

            # Кнопка выбора книги
            self.book_choose_button = QPushButton("Выбрать")
            self.book_choose_button.clicked.connect(self.choose_book)
            layout.addWidget(self.book_choose_button)

        else:
            label = QLabel("<h1>Нет доступных книг.</h1>")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

    def choose_book(self):
        """Функция, вызываемая при выборе книги."""
        selected_button = self.books_button_group.checkedButton()
        if selected_button:
            book_id = int(selected_button.objectName())  # Получаем ID книги
            selected_book = self.book_widgets[book_id]

            # Увеличиваем рейтинг книги
            selected_book.increment_rating()
            DB.increase_book_rating(str(book_id))

            # print(f"Выбрана книга ID {book_id}, новый рейтинг: {selected_book.rating}")

