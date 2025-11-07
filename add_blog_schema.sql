-- Add blog functionality to Shaaka
-- Run this to add blog and FAQ tables

USE farmer_market;

-- Create blogs table
CREATE TABLE IF NOT EXISTS blogs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    featured_image VARCHAR(255),
    author_id INT NOT NULL,
    status ENUM('draft', 'published') DEFAULT 'draft',
    tags VARCHAR(500),
    meta_description VARCHAR(160),
    views INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES admin(id) ON DELETE CASCADE,
    INDEX idx_slug (slug),
    INDEX idx_status (status),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create FAQ table
CREATE TABLE IF NOT EXISTS faqs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(500) NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(100) DEFAULT 'General',
    display_order INT DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_active (is_active),
    INDEX idx_order (display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample blog posts
INSERT INTO blogs (title, slug, content, excerpt, author_id, status, tags, meta_description) VALUES
('The Benefits of Organic Farming', 'benefits-organic-farming', 
'<p>Organic farming is more than just a trend – it''s a sustainable approach to agriculture that benefits both our health and the environment.</p>
<h3>What is Organic Farming?</h3>
<p>Organic farming is a method of crop production that avoids the use of synthetic pesticides, herbicides, fertilizers, and genetically modified organisms (GMOs). Instead, it relies on natural processes and materials to maintain soil health and control pests.</p>
<h3>Health Benefits</h3>
<ul>
<li>No harmful chemical residues</li>
<li>Higher nutritional content</li>
<li>Better taste and freshness</li>
<li>Reduced risk of allergies</li>
</ul>
<h3>Environmental Benefits</h3>
<ul>
<li>Improved soil health</li>
<li>Better water quality</li>
<li>Increased biodiversity</li>
<li>Reduced carbon footprint</li>
</ul>
<p>At Shaaka, we work exclusively with certified organic farmers who follow these sustainable practices.</p>',
'Discover why organic farming is better for your health and the environment. Learn about the benefits of choosing organic produce.',
1, 'published', 'organic,farming,health,environment', 'Learn about the health and environmental benefits of organic farming and why it matters for your family.'),

('Farm to Table: The Journey of Your Food', 'farm-to-table-journey',
'<p>Ever wondered how your fresh vegetables travel from the farm to your table? Let us take you on that journey.</p>
<h3>Morning Harvest</h3>
<p>Our farmers wake up before dawn to harvest crops at their peak freshness. Vegetables are picked when they''re perfectly ripe, ensuring maximum flavor and nutrition.</p>
<h3>Quality Check</h3>
<p>Each batch undergoes rigorous quality inspection. We check for freshness, size, and ensure there are no defects.</p>
<h3>Packaging</h3>
<p>Products are carefully packaged to maintain freshness during transit. We use eco-friendly packaging materials.</p>
<h3>Delivery</h3>
<p>Within 24 hours of harvest, your order reaches your doorstep. This is what we call true farm-to-table freshness!</p>',
'Follow the journey of your fresh produce from the farm to your table. See how we ensure maximum freshness in just 24 hours.',
1, 'published', 'farm-to-table,delivery,freshness', 'Discover how Shaaka delivers farm-fresh produce to your doorstep within 24 hours of harvest.'),

('Supporting Local Farmers: Why It Matters', 'supporting-local-farmers',
'<p>When you buy from Shaaka, you''re not just getting fresh produce – you''re supporting local farming communities.</p>
<h3>Fair Prices for Farmers</h3>
<p>By eliminating middlemen, we ensure farmers get fair compensation for their hard work. This helps them invest in better farming practices and improve their livelihoods.</p>
<h3>Strengthening Local Economy</h3>
<p>Every purchase keeps money within the local community, creating jobs and economic opportunities.</p>
<h3>Preserving Traditional Farming</h3>
<p>Your support helps preserve traditional farming knowledge and sustainable agricultural practices for future generations.</p>
<h3>Building Relationships</h3>
<p>We create direct connections between farmers and consumers, fostering trust and transparency in the food system.</p>',
'Learn why supporting local farmers matters and how your purchases make a real difference in farming communities.',
1, 'published', 'local,farmers,community,support', 'Discover how buying from local farmers strengthens communities and supports sustainable agriculture.');

-- Insert sample FAQs
INSERT INTO faqs (question, answer, category, display_order, is_active) VALUES
('How do I place an order?', 'Simply browse our products, add items to your cart, and proceed to checkout. You can pay online or choose cash on delivery.', 'Orders', 1, 1),
('What are your delivery timings?', 'We deliver between 8 AM to 8 PM, 7 days a week. You can choose your preferred delivery slot during checkout.', 'Delivery', 2, 1),
('Is the produce really organic?', 'Yes! All our farmers are certified organic and follow strict organic farming practices. We regularly audit our farmers to ensure compliance.', 'Products', 3, 1),
('What is your return policy?', 'If you''re not satisfied with the quality, you can return the product within 24 hours for a full refund. Your satisfaction is our priority.', 'Returns', 4, 1),
('Do you deliver to my area?', 'We currently deliver within 50km of our partner farms. Enter your pincode during checkout to check availability.', 'Delivery', 5, 1),
('How fresh is the produce?', 'All produce is harvested within 24 hours of delivery. We guarantee maximum freshness from farm to your table.', 'Products', 6, 1),
('Can I cancel my order?', 'Yes, you can cancel your order before it''s dispatched. Once dispatched, cancellation is not possible but you can return the items.', 'Orders', 7, 1),
('What payment methods do you accept?', 'We accept credit/debit cards, UPI, net banking, and cash on delivery. All online payments are secure and encrypted.', 'Payment', 8, 1),
('How do I become a farmer partner?', 'If you''re an organic farmer, you can register on our platform. Our team will verify your credentials and help you get started.', 'Farmers', 9, 1),
('Do you have a minimum order value?', 'Yes, the minimum order value is ₹200 to ensure economical delivery. Orders above ₹500 get free delivery.', 'Orders', 10, 1);

SELECT 'Blog and FAQ tables created successfully!' as Status;
