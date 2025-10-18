CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    registration_date DATE
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    order_date DATE,
    status VARCHAR(20),
    amount NUMERIC(10,2),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price NUMERIC(10,2),
    stock_quantity INT
);

CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    price NUMERIC(10,2),
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    product_id INT REFERENCES products(product_id),
    review_text TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    CONSTRAINT fk_review_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_review_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO users (first_name, last_name, email, phone, registration_date) 
VALUES 
('Иван', 'Петров', 'petrov@mail.ru', '+79991234567', '2025-10-15'),
('Анна', 'Сидорова', 'anna@gmail.com', '+79123456789', '2025-10-12'),
('Михаил', 'Иванов', 'mikhail@mail.ru', '+79001234567', '2025-10-10');

INSERT INTO products (product_name, category, price, stock_quantity) 
VALUES 
('Смартфон', 'Электроника', 25000.00, 15),
('Ноутбук', 'Электроника', 65000.00, 8),
('Планшет', 'Электроника', 18000.00, 25);

INSERT INTO orders (user_id, order_date, status, amount) 
VALUES 
(1, '2025-10-15', 'Выполнен', 5000.00),
(2, '2025-10-16', 'В обработке', 3500.00),
(3, '2025-10-17', 'Ожидает оплаты', 7000.00);

INSERT INTO order_items (order_id, product_id, quantity, price) 
VALUES 
(1, 1, 2, 25000.00),
(2, 3, 1, 18000.00),
(3, 2, 1, 65000.00);

INSERT INTO reviews (user_id, product_id, review_text, rating) 
VALUES 
(1, 1, 'Отличный смартфон!', 5),
(3, 2, 'Быстро работает', 4),
(2, 3, 'Удобный планшет', 5);
