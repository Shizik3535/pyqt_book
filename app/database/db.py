import MySQLdb as mdb
import sys

# Подключение к базе данных
try:
    db = mdb.connect(
        host="192.168.31.205",
        port=3306,
        user="root",
        password="root",
        database="book_store"
    )
except mdb.Error as e:
    print("Ошибка подключения к базе данных:", e)
    sys.exit(1)


class DB:
    # AUTH
    @classmethod
    def auth(cls, email, password):
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE email = %s AND password = %s",
                    (email, password),
                )
                user = cursor.fetchone()
                return user
        except mdb.Error as e:
            print("Ошибка при аутентификации:", e)
            return None

    # Users
    @classmethod
    def take_user_check(cls, user_id):
        try:
            with db.cursor() as cursor:
                cursor.callproc("get_user_check", (user_id,))  # Используем callproc
                results = cursor.fetchall()  # Получаем первый набор результатов
                while cursor.nextset():  # Переходим к следующему набору
                    pass
                return results
        except mdb.Error as e:
            print("Ошибка при получении чеков пользователя:", e)
            return None

    @classmethod
    def new_check(cls, user_id, books):
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO check_sale (user_id)
                    VALUES (%s);
                    """,
                    (user_id,),
                )
                check_id = cursor.lastrowid
                for book in books:
                    cursor.execute(
                        """
                        INSERT INTO check_sale_book (check_id, book_id, quantity)
                        VALUES (%s, %s, %s);
                        """,
                        (check_id, book.id, book.quantity),
                    )
                db.commit()
                return check_id
        except mdb.Error as e:
            print("Ошибка при создании чека:", e)
            return None

    # Books
    @classmethod
    def get_books(cls):
        try:
            with db.cursor() as cursor:
                cursor.execute("SELECT * FROM book")
                books = cursor.fetchall()
                return books
        except mdb.Error as e:
            print("Ошибка при получении списка книг:", e)
            return None

    # Admin
    @classmethod
    def get_users_info(cls):
        try:
            with db.cursor() as cursor:
                cursor.callproc("get_users_info")  # Используем callproc
                results = cursor.fetchall()  # Получаем первый набор результатов
                while cursor.nextset():  # Переходим к следующему набору
                    pass
                return results
        except mdb.Error as e:
            print("Ошибка при получении информации о пользователях:", e)
            return None