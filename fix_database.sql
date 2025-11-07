-- Fix Database Schema for Shaaka
-- Run this to fix all missing tables and columns

USE farmer_market;

-- 1. Add missing columns to crops table (with error handling)
ALTER TABLE crops ADD COLUMN average_rating DECIMAL(3,2) DEFAULT 0.00;
ALTER TABLE crops ADD COLUMN review_count INT DEFAULT 0;
ALTER TABLE crops ADD COLUMN discount DECIMAL(5,2) DEFAULT 0.00;
ALTER TABLE crops ADD COLUMN mrp DECIMAL(10,2) DEFAULT 0.00;
ALTER TABLE crops ADD COLUMN delivery_days INT DEFAULT 2;
ALTER TABLE crops ADD COLUMN place_of_origin VARCHAR(255) DEFAULT NULL;
ALTER TABLE crops ADD COLUMN description TEXT DEFAULT NULL;
ALTER TABLE crops ADD COLUMN is_available TINYINT(1) DEFAULT 1;
ALTER TABLE crops ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE crops ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- 2. Add missing columns to customers table
ALTER TABLE customers ADD COLUMN alternate_phone VARCHAR(15) DEFAULT NULL;
ALTER TABLE customers ADD COLUMN profile_image VARCHAR(255) DEFAULT 'default-avatar.png';

-- 3. Create customer_addresses table
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

-- 4. Create product_offers table
CREATE TABLE IF NOT EXISTS product_offers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    crop_id INT NOT NULL,
    offer_name VARCHAR(255) NOT NULL,
    discount_percentage DECIMAL(5,2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE CASCADE,
    INDEX idx_crop (crop_id),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Create sales_analytics table
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

-- 6. Create admin_activity_log table
CREATE TABLE IF NOT EXISTS admin_activity_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    description TEXT,
    target_id INT,
    target_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admin(id) ON DELETE CASCADE,
    INDEX idx_admin (admin_id),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Update existing crops with default values
UPDATE crops 
SET mrp = CASE WHEN mrp IS NULL OR mrp = 0 THEN price_per_kg * 1.2 ELSE mrp END,
    discount = CASE WHEN discount IS NULL THEN 0 ELSE discount END,
    delivery_days = CASE WHEN delivery_days IS NULL THEN 2 ELSE delivery_days END,
    place_of_origin = CASE WHEN place_of_origin IS NULL THEN location ELSE place_of_origin END,
    description = CASE 
        WHEN description IS NULL THEN CONCAT('Fresh ', crop_name, ' directly from local farmers')
        ELSE description 
    END,
    is_available = CASE WHEN is_available IS NULL THEN IF(quantity > 0, 1, 0) ELSE is_available END
WHERE id > 0;

-- 8. Drop existing triggers if they exist
DROP TRIGGER IF EXISTS update_crop_rating_after_insert;
DROP TRIGGER IF EXISTS update_crop_rating_after_update;
DROP TRIGGER IF EXISTS update_crop_rating_after_delete;
DROP TRIGGER IF EXISTS update_crop_quantity_after_sale;

-- 9. Create triggers for automatic rating updates
DELIMITER //

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

-- 10. Add some sample addresses for existing customers
INSERT IGNORE INTO customer_addresses (customer_id, address_type, house_number, area, landmark, pincode, city, district, state, is_default) VALUES
(1, 'Home', '123', 'Main St, Koramangala', 'Near Metro Station', '560034', 'Bangalore', 'Bangalore Urban', 'Karnataka', 1),
(2, 'Home', '456', 'Oak Ave, Jayanagar', 'Opposite Park', '570001', 'Mysore', 'Mysore', 'Karnataka', 1),
(3, 'Home', '789', 'Pine Rd, Indiranagar', 'Near Mall', '560038', 'Bangalore', 'Bangalore Urban', 'Karnataka', 1);

-- 11. Add some sample orders for testing reviews
INSERT IGNORE INTO orders (customer_id, address, total_cost, status, created_at) VALUES
(1, '123 Main St, Koramangala, Bangalore', 180.00, 'Delivered', DATE_SUB(NOW(), INTERVAL 10 DAY)),
(1, '123 Main St, Koramangala, Bangalore', 250.00, 'Delivered', DATE_SUB(NOW(), INTERVAL 7 DAY)),
(2, '456 Oak Ave, Jayanagar, Mysore', 320.00, 'Delivered', DATE_SUB(NOW(), INTERVAL 5 DAY)),
(3, '789 Pine Rd, Indiranagar, Bangalore', 150.00, 'Delivered', DATE_SUB(NOW(), INTERVAL 3 DAY));

-- 12. Fix cart table to have total_cost
ALTER TABLE cart ADD COLUMN total_cost DECIMAL(10,2) DEFAULT 0;

-- Update cart total_cost for existing items
UPDATE cart c
JOIN crops cr ON c.crop_id = cr.id
SET c.total_cost = c.quantity * cr.price_per_kg
WHERE c.total_cost = 0 OR c.total_cost IS NULL;

-- 13. Update crop ratings from existing reviews
UPDATE crops c
SET c.average_rating = COALESCE((
    SELECT AVG(rating) 
    FROM crop_reviews cr 
    WHERE cr.crop_id = c.id
), 0),
c.review_count = (
    SELECT COUNT(*) 
    FROM crop_reviews cr 
    WHERE cr.crop_id = c.id
)
WHERE id > 0;

SELECT 'Database fixed successfully!' AS status;
