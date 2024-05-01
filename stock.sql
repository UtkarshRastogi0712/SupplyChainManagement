-- Inserting 30 rows of stock data with specific warehouse and product assignment
INSERT INTO stock (pid, wid, available_units) 
VALUES 
-- Warehouse A (ID: 1)
(1, 1, 100), (2, 1, 150), (3, 1, 200), (4, 1, 50), (5, 1, 100),
-- Warehouse B (ID: 2)
(6, 2, 150), (7, 2, 200), (8, 2, 50), (9, 2, 100), (10, 2, 150),
-- Warehouse C (ID: 3)
(11, 3, 100), (12, 3, 150), (13, 3, 200), (14, 3, 50), (15, 3, 100),
-- Warehouse D (ID: 4)
(16, 4, 100), (17, 4, 150), (18, 4, 200), (19, 4, 50), (20, 4, 100), 
(1, 4, 150), (2, 4, 200), (3, 4, 50), (4, 4, 100), (5, 4, 150),
-- Warehouse E (ID: 5)
(6, 5, 200), (7, 5, 250), (8, 5, 300), (9, 5, 200), (10, 5, 250);
