	-- Создание таблицы brands и вставка данных
CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

INSERT INTO brands (id, name, description) VALUES
	(1, 'Reebok', 'Иконический бренд с богатой историей.'),
	(2, 'Adidas', 'Качественная обувь для профессиональных спортсменов.'),
	(3, 'Puma', 'Стиль и инновации в каждой модели.'),
	(4, 'Fila', 'Доступные цены без потери качества.'),
	(5, 'Converse', 'Лидер в мире кроссовок и активной одежды.'),
	(6, 'Nike', 'Экологичные материалы для ответственного потребления.'),
	(7, 'Demix', 'Популярный среди молодежи и модников.'),
	(8, 'Asics', 'Специальные коллекции для уникального стиля.'),
	(9, 'Kappa', 'Комфорт и производительность в каждой паре.'),
	(10, 'Gucci', 'Бренд, который вдохновляет на движение.');

-- Создание таблицы sneakers и вставка данных
CREATE TABLE sneakers (
    id SERIAL PRIMARY KEY,
    size DECIMAL(3, 1) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    brand_id INT REFERENCES brands(id)
);

INSERT INTO sneakers (id, size, name, description, price, brand_id) VALUES
	(1, 30, 'Club C Grounds', 'Легкие и стильные кроссовки для бега.', 75.00, 1),
	(2, 31, 'Air Max', 'Удобная обувь с хорошей амортизацией.', 120.00, 3),
	(3, 32, 'UltraBoost', 'Элегантный дизайн для повседневной носки.', 180.00, 5),
	(4, 33, 'Suede Classic', 'Дышащая сетка, идеальная для лета.', 65.00, 2),
	(5, 34, '574 Core', 'Прочные материалы для долгого использования.', 80.00, 4),
	(6, 35, 'Gel-Lyte III', 'Кроссовки с ярким логотипом на боках.', 100.00, 8),
	(7, 36, 'PLAY COMME DES GARCONS', 'Отличное сцепление для активного отдыха.', 150.00, 6),
	(8, 37, 'Old Skool', 'Спортивная обувь с уникальным цветовым решением.', 60.00, 7),
	(9, 38, 'Disruptor 2', 'Мягкая подошва для комфорта и поддержки.', 85.00, 10),
	(10, 39, 'HOVR Phantom', 'Идеальный выбор для тренировки и прогулок.', 110.00, 9);

-- Создание таблицы orders и вставка данных
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    name_customer VARCHAR(255) NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    pickup_code TEXT NOT NULL
);

INSERT INTO orders (id, name_customer, pickup_code) VALUES 
	(1, "John", "1351147641"), 
	(2, "Maria", "61441147411"), 
	(3, "David", "1461147461"), 
	(4, "Joseph", "1464717447174"),
	(5, "Robert", "14716471747"), 
	(6, "Lola", "147417147417"),
	(7, "Olga", "717857221785");

-- Создание таблицы orders_sneakers и вставка данных
CREATE TABLE orders_sneakers (
    order_id INT REFERENCES orders(id),
    sneaker_id INT REFERENCES sneakers(id),
    quantity INT NOT NULL DEFAULT 1,
    price DECIMAL(10, 2),
    PRIMARY KEY (order_id, sneaker_id)
);

INSERT INTO orders_sneakers (order_id, sneaker_id, quantity, price) VALUES
	(1, 1, 1, 1000),
	(1, 2, 3, 1200),
	(2, 3, 100, 1300),
	(2, 4, 2, 1400),
	(3, 5, 1, 1500),
	(4, 6, 1, 1600),
	(5, 7, 1, 1700);

-- Создание таблицы payment и вставка данных
CREATE TABLE payment (
    id SERIAL PRIMARY KEY,
    status VARCHAR(50) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    order_id INT REFERENCES orders(id),
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO payment (id, status, provider, order_id) VALUES
	(1, 'paid', 'Tinkoff', 1),
	(2, 'paid', 'Alfa', 2),
	(3, 'paid', 'Tochka', 3),
	(4, 'paid', 'Sberbank', 4),
	(5, 'paid', 'Tochka', 5),
	(6, 'paid', 'Sberbank', 6),
	(7, 'paid', 'Alfa', 7);
