-- Update crops table to support new product categories
ALTER TABLE crops 
MODIFY COLUMN crop_type ENUM(
    'Vegetable', 
    'Fruit', 
    'Food Grains',
    'Homemade Food',
    'Grocery',
    'Poultry',
    'Dairy',
    'Meat'
) NOT NULL;

-- Add new columns for additional product details (check if they exist first)
ALTER TABLE crops ADD COLUMN brand VARCHAR(100) DEFAULT NULL;
ALTER TABLE crops ADD COLUMN unit VARCHAR(50) DEFAULT 'kg';
ALTER TABLE crops ADD COLUMN expiry_date DATE DEFAULT NULL;
ALTER TABLE crops ADD COLUMN manufacturing_date DATE DEFAULT NULL;
ALTER TABLE crops ADD COLUMN organic_certified BOOLEAN DEFAULT TRUE;

-- Insert dummy data for testing

-- Homemade Products
INSERT INTO crops (farmer_id, crop_name, crop_type, quantity, price_per_kg, unit, image, description, place_of_origin, organic_certified) VALUES
(1, 'Homemade Pickles', 'Homemade Food', 50, 150, 'jar', 'pickle.jpg', 'Traditional Indian pickles made with organic ingredients', 'Bangalore', TRUE),
(1, 'Fresh Ghee', 'Homemade Food', 30, 500, 'kg', 'ghee.jpg', 'Pure homemade ghee from organic milk', 'Mysore', TRUE),
(1, 'Homemade Papad', 'Homemade Food', 100, 80, 'pack', 'papad.jpg', 'Crispy traditional papads', 'Hassan', TRUE);

-- Groceries
INSERT INTO crops (farmer_id, crop_name, crop_type, quantity, price_per_kg, unit, image, description, place_of_origin, organic_certified) VALUES
(1, 'Organic Rice', 'Grocery', 500, 80, 'kg', 'rice.jpg', 'Premium organic basmati rice', 'Punjab', TRUE),
(1, 'Organic Wheat Flour', 'Grocery', 300, 45, 'kg', 'wheat.jpg', 'Stone ground organic wheat flour', 'Haryana', TRUE),
(1, 'Organic Pulses (Toor Dal)', 'Grocery', 200, 120, 'kg', 'dal.jpg', 'Organic toor dal', 'Maharashtra', TRUE),
(1, 'Organic Sugar', 'Grocery', 150, 50, 'kg', 'sugar.jpg', 'Organic cane sugar', 'Karnataka', TRUE),
(1, 'Rock Salt', 'Grocery', 100, 30, 'kg', 'salt.jpg', 'Natural rock salt', 'Himachal', TRUE);

-- Poultry
INSERT INTO crops (farmer_id, crop_name, crop_type, quantity, price_per_kg, unit, image, description, place_of_origin, organic_certified) VALUES
(1, 'Farm Fresh Eggs', 'Poultry', 500, 8, 'piece', 'eggs.jpg', 'Free range organic eggs', 'Local Farm', TRUE),
(1, 'Country Chicken', 'Poultry', 50, 350, 'kg', 'chicken.jpg', 'Free range country chicken', 'Local Farm', TRUE),
(1, 'Duck Eggs', 'Poultry', 200, 12, 'piece', 'duck_eggs.jpg', 'Fresh duck eggs', 'Local Farm', TRUE);

-- Dairy Products
INSERT INTO crops (farmer_id, crop_name, crop_type, quantity, price_per_kg, unit, image, description, place_of_origin, organic_certified) VALUES
(1, 'Fresh Cow Milk', 'Dairy', 200, 60, 'liter', 'milk.jpg', 'Fresh organic cow milk', 'Local Dairy', TRUE),
(1, 'Buffalo Milk', 'Dairy', 150, 70, 'liter', 'buffalo_milk.jpg', 'Rich buffalo milk', 'Local Dairy', TRUE),
(1, 'Pure Desi Ghee', 'Dairy', 80, 600, 'kg', 'desi_ghee.jpg', 'Pure desi ghee from cow milk', 'Local Dairy', TRUE),
(1, 'A2 Cow Ghee', 'Dairy', 50, 800, 'kg', 'a2_ghee.jpg', 'Premium A2 cow ghee', 'Local Dairy', TRUE),
(1, 'White Butter', 'Dairy', 60, 400, 'kg', 'butter.jpg', 'Fresh white butter', 'Local Dairy', TRUE),
(1, 'Fresh Paneer', 'Dairy', 100, 300, 'kg', 'paneer.jpg', 'Soft fresh paneer', 'Local Dairy', TRUE),
(1, 'Curd (Dahi)', 'Dairy', 150, 50, 'kg', 'curd.jpg', 'Fresh homemade curd', 'Local Dairy', TRUE);

-- Meat Products
INSERT INTO crops (farmer_id, crop_name, crop_type, quantity, price_per_kg, unit, image, description, place_of_origin, organic_certified) VALUES
(1, 'Fresh Chicken', 'Meat', 100, 280, 'kg', 'fresh_chicken.jpg', 'Fresh broiler chicken', 'Local Farm', FALSE),
(1, 'Mutton', 'Meat', 50, 650, 'kg', 'mutton.jpg', 'Fresh mutton', 'Local Farm', FALSE),
(1, 'Fish (Rohu)', 'Meat', 80, 350, 'kg', 'fish.jpg', 'Fresh water fish', 'Local Farm', FALSE);

-- Update existing products with units
UPDATE crops SET unit = 'kg' WHERE unit IS NULL OR unit = '';
UPDATE crops SET organic_certified = TRUE WHERE crop_type IN ('Vegetable', 'Fruit', 'Food Grains');
