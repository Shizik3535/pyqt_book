from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PyQt6.QtGui import QPixmap
from app.database.db import DB


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Главное окно')
        self.setGeometry(300, 300, 500, 300)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(self.main_layout)

        # Title
        self.title_label = QLabel("<h1>Список покупателей и их заказы: (В3)</h1>")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Main content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_content_layout = QVBoxLayout()
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_content_layout)

        # Добавляем виджеты
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.scroll_area)

        self.users = DB.get_users_info()
        if self.users:
            for user in self.users:
                user_id = user[0]
                email = user[1]
                phone = user[2]
                total_quantity = user[3]
                total_price = user[4]
                user_book = DB.take_user_check(str(user_id))

                self.user_label = QLabel(f"""
                Почта:<strong>{email}</strong> Номер телефона:<strong>{phone}</strong>
                <br/>
                Количество заказанных книг:<strong>{total_quantity}</strong>
                <br/>
                Сумма заказанных книг:<strong>{total_price}</strong>
                """)
                self.scroll_content_layout.addWidget(self.user_label)
                if user_book:
                    books_layout = QVBoxLayout()
                    books_layout.setContentsMargins(30, 0, 0, 0)
                    self.scroll_content_layout.addLayout(books_layout)
                    for book in user_book:
                        # print(book)
                        book_photo = book[0]
                        book_title = book[1]
                        book_sale_date = book[2]
                        book_quantity = book[3]

                        book_layout = QHBoxLayout()
                        books_layout.addLayout(book_layout)

                        # Image
                        book_image = QLabel()
                        book_image.setFixedSize(200, 250)
                        book_image.setScaledContents(True)
                        book_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        if book_photo:
                            book_pixmap = QPixmap()
                            if book_pixmap.loadFromData(book_photo):
                                book_image.setPixmap(book_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
                            else:
                                book_image.setText("<h3>Фото не загрузилось</h3>")
                                book_image.setStyleSheet("border: 1px solid #ccc")
                        else:
                            book_image.setText("<h3>Фото не загрузилось</h3>")
                            book_image.setStyleSheet("border: 1px solid #ccc")
                        book_layout.addWidget(book_image)

                        # Book info
                        book_label = QLabel(f"""
                        <h3>{book_title}</h3>
                        Дата продажи:<strong>{book_sale_date}</strong>
                        <br/>
                        Количество:<strong>{book_quantity}</strong>
                        """)
                        book_layout.addWidget(book_label)


                else:
                    book_label = QLabel("<h3>Нет покупок</h3>")
                    self.scroll_content_layout.addWidget(book_label)
        else:
            self.empty_label = QLabel("<h2>Нет покупателей в базе данных</h2>")
            self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(self.empty_label)

