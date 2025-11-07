-- Add reviews and ratings table
CREATE TABLE IF NOT EXISTS `crop_reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `crop_id` int NOT NULL,
  `customer_id` int NOT NULL,
  `rating` int NOT NULL CHECK (rating >= 1 AND rating <= 5),
  `review_text` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_customer_crop` (`crop_id`, `customer_id`),
  KEY `crop_id` (`crop_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `crop_reviews_ibfk_1` FOREIGN KEY (`crop_id`) REFERENCES `crops` (`id`) ON DELETE CASCADE,
  CONSTRAINT `crop_reviews_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE CASCADE
);

-- Add average rating column to crops table (check if exists first)
SET @exist := (SELECT COUNT(*) FROM information_schema.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
    AND TABLE_NAME = 'crops' 
    AND COLUMN_NAME = 'average_rating');

SET @sqlstmt := IF(@exist = 0, 
    'ALTER TABLE crops ADD COLUMN average_rating DECIMAL(3,2) DEFAULT 0.00',
    'SELECT "Column average_rating already exists" AS message');
PREPARE stmt FROM @sqlstmt;
EXECUTE stmt;

SET @exist := (SELECT COUNT(*) FROM information_schema.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
    AND TABLE_NAME = 'crops' 
    AND COLUMN_NAME = 'review_count');

SET @sqlstmt := IF(@exist = 0, 
    'ALTER TABLE crops ADD COLUMN review_count INT DEFAULT 0',
    'SELECT "Column review_count already exists" AS message');
PREPARE stmt FROM @sqlstmt;
EXECUTE stmt;

-- Insert dummy data for testing
-- Dummy customers (password: password123)
INSERT INTO customers (name, phone, email, address, password, location) VALUES
('John Doe', '9876543210', 'john@example.com', '123 Main St, Koramangala', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 'Bangalore'),
('Jane Smith', '9876543211', 'jane@example.com', '456 Oak Ave, Jayanagar', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 'Mysore'),
('Bob Wilson', '9876543212', 'bob@example.com', '789 Pine Rd, Indiranagar', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 'Bangalore'),
('Alice Johnson', '9876543213', 'alice@example.com', '321 Elm St, Whitefield', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 'Bangalore'),
('Mike Brown', '9876543214', 'mike@example.com', '654 Maple Dr, HSR Layout', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 'Bangalore'),
('Sarah Davis', '9876543215', 'sarah@example.com', '987 Cedar Ln, Gokulam', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 'Mysore'),
('Tom Anderson', '9876543216', 'tom@example.com', '147 Birch Rd, Malleshwaram', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 'Bangalore'),
('Emma Wilson', '9876543217', 'emma@example.com', '258 Spruce Ave, Yelahanka', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 'Bangalore')
ON DUPLICATE KEY UPDATE name=name;

