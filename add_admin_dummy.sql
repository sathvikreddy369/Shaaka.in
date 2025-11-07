-- Add admin account for testing (password: password123)
INSERT INTO admin (username, email, password, is_admin) VALUES
('admin', 'admin@farmermarket.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 1),
('superadmin', 'superadmin@farmermarket.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 1)
ON DUPLICATE KEY UPDATE username=username;

-- Add some sample orders for testing
INSERT INTO orders (customer_id, address, total_cost, status, created_at) VALUES
(1, '123 Main St, Koramangala, Bangalore', 180.00, 'Delivered', DATE_SUB(NOW(), INTERVAL 10 DAY)),
(1, '123 Main St, Koramangala, Bangalore', 250.00, 'Delivered', DATE_SUB(NOW(), INTERVAL 7 DAY)),
(2, '456 Oak Ave, Jayanagar, Mysore', 320.00, 'Placed', DATE_SUB(NOW(), INTERVAL 3 DAY)),
(3, '789 Pine Rd, Indiranagar, Bangalore', 150.00, 'Delivered', DATE_SUB(NOW(), INTERVAL 5 DAY)),
(4, '321 Elm St, Whitefield, Bangalore', 420.00, 'Placed', DATE_SUB(NOW(), INTERVAL 2 DAY)),
(5, '654 Maple Dr, HSR Layout, Bangalore', 280.00, 'Delivered', DATE_SUB(NOW(), INTERVAL 8 DAY))
ON DUPLICATE KEY UPDATE customer_id=customer_id;

-- Add some cart items for testing (for customer 1)
INSERT INTO cart (customer_id, crop_id, quantity, price) VALUES
(1, 1, 2, 30.00),
(1, 4, 1, 40.00)
ON DUPLICATE KEY UPDATE quantity=quantity;

-- Add some recipe cart items
INSERT INTO recipe_cart (customer_id, recipe_id, recipe_name, image, masala_cost, quantity) VALUES
(1, 1, 'Tomato Curry', 'tomato_curry.webp', 50.00, 1),
(2, 2, 'Potato Fry', 'aloo-fry-3.webp', 40.00, 2)
ON DUPLICATE KEY UPDATE quantity=quantity;

-- Add some food cart items
INSERT INTO food_cart (customer_id, food_id, quantity) VALUES
(2, 1, 2),
(2, 4, 1),
(3, 2, 1)
ON DUPLICATE KEY UPDATE quantity=quantity;

-- Add some customer orders for employees
INSERT INTO customer_orders (food_id, customer_id, quantity, ordered_time, status, employee_id, address, total_cost) VALUES
(1, 1, 2, DATE_SUB(NOW(), INTERVAL 2 HOUR), 'pending', 1, '123 Main St, Koramangala, Bangalore', 160.00),
(4, 2, 1, DATE_SUB(NOW(), INTERVAL 5 HOUR), 'pending', 2, '456 Oak Ave, Jayanagar, Mysore', 70.00),
(7, 3, 1, DATE_SUB(NOW(), INTERVAL 1 DAY), 'ready to dispatch', 3, '789 Pine Rd, Indiranagar, Bangalore', 100.00),
(10, 4, 2, DATE_SUB(NOW(), INTERVAL 3 HOUR), 'pending', 4, '321 Elm St, Whitefield, Bangalore', 120.00)
ON DUPLICATE KEY UPDATE food_id=food_id;

-- Add some temporary addresses for customers
INSERT INTO temporary_addresses (customer_id, address) VALUES
(1, 'Office: Tech Park, Whitefield, Bangalore'),
(1, 'Parents House: 45 MG Road, Bangalore'),
(2, 'Work: IT Park, Mysore'),
(3, 'Friends Place: 12 Brigade Road, Bangalore')
ON DUPLICATE KEY UPDATE address=address;

-- Update some crops with sold quantity and customer count
UPDATE crops SET sold_quantity = 50, customer_count = 8 WHERE id = 1;
UPDATE crops SET sold_quantity = 75, customer_count = 12 WHERE id = 2;
UPDATE crops SET sold_quantity = 30, customer_count = 15 WHERE id = 4;
UPDATE crops SET sold_quantity = 40, customer_count = 9 WHERE id = 5;
UPDATE crops SET sold_quantity = 25, customer_count = 11 WHERE id = 7;
