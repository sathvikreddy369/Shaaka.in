-- Enhanced Schema for Shaaka Application
-- Run this to add all new fields and tables

-- Add new fields to crops table
ALTER TABLE crops 
ADD COLUMN IF NOT EXISTS discount DECIMAL(5,2) DEFAULT 0.00 COMMENT 'Discount percentage',
ADD COLUMN IF NOT EXISTS mrp DECIMAL(10,2) DEFAULT 0.00 COMMENT 'Maximum Retail Price',
ADD COLUMN IF NOT EXISTS delivery_days INT DEFAULT 2 COMMENT 'Number of days for delivery',
ADD COLUMN IF NOT EXISTS place_of_origin VARCHAR(255) DEFAULT NULL COMMENT 'Where the crop is grown',
ADD COLUMN IF NOT EXISTS description TEXT DEFAULT NULL COMMENT 'Detailed product description',
ADD COLUMN IF NOT EXISTS is_available TINYINT(1) DEFAULT 1 COMMENT '1=In Stock, 0=Out of Stock',
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Create customer addresses table
CREATE TABLE IF NOT EXISTS customer_addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    address_type ENUM('Home', 'Work', 'Other') DEFAULT 'Home',
    house_number VARCHAR(100),
    area VARCHAR(255),
    landmark VARCHAR(255),
    pincode VARCHAR(10),
    city VARCHAR(100),
    district VARCHAR(100),
    state VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    is_default TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_customer (customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Add mobile number to customers if not exists
ALTER TABLE customers 
ADD COLUMN IF NOT EXISTS alternate_phone VARCHAR(15) DEFAULT NULL,
ADD COLUMN IF NOT EXISTS profile_image VARCHAR(255) DEFAULT 'default-avatar.png';

-- Create offers table for admin-managed offers
CREATE TABLE IF NOT EXISTS product_offers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    crop_id INT NOT NULL,
    offer_name VARCHAR(255) NOT NULL,
    discount_percentage DECIMAL(5,2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_by INT COMMENT 'Admin ID who created the offer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE CASCADE,
    INDEX idx_crop (crop_id),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create sales analytics table
CREATE TABLE IF NOT EXISTS sales_analytics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id INT NOT NULL,
    crop_id INT NOT NULL,
    customer_id INT NOT NULL,
    quantity_sold INT NOT NULL,
    sale_amount DECIMAL(10,2) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmers(id) ON DELETE CASCADE,
    FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_farmer (farmer_id),
    INDEX idx_crop (crop_id),
    INDEX idx_date (sale_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create admin activity log
CREATE TABLE IF NOT EXISTS admin_activity_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    description TEXT,
    target_id INT COMMENT 'ID of affected entity',
    target_type VARCHAR(50) COMMENT 'Type of entity (crop, user, etc)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admin(id) ON DELETE CASCADE,
    INDEX idx_admin (admin_id),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Update existing crops with new fields (set defaults)
UPDATE crops 
SET mrp = price_per_kg * 1.2,
    discount = 0,
    delivery_days = 2,
    place_of_origin = location,
    description = CONCAT('Fresh ', crop_name, ' directly from local farmers'),
    is_available = IF(quantity > 0, 1, 0)
WHERE mrp IS NULL OR mrp = 0;

-- Create trigger to auto-update average rating when review is added
DELIMITER //

DROP TRIGGER IF EXISTS update_crop_rating_after_insert//
CREATE TRIGGER update_crop_rating_after_insert
AFTER INSERT ON crop_reviews
FOR EACH ROW
BEGIN
    UPDATE crops 
    SET average_rating = (
        SELECT AVG(rating) FROM crop_reviews WHERE crop_id = NEW.crop_id
    ),
    review_count = (
        SELECT COUNT(*) FROM crop_reviews WHERE crop_id = NEW.crop_id
    )
    WHERE id = NEW.crop_id;
END//

DROP TRIGGER IF EXISTS update_crop_rating_after_update//
CREATE TRIGGER update_crop_rating_after_update
AFTER UPDATE ON crop_reviews
FOR EACH ROW
BEGIN
    UPDATE crops 
    SET average_rating = (
        SELECT AVG(rating) FROM crop_reviews WHERE crop_id = NEW.crop_id
    ),
    review_count = (
        SELECT COUNT(*) FROM crop_reviews WHERE crop_id = NEW.crop_id
    )
    WHERE id = NEW.crop_id;
END//

DROP TRIGGER IF EXISTS update_crop_rating_after_delete//
CREATE TRIGGER update_crop_rating_after_delete
AFTER DELETE ON crop_reviews
FOR EACH ROW
BEGIN
    UPDATE crops 
    SET average_rating = COALESCE((
        SELECT AVG(rating) FROM crop_reviews WHERE crop_id = OLD.crop_id
    ), 0),
    review_count = (
        SELECT COUNT(*) FROM crop_reviews WHERE crop_id = OLD.crop_id
    )
    WHERE id = OLD.crop_id;
END//

-- Create trigger to update crop quantity after purchase
DROP TRIGGER IF EXISTS update_crop_quantity_after_sale//
CREATE TRIGGER update_crop_quantity_after_sale
AFTER INSERT ON sales_analytics
FOR EACH ROW
BEGIN
    UPDATE crops 
    SET quantity = quantity - NEW.quantity_sold,
        sold_quantity = sold_quantity + NEW.quantity_sold,
        is_available = IF(quantity - NEW.quantity_sold > 0, 1, 0)
    WHERE id = NEW.crop_id;
END//

DELIMITER ;

-- Add some sample data for new fields
UPDATE crops SET 
    discount = CASE 
        WHEN offer = 'Yes' THEN FLOOR(10 + RAND() * 20)
        ELSE 0 
    END,
    delivery_days = FLOOR(1 + RAND() * 4),
    description = CASE crop_name
        WHEN 'Tomato' THEN 'Fresh, juicy tomatoes perfect for cooking. Rich in vitamins and antioxidants.'
        WHEN 'Potato' THEN 'High-quality potatoes ideal for all types of cooking. Freshly harvested.'
        WHEN 'Onion' THEN 'Premium quality onions with strong flavor. Essential for every kitchen.'
        WHEN 'Watermelon' THEN 'Sweet and refreshing watermelons. Perfect for hot summer days.'
        WHEN 'Corn' THEN 'Sweet corn kernels packed with nutrients. Great for salads and cooking.'
        WHEN 'Mango' THEN 'Premium Alphonso mangoes. Sweet, juicy, and aromatic.'
        WHEN 'Chilli' THEN 'Fresh green chillies with perfect spice level. Adds flavor to any dish.'
        WHEN 'Brinjal' THEN 'Fresh brinjals (eggplant) perfect for curries and fries.'
        WHEN 'Beetroot' THEN 'Organic beetroots rich in iron and nutrients. Great for health.'
        WHEN 'Carrot' THEN 'Crunchy carrots loaded with vitamin A. Perfect for salads.'
        WHEN 'Cabbage' THEN 'Fresh cabbage heads perfect for salads and cooking.'
        WHEN 'Rice' THEN 'Premium quality organic rice. Aromatic and nutritious.'
        WHEN 'Banana' THEN 'Fresh bananas rich in potassium. Perfect healthy snack.'
        WHEN 'Papaya' THEN 'Ripe papayas rich in vitamins. Great for digestion.'
        WHEN 'Cucumber' THEN 'Fresh cucumbers perfect for salads. Hydrating and healthy.'
        ELSE CONCAT('Fresh ', crop_name, ' from local farms')
    END;

SELECT 'Enhanced schema applied successfully!' AS status;
