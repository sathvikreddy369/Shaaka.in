# 🚀 Shaaka Quick Start Guide

Get up and running with Shaaka in 5 minutes!

## Prerequisites
- Python 3.8+
- MySQL 8.0+
- 10 minutes of your time

## Option 1: Automated Setup (Recommended)

### macOS/Linux
```bash
chmod +x setup.sh
./setup.sh
```

### Windows
```bash
setup.bat
```

That's it! The script will:
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Setup database
- ✅ Import sample data
- ✅ Start the application

## Option 2: Manual Setup (5 Steps)

### Step 1: Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
mysql -u root -p
```
```sql
CREATE DATABASE farmer_market;
exit;
```

### Step 3: Import Schema
```bash
mysql -u root -p farmer_market < database_schema.sql
mysql -u root -p farmer_market < add_blog_schema.sql
mysql -u root -p farmer_market < sample_data.sql
```

### Step 4: Update Database Password
Edit `app.py` line 47:
```python
'password': 'your_mysql_password',  # Change this
```

### Step 5: Run Application
```bash
python app.py
```

Visit: http://localhost:5001

## 🔑 Login Credentials

### Admin
- Email: admin@farmermarket.com
- Password: password123
- Access: Full system control

### Customer
- Email: customer@example.com
- Password: password123
- Access: Browse and order products

### Farmer
- Phone: 9876543220
- Password: password123
- Access: Manage products and sales

### Homemaker
- Email: homemaker@example.com
- Password: password123
- Access: Upload food items

## 📱 Test the Application

### As Customer:
1. Login with customer credentials
2. Browse products
3. Add to cart
4. Checkout
5. View orders

### As Farmer:
1. Login with farmer credentials
2. Add new products
3. View dashboard
4. Check analytics

### As Admin:
1. Login with admin credentials
2. View dashboard
3. Manage products
4. Create blog posts
5. Manage FAQs

## 🐛 Common Issues

### Port 5001 already in use?
Change port in `app.py`:
```python
app.run(debug=True, port=5002)
```

### Database connection error?
Check MySQL is running:
```bash
# macOS
mysql.server status

# Windows
net start mysql

# Linux
sudo systemctl status mysql
```

### Module not found?
Activate virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

## 📚 Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [ADMIN_GUIDE.md](ADMIN_GUIDE.md) for admin features
- Review [NEW_PAGES_GUIDE.md](NEW_PAGES_GUIDE.md) for new features

## 🎯 Key Features to Try

1. **Home Page** - See trust-building content
2. **Blog** - Read organic farming tips
3. **FAQ** - Common questions answered
4. **Contact** - Send a message
5. **Admin Panel** - Manage everything
6. **Customer Dashboard** - Shop for products
7. **Farmer Dashboard** - Manage inventory
8. **Analytics** - View sales data

## 💡 Tips

- Use Chrome/Firefox for best experience
- Clear browser cache if styles don't load
- Check console for any JavaScript errors
- Enable pop-ups for some features

## 🆘 Need Help?

- Check the logs in terminal
- Review error messages
- Ensure all dependencies are installed
- Verify database is running
- Check file permissions

## 🎉 You're Ready!

Start exploring Shaaka and enjoy the farm-to-table experience!

---

**Happy Farming! 🌾**
