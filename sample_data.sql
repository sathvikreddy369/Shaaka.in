-- Sample Data for Shaaka Platform
-- This file contains mock data for testing

USE farmer_market;

-- Insert sample admin (password: password123)
INSERT INTO admin (username, email, password) VALUES
('admin', 'admin@farmermarket.com', 'scrypt:32768:8:1$vK8ZGxQYHqJ5rXmL$8f5e3c9a1b2d4e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f')
ON DUPLICATE KEY UPDATE username=username;

-- Insert sample customers (password: password123)
INSERT INTO customers (name, phone, email, password, address, latitude, longitude) VALUES
('John Doe', '9876543210', 'customer@example.com', 'scrypt:32768:8:1$vK8ZGxQYHqJ5rXmL$8f5e3c9a1b2d4e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', '123 Main Street, Bangalore', 12.9716, 77.5946),
('Priya Sharma', '9876543211', 'priya@example.com', 'scrypt:32768:8:1$vK8ZGxQYHqJ5rXmL$8f5e3c9a1b2d4e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', '456 Park Avenue, Bangalore', 12.9716, 77.5946),
('Rajesh Kumar', '9876543212', 'rajesh@example.com', 'scrypt:32768:8:1$vK8ZGxQYHqJ5rXmL$8f5e3c9a1b2d4e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', '789 Lake Road, Mysore', 12.2958, 76.6394)
ON DUPLICATE KEY UPDATE name=name;

-- Insert sample farmers (password: password123)
INSERT INTO farmers (name, phone, email, password, location, latitude, longitude) VALUES
('Farmer Ravi', '9876543220', 'farmer@example.com', 'scrypt:32768:8:1$vK8ZGxQYHqJ5rXmL$8f5e3c9a1b2d4e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'Kanakapura Road, Bangalore', 12.8698, 77.5802),
('Farmer Lakshmi', '9876543221', 'lakshmi@example.com', 'scrypt:32768:8:1$vK8ZGxQYHqJ5rXmL$8f5e3c9a1b2d4e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'Mandya District', 12.5244, 76.8958),
('Farmer Suresh', '9876543222', 'suresh@example.com', 'scrypt:32768:8:1$vK8ZGxQYHqJ5rXmL$8f5e3c9a1b2d4e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'Hassan District', 13.0033, 76.0977)
ON DUPLICATE KEY UPDATE name=name;

-- Insert sample employees/homemakers (password: password123)
INSERT INTO employees (name, phone, email, password, address) VALUES
('Homemaker Anita', '9876543230', 'homemaker@example.com', 'scrypt:32768:8:1$vK8ZGxQYHqJ5rXmL$8f5e3c9a1b2d4e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'Jayanagar, Bangalore'),
('Homemaker Meera', '9876543231', 'meera@example.com', 'scrypt:32768:8:1$vK8ZGxQYHqJ5rXmL$8f5e3c9a1b2d4e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f', 'Indiranagar, Bangalore')
ON DUPLICATE KEY UPDATE name=name;

-- Insert sample crops/products
INSERT INTO crops (farmer_id, crop_name, crop_type, quantity, price_per_kg, mrp, discount, description, image, place_of_origin, delivery_days, is_available) VALUES
(1, 'Organic Tomatoes', 'Vegetable', 100, 40, 50, 20, 'Fresh organic tomatoes grown without pesticides', 'tomato.jpg', 'Bangalore', 1, 1),
(1, 'Organic Spinach', 'Vegetable', 50, 30, 40, 25, 'Nutrient-rich organic spinach leaves', 'spinach.jpg', 'Bangalore', 1, 1),
(2, 'Organic Carrots', 'Vegetable', 80, 45, 55, 18, 'Crunchy organic carrots full of vitamins', 'carrot.jpg', 'Mandya', 2, 1),
(2, 'Organic Bananas', 'Fruit', 120, 35, 45, 22, 'Sweet organic bananas from local farms', 'banana.jpg', 'Mandya', 1, 1),
(3, 'Organic Mangoes', 'Fruit', 60, 80, 100, 20, 'Delicious organic Alphonso mangoes', 'mango.jpg', 'Hassan', 2, 1),
(3, 'Organic Potatoes', 'Vegetable', 150, 25, 30, 17, 'Fresh organic potatoes for daily cooking', 'potato.jpg', 'Hassan', 1, 1)
ON DUPLICATE KEY UPDATE crop_name=crop_name;

-- Insert sample food items from homemakers
INSERT INTO food_items (employee_id, food_name, description, price, quantity, image, is_available) VALUES
(1, 'Homemade Idli Batter', 'Fresh idli batter made with organic rice and urad dal', 80, 20, 'idli_batter.jpg', 1),
(1, 'Homemade Pickles', 'Traditional mango pickle made with organic ingredients', 150, 15, 'pickle.jpg', 1),
(2, 'Fresh Chapatis', 'Soft whole wheat chapatis made fresh daily', 60, 30, 'chapati.jpg', 1),
(2, 'Homemade Sweets', 'Traditional Indian sweets made with pure ghee', 200, 10, 'sweets.jpg', 1)
ON DUPLICATE KEY UPDATE food_name=food_name;

-- Insert sample reviews
INSERT INTO reviews (crop_id, customer_id, rating, review_text) VALUES
(1, 1, 5, 'Excellent quality tomatoes! Very fresh and tasty.'),
(1, 2, 5, 'Best organic tomatoes I have ever bought. Will order again!'),
(2, 1, 4, 'Good quality spinach, very fresh.'),
(3, 3, 5, 'Carrots are crunchy and sweet. Highly recommended!'),
(4, 2, 5, 'Perfect bananas for my kids. They loved it!'),
(5, 3, 5, 'Amazing mangoes! Worth every penny.')
ON DUPLICATE KEY UPDATE rating=rating;

-- Update average ratings for crops
UPDATE crops c SET average_rating = (
    SELECT AVG(rating) FROM reviews WHERE crop_id = c.id
) WHERE id IN (SELECT DISTINCT crop_id FROM reviews);

SELECT 'Sample data inserted successfully!' as Status;
SELECT 'Login Credentials:' as Info;
SELECT 'Admin: admin@farmermarket.com / password123' as Admin;
SELECT 'Customer: customer@example.com / password123' as Customer;
SELECT 'Farmer: farmer@example.com / password123' as Farmer;
SELECT 'Homemaker: homemaker@example.com / password123' as Homemaker;
