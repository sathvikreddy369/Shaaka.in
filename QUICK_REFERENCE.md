# 🚀 Shaaka - Quick Reference Card

## ⚡ Quick Start
```bash
# Automated Setup
./setup.sh        # macOS/Linux
setup.bat         # Windows

# Manual Start
python app.py

# Access
http://localhost:5001
```

## 🔑 Login Credentials

| Role | Login | Password |
|------|-------|----------|
| **Admin** | admin@farmermarket.com | password123 |
| **Customer** | customer@example.com | password123 |
| **Farmer** | 9876543220 (phone) | password123 |
| **Homemaker** | homemaker@example.com | password123 |

## 📄 Key URLs

| Page | URL |
|------|-----|
| Home | http://localhost:5001 |
| About | http://localhost:5001/about |
| Contact | http://localhost:5001/contact |
| Blog | http://localhost:5001/blog |
| FAQ | http://localhost:5001/faq |
| Admin Login | http://localhost:5001/admin_login |
| Customer Login | http://localhost:5001/customer_login |
| Farmer Login | http://localhost:5001/login |
| Homemaker Login | http://localhost:5001/employee_login |

## 🗄️ Database Setup
```bash
# Create database
mysql -u root -p
CREATE DATABASE farmer_market;
exit;

# Import schema
mysql -u root -p farmer_market < database_schema.sql
mysql -u root -p farmer_market < add_blog_schema.sql

# Seed data
./seed_data.sh    # macOS/Linux
seed_data.bat     # Windows
```

## 📊 Sample Data Included

- **9 User Accounts** (1 admin, 3 customers, 3 farmers, 2 homemakers)
- **6 Products** (vegetables and fruits)
- **4 Food Items** (home-cooked meals)
- **6 Reviews** (4-5 star ratings)
- **3 Blog Posts** (organic farming topics)
- **10 FAQs** (categorized)

## 🎯 Quick Tests

### Test Customer Flow
1. Login: customer@example.com / password123
2. Browse products
3. Add to cart
4. Checkout
5. View orders

### Test Farmer Flow
1. Login: 9876543220 / password123
2. View dashboard
3. Add product
4. View analytics

### Test Admin Flow
1. Login: admin@farmermarket.com / password123
2. View dashboard
3. Manage products
4. Create blog post
5. Add FAQ

## 🔧 Common Commands

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Check database
mysql -u root -p farmer_market
```

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Main documentation |
| QUICKSTART.md | 5-minute setup |
| SAMPLE_DATA_INFO.md | Sample data details |
| FINAL_SUMMARY.md | Complete summary |
| ADMIN_GUIDE.md | Admin features |

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port in use | Change port in app.py |
| Database error | Check MySQL is running |
| Module not found | Activate venv, reinstall deps |
| Template not found | Check file exists in templates/ |

## 📱 Features

### For Customers
- Browse organic products
- Shopping cart
- Order tracking
- Product reviews
- Profile management

### For Farmers
- Product management
- Sales analytics
- Order management
- Earnings dashboard

### For Admins
- User management
- Product management
- Blog management
- FAQ management
- Analytics

## 🎨 Tech Stack

- **Backend:** Python Flask 3.0.0
- **Database:** MySQL 8.0+
- **Frontend:** Bootstrap 5, JavaScript
- **Icons:** Bootstrap Icons
- **Auth:** Flask-Login

## 📞 Support

- 📧 support@shaaka.com
- 📱 +91 1800-123-4567
- 🌐 https://shaaka.com

---

**Version:** 1.0.0 | **Status:** Production Ready ✅

**Happy Farming! 🌾**
