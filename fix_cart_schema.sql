-- Fix cart table to ensure total_cost column exists
ALTER TABLE `cart` ADD COLUMN IF NOT EXISTS `total_cost` DECIMAL(10,2) GENERATED ALWAYS AS (`quantity` * `price`) STORED;

-- Update existing cart items to recalculate
UPDATE cart c
JOIN crops cr ON c.crop_id = cr.id
SET c.price = cr.price_per_kg
WHERE c.price = 0 OR c.price IS NULL;
