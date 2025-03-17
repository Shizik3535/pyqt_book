-- -- Создание базы данных
-- CREATE DATABASE IF NOT EXISTS book_store;
-- USE book_store;

-- Книга. Название, цена, фото
CREATE TABLE IF NOT EXISTS book (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    photo LONGBLOB
);

-- Пользователи. Почта, телефон, пароль, дата рождения
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

-- Чек
CREATE TABLE IF NOT EXISTS check_sale (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    sale_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Книги в чеке
CREATE TABLE IF NOT EXISTS check_sale_book (
    id INT PRIMARY KEY AUTO_INCREMENT,
    check_id INT NOT NULL,
    book_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (check_id) REFERENCES check_sale(id),
    FOREIGN KEY (book_id) REFERENCES book(id)
);

-- Тестовые данные
INSERT INTO book (title, price) VALUES
('Book 1', 10.99),
('Book 2', 19.99),
('Book 3', 5.99),
('Book 4', 12.99);

INSERT INTO users (email, phone, password, birth_date, is_admin) VALUES
('admin@gmail.com', '123', 'password123', '1990-01-25', TRUE),
('user@gmail.com', '123', 'password123', '2003-11-19', FALSE);

INSERT INTO check_sale (user_id, sale_date) VALUES
(1, '2023-01-01 10:00:00'),
(2, '2023-01-02 11:00:00');

INSERT INTO check_sale_book (check_id, book_id, quantity) VALUES
(1, 1, 2),
(1, 2, 1),
(2, 3, 3),
(2, 4, 1);

-- Хранимые процедуры

-- ХП 1. Выводит почту, телефон клиента, общее количество купленных книг, общую сумму покупок за всё время.
DROP PROCEDURE IF EXISTS get_users_info;
DELIMITER //
CREATE PROCEDURE get_users_info()
BEGIN
    SELECT
        users.id,
        email,
        phone,
        SUM(quantity) AS total_quantity,
        SUM(price * quantity) AS total_price
    FROM
        check_sale
        INNER JOIN check_sale_book ON check_sale.id = check_sale_book.check_id
        INNER JOIN book ON check_sale_book.book_id = book.id
        INNER JOIN users ON check_sale.user_id = users.id
    GROUP BY
        check_sale.user_id;
END //
DELIMITER ;

-- ХП 2. Выводит для указанного клиента - фото, название книги, дату покупки, количество.
DROP PROCEDURE IF EXISTS get_user_check;
DELIMITER //
CREATE PROCEDURE get_user_check(IN p_user_id INT)
BEGIN
    SELECT
        book.photo,
        book.title,
        check_sale.sale_date,
        check_sale_book.quantity
    FROM
        check_sale
        INNER JOIN check_sale_book ON check_sale.id = check_sale_book.check_id
        INNER JOIN book ON check_sale_book.book_id = book.id
    WHERE
        check_sale.user_id = p_user_id;
END //
DELIMITER ;