-- Dummy farmers (password: password123)
INSERT INTO farmers (name, age, phone, location, aadhar, password, profile_pic) VALUES
('Ravi Kumar', 45, '9123456780', 'Bangalore Rural', '123456789012', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 'farmer.jpg'),
('Lakshmi Devi', 38, '9123456781', 'Mysore', '123456789013', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 'farmer.jpg'),
('Suresh Reddy', 52, '9123456782', 'Mandya', '123456789014', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 'farmer.jpg'),
('Manjunath Gowda', 48, '9123456783', 'Hassan', '123456789015', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 'farmer.jpg'),
('Kavitha Naik', 42, '9123456784', 'Tumkur', '123456789016', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi', 'farmer.jpg')
ON DUPLICATE KEY UPDATE name=name;

-- Dummy crops with variety
INSERT INTO crops (farmer_id, crop_name, crop_type, quantity, price_per_kg, offer, offer_details, image) VALUES
-- Farmer 1 crops
(1, 'Tomato', 'Vegetable', 100, 30.00, 'Yes', '10% off on bulk orders above 10kg', 'tomato.jpg'),
(1, 'Potato', 'Vegetable', 150, 25.00, 'No', NULL, 'potato.jpg'),
(1, 'Onion', 'Vegetable', 120, 28.00, 'Yes', 'Buy 5kg get 500g free', 'tomato.jpg'),
-- Farmer 2 crops
(2, 'Watermelon', 'Fruit', 50, 40.00, 'Yes', 'Buy 2 get 1 free', 'water-melon.jpg'),
(2, 'Corn', 'Food Grains', 80, 35.00, 'No', NULL, 'corn.jpg'),
(2, 'Mango', 'Fruit', 60, 80.00, 'Yes', 'Premium Alphonso - 20% off', 'water-melon.jpg'),
-- Farmer 3 crops
(3, 'Chilli', 'Vegetable', 60, 50.00, 'Yes', '15% off this week only', 'chilli.jpg'),
(3, 'Brinjal', 'Vegetable', 70, 32.00, 'No', NULL, 'tomato.jpg'),
(3, 'Beetroot', 'Vegetable', 45, 35.00, 'Yes', 'Fresh harvest - 10% off', 'tomato.jpg'),
-- Farmer 4 crops
(4, 'Carrot', 'Vegetable', 90, 38.00, 'No', NULL, 'tomato.jpg'),
(4, 'Cabbage', 'Vegetable', 55, 22.00, 'Yes', 'Weekend special - 15% off', 'tomato.jpg'),
(4, 'Rice', 'Food Grains', 200, 45.00, 'Yes', 'Organic rice - Buy 10kg get 1kg free', 'corn.jpg'),
-- Farmer 5 crops
(5, 'Banana', 'Fruit', 100, 35.00, 'No', NULL, 'water-melon.jpg'),
(5, 'Papaya', 'Fruit', 40, 30.00, 'Yes', 'Ripe and ready - 10% off', 'water-melon.jpg'),
(5, 'Cucumber', 'Vegetable', 65, 20.00, 'No', NULL, 'tomato.jpg')
ON DUPLICATE KEY UPDATE crop_name=crop_name;

-- Dummy recipes with more variety
INSERT INTO recipes (recipe_name, image, ingredients, masala_cost, cooking_instructions, main_items, created_by) VALUES
('Tomato Curry', 'tomato_curry.webp', 'Tomatoes, Onions, Garlic, Ginger, Turmeric, Red Chilli, Coriander', 50.00, 'Heat oil, add onions and garlic, add tomatoes, add spices, cook for 15 minutes', 'Tomato', 1),
('Potato Fry', 'aloo-fry-3.webp', 'Potatoes, Turmeric, Chilli powder, Salt, Curry leaves', 40.00, 'Cut potatoes, fry with spices until golden brown', 'Potato', 1),
('Corn Curry', 'Sweetcorn_Curry_4.JPG', 'Sweet Corn, Coconut, Green Chillies, Cumin, Mustard seeds', 60.00, 'Boil corn, prepare coconut gravy, mix and cook', 'Corn', 1),
('Beetroot Halwa', 'Beetroot_halwa.jpeg', 'Beetroot, Milk, Sugar, Ghee, Cardamom, Cashews', 70.00, 'Grate beetroot, cook with milk and sugar, add ghee and nuts', 'Beetroot', 1),
('Brinjal Masala', 'Brinjal_masala.jpeg', 'Brinjal, Onion, Tomato, Peanuts, Sesame, Spices', 55.00, 'Roast masala, stuff brinjals, cook until tender', 'Brinjal', 1),
('Drumstick Sambar', 'Drumstick_sambar.jpeg', 'Drumstick, Toor dal, Tamarind, Sambar powder, Vegetables', 65.00, 'Cook dal, add vegetables and drumstick, temper with spices', 'Drumstick', 1),
('Tomato Rice', 'Tomato_rice.jpeg', 'Rice, Tomatoes, Onions, Spices, Mint, Coriander', 45.00, 'Cook rice, prepare tomato masala, mix together', 'Tomato,Rice', 1),
('Beetroot Rice', 'Beetroot_rice.jpeg', 'Rice, Beetroot, Onions, Spices, Lemon', 50.00, 'Cook rice with grated beetroot and spices', 'Beetroot,Rice', 1)
ON DUPLICATE KEY UPDATE recipe_name=recipe_name;

-- Dummy employees (password: password123)
INSERT INTO employees (name, email, phone, house_address, location, password) VALUES
('Priya Sharma', 'priya@example.com', '9234567890', '12 Garden Street, Koramangala', 'Bangalore', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi'),
('Anita Rao', 'anita@example.com', '9234567891', '45 Lake View, Gokulam', 'Mysore', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi'),
('Meena Patel', 'meena@example.com', '9234567892', '78 Temple Road, Jayanagar', 'Bangalore', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi'),
('Rekha Nair', 'rekha@example.com', '9234567893', '23 Park Avenue, Indiranagar', 'Bangalore', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWU7u3oi')
ON DUPLICATE KEY UPDATE name=name;

-- Dummy cooked foods with variety
INSERT INTO cooked_foods (employee_id, food_name, image, main_items, cooked_time, price) VALUES
-- Priya's foods
(1, 'Tomato Rice', 'Tomato_rice.jpeg', 'Rice, Tomato', NOW(), 80.00),
(1, 'Beetroot Fry', 'Beetroot_fry.jpeg', 'Beetroot', NOW(), 60.00),
(1, 'Potato Chips', 'potato-chips.jpg', 'Potato', NOW(), 50.00),
-- Anita's foods
(2, 'Brinjal Curry', 'Brinjal_curry.jpeg', 'Brinjal', NOW(), 70.00),
(2, 'Drumstick Sambar', 'Drumstick_sambar.jpeg', 'Drumstick', NOW(), 75.00),
(2, 'Tomato Pickle', 'Tomato_pickle.jpeg', 'Tomato', NOW(), 90.00),
-- Meena's foods
(3, 'Beetroot Halwa', 'Beetroot_halwa.jpeg', 'Beetroot', NOW(), 100.00),
(3, 'Corn Curry', 'Sweetcorn_Curry_4.JPG', 'Corn', NOW(), 85.00),
(3, 'Brinjal Biryani', 'Brinjal_biryani.jpeg', 'Brinjal, Rice', NOW(), 120.00),
-- Rekha's foods
(4, 'Tomato Rasam', 'Tomato_rasam.jpeg', 'Tomato', NOW(), 60.00),
(4, 'Beetroot Juice', 'beetroot_juice.jpeg', 'Beetroot', NOW(), 40.00),
(4, 'Brinjal Chutney', 'Brinjal_chutney.jpeg', 'Brinjal', NOW(), 55.00)
ON DUPLICATE KEY UPDATE food_name=food_name;

-- Dummy reviews for crops
INSERT INTO crop_reviews (crop_id, customer_id, rating, review_text, created_at) VALUES
-- Reviews for Tomato (crop_id 1)
(1, 1, 5, 'Excellent quality tomatoes! Very fresh and juicy.', DATE_SUB(NOW(), INTERVAL 5 DAY)),
(1, 2, 4, 'Good quality, but slightly expensive.', DATE_SUB(NOW(), INTERVAL 4 DAY)),
(1, 3, 5, 'Best tomatoes I have bought online. Will order again!', DATE_SUB(NOW(), INTERVAL 3 DAY)),
(1, 4, 4, 'Fresh and tasty. Good for cooking.', DATE_SUB(NOW(), INTERVAL 2 DAY)),
-- Reviews for Potato (crop_id 2)
(2, 2, 4, 'Nice potatoes, good for frying.', DATE_SUB(NOW(), INTERVAL 6 DAY)),
(2, 5, 4, 'Fresh and clean. Good quality.', DATE_SUB(NOW(), INTERVAL 3 DAY)),
(2, 6, 5, 'Perfect for making chips!', DATE_SUB(NOW(), INTERVAL 1 DAY)),
-- Reviews for Watermelon (crop_id 4)
(4, 1, 5, 'Super sweet and juicy watermelon!', DATE_SUB(NOW(), INTERVAL 7 DAY)),
(4, 3, 5, 'Best watermelon ever! Kids loved it.', DATE_SUB(NOW(), INTERVAL 5 DAY)),
(4, 7, 5, 'Very fresh and sweet. Highly recommended!', DATE_SUB(NOW(), INTERVAL 2 DAY)),
(4, 8, 4, 'Good quality, slightly small size.', DATE_SUB(NOW(), INTERVAL 1 DAY)),
-- Reviews for Corn (crop_id 5)
(5, 4, 4, 'Fresh corn, good for boiling.', DATE_SUB(NOW(), INTERVAL 4 DAY)),
(5, 5, 5, 'Sweet and tender corn. Excellent!', DATE_SUB(NOW(), INTERVAL 2 DAY)),
-- Reviews for Chilli (crop_id 7)
(7, 2, 5, 'Very spicy and fresh chillies!', DATE_SUB(NOW(), INTERVAL 6 DAY)),
(7, 6, 4, 'Good quality, perfect spice level.', DATE_SUB(NOW(), INTERVAL 3 DAY))
ON DUPLICATE KEY UPDATE review_text=review_text;

-- Update crop ratings based on reviews
UPDATE crops c
SET c.average_rating = (
    SELECT AVG(rating) 
    FROM crop_reviews cr 
    WHERE cr.crop_id = c.id
),
c.review_count = (
    SELECT COUNT(*) 
    FROM crop_reviews cr 
    WHERE cr.crop_id = c.id
)
WHERE c.id IN (SELECT DISTINCT crop_id FROM crop_reviews);
