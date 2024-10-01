--Создание

CREATE TABLE Brands (
    id INTEGER PRIMARY KEY,
		name VARCHAR(50) NOT NULL,
		descriptions TEXT NOT NULL,
);

CREATE TABLE Sneakers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    brand_id FOREIGN KEY REFERENCES Brands(id),
);

CREATE TABLE Orders (
    id INTEGER PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    order_date TIMESTAMP DEFAULT NOW(),
);

CREATE TABLE Order_sneakers (
		quantity INTEGER NOT NULL DEFAULT 1,
    order_id INTEGER FOREIGN KEY REFERENCES Orders(id),
    sneaker_id INTEGER FOREIGN KEY REFERENCES Sneakers(id),
    PRIMARY KEY (order_id, sneaker_id),
);

--Добавление

INSERT INTO Brands (id, name, description) VALUES 
	(1, 'Reebok', 'Good'), 
	(2, 'Adidas', 'Perfectly'), 
	(3, 'Puma', 'Wonderful!'), 
	(4, 'Fila', 'Cool'), 
	(5, 'Converse', 'Not bad'), 
	(6, 'Nike', 'Wonderful!'), 
	(7, 'Demix', 'I like it'), 
	(8, 'Asics', 'Interesting'), 
	(9, 'Kappa', 'Beautifully'), 
	(10, 'Gucci', 'Marvelous');

INSERT INTO Sneakers (id, name, price, brand_id) VALUES 
	(1, 'Club C Grounds', 75.00, 1), 
	(2, 'Air Max', 120.00, 3), 
	(3, 'UltraBoost', 180.00, 5), 
	(4, 'Suede Classic', 65.00, 2), 
	(5, '574 Core', 80.00, 4), 
	(6, 'Gel-Lyte III', 100.00, 8), 
	(7, 'PLAY COMME DES GARCONS', 150.00, 6), 
	(8, 'Old Skool', 60.00, 7), 
	(9, 'Disruptor 2', 85.00, 10), 
	(10, 'HOVR Phantom', 110.00, 9);

INSERT INTO Orders (id, amount) VALUES 
	(1, 1000), 
	(2, 1400), 
	(3, 5000), 
	(4, 1100), 
	(5, 5500), 
	(6, 61000), 
	(7, 5000);

INSERT INTO Order_sneakers (order_id, sneaker_id) VALUES 
	(1, 1),
	(1, 2),
	(2, 3),
	(2, 4),
	(3, 5),
	(4, 6),
	(5, 7);