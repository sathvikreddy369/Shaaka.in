# 🌾 Shaaka - Farm to Table Marketplace

A comprehensive web platform connecting organic farmers directly with customers, eliminating middlemen and ensuring fresh, pesticide-free produce reaches your table within 24 hours.

## 🎯 Features

### For Customers
- Browse organic produce from certified farmers
- Order fresh vegetables, fruits, and home-cooked meals
- Real-time order tracking
- Multiple payment options (Card, UPI, COD)
- Review and rate products
- View order history
- Manage delivery addresses

### For Farmers
- List and manage products
- Track sales and earnings
- View analytics and insights
- Manage inventory
- Direct customer communication
- Fair pricing without middlemen

### For Homemakers (Employees)
- Upload home-cooked food items
- Manage food listings
- Track orders and earnings
- Build customer base

### For Admins
- Comprehensive dashboard
- User management (customers, farmers, employees)
- Product management
- Order management
- Blog and FAQ management
- Analytics and reports
- Recipe management

### Additional Features
- Blog system for organic farming tips
- FAQ section
- Contact form
- About Us, Privacy Policy, Terms of Service
- Responsive design for mobile and desktop
- Secure authentication
- Email notifications

## 🛠️ Technology Stack

- **Backend:** Python Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Authentication:** Flask-Login
- **File Upload:** Werkzeug
- **Icons:** Bootstrap Icons
- **Maps:** Google Maps API (for location)

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)
- Git (optional, for cloning)

## 🚀 Quick Setup (Automated)

### For macOS/Linux:
```bash
chmod +x setup.sh
./setup.sh
```

### For Windows:
```bash
setup.bat
```

The automated setup will:
1. Create virtual environment
2. Install dependencies
3. Create database and tables
4. Add sample data
5. Start the application

## 📝 Manual Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Shaaka_web
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database

Edit `app.py` and update database credentials:
```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # Change this
    'database': 'farmer_market',
    'charset': 'utf8mb4'
}
```

### 5. Create Database
```bash
mysql -u root -p
```

```sql
CREATE DATABASE farmer_market;
USE farmer_market;
```

### 6. Import Database Schema
```bash
mysql -u root -p farmer_market < database_schema.sql
mysql -u root -p farmer_market < add_blog_schema.sql
```

### 7. Add Sample Data (Optional)

#### Option A: Using Seed Script (Recommended)
```bash
# macOS/Linux
chmod +x seed_data.sh
./seed_data.sh

# Windows
seed_data.bat
```

#### Option B: Manual Import
```bash
mysql -u root -p farmer_market < sample_data.sql
```

### 8. Create Upload Directory
```bash
mkdir -p static/uploads
```

### 9. Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5001`

## 🔑 Default Login Credentials

### Admin Account
- **Email:** admin@farmermarket.com
- **Password:** password123
- **Access:** Full system control, user management, content management

### Customer Account
- **Email:** customer@example.com
- **Password:** password123
- **Access:** Browse products, place orders, manage profile

### Farmer Account
- **Phone:** 9876543220
- **Password:** password123
- **Access:** Manage products, view sales, analytics

### Homemaker Account
- **Email:** homemaker@example.com
- **Password:** password123
- **Access:** Upload food items, manage listings

> 📋 **Note:** For complete details about all sample data including additional accounts, products, and test scenarios, see [SAMPLE_DATA_INFO.md](SAMPLE_DATA_INFO.md)

## 📁 Project Structure

```
Shaaka_web/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── database_schema.sql         # Database structure
├── add_blog_schema.sql        # Blog and FAQ tables
├── sample_data.sql            # Sample data for testing
├── setup.sh                   # Setup script (macOS/Linux)
├── setup.bat                  # Setup script (Windows)
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── static/                    # Static files
│   ├── css/                   # Custom stylesheets
│   ├── js/                    # JavaScript files
│   ├── img/                   # Images
│   ├── uploads/               # User uploaded files
│   └── vendor/                # Third-party libraries
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── index_new.html        # Home page
│   ├── about.html            # About page
│   ├── contact.html          # Contact page
│   ├── blog.html             # Blog listing
│   ├── faq.html              # FAQ page
│   ├── customer_*.html       # Customer pages
│   ├── farmer_*.html         # Farmer pages
│   ├── employee_*.html       # Employee pages
│   └── admin_*.html          # Admin pages
└── docs/                      # Documentation
    ├── ADMIN_GUIDE.md
    ├── ADMIN_FEATURES.md
    └── NEW_PAGES_GUIDE.md
```

## 🌐 Application Routes

### Public Routes
- `/` - Home page
- `/about` - About us
- `/contact` - Contact form
- `/blog` - Blog listing
- `/blog/<slug>` - Individual blog post
- `/faq` - Frequently asked questions
- `/privacy` - Privacy policy
- `/terms` - Terms of service

### Customer Routes
- `/customer_register` - Customer registration
- `/customer_login` - Customer login
- `/customer_dashboard` - Customer dashboard
- `/customer_profile` - Profile management
- `/view_cart` - Shopping cart
- `/checkout` - Checkout process
- `/my_orders` - Order history

### Farmer Routes
- `/register` - Farmer registration
- `/login` - Farmer login
- `/farmer_dashboard` - Farmer dashboard
- `/add_crop` - Add new product
- `/farmer_analytics` - Sales analytics
- `/farmer_orders` - Order management

### Employee Routes
- `/employee_register` - Employee registration
- `/employee_login` - Employee login
- `/employee_dashboard` - Employee dashboard
- `/upload_food` - Upload food items

### Admin Routes
- `/admin_login` - Admin login
- `/admin_dashboard` - Admin dashboard
- `/admin_products` - Product management
- `/admin_blogs` - Blog management
- `/admin_faqs` - FAQ management
- `/admin_users` - User management

## 🔧 Configuration

### Email Configuration (Optional)
To enable email notifications, update `app.py`:
```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

### Google Maps API (Optional)
For location features, add your API key in templates:
```javascript
const GOOGLE_MAPS_API_KEY = 'your-api-key';
```

## 📊 Database Schema

### Main Tables
- `customers` - Customer accounts
- `farmers` - Farmer accounts
- `employees` - Homemaker accounts
- `admin` - Admin accounts
- `crops` - Product listings
- `orders` - Customer orders
- `cart` - Shopping cart items
- `reviews` - Product reviews
- `blogs` - Blog posts
- `faqs` - FAQ entries

## 🧪 Testing

### Test Customer Flow
1. Register as customer
2. Browse products
3. Add items to cart
4. Proceed to checkout
5. Place order
6. View order history
7. Leave product review

### Test Farmer Flow
1. Register as farmer
2. Add products
3. View dashboard
4. Check analytics
5. Manage orders

### Test Admin Flow
1. Login as admin
2. View dashboard
3. Manage products
4. Create blog post
5. Add FAQ
6. View reports

## 🐛 Troubleshooting

### Database Connection Error
- Check MySQL is running: `mysql.server status` (macOS) or `net start mysql` (Windows)
- Verify credentials in `app.py`
- Ensure database exists: `SHOW DATABASES;`

### Port Already in Use
- Change port in `app.py`: `app.run(port=5002)`
- Or kill process using port 5001: `lsof -ti:5001 | xargs kill` (macOS/Linux)

### Module Not Found Error
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

### Upload Directory Error
- Create directory: `mkdir -p static/uploads`
- Check permissions: `chmod 755 static/uploads`

### Template Not Found
- Verify template exists in `templates/` folder
- Check template name spelling in routes

## 📱 Mobile Responsiveness

The application is fully responsive and works on:
- Desktop (1920px and above)
- Laptop (1366px - 1920px)
- Tablet (768px - 1366px)
- Mobile (320px - 768px)

## 🔒 Security Features

- Password hashing (Werkzeug)
- Session management
- CSRF protection
- SQL injection prevention (parameterized queries)
- XSS protection
- Secure file uploads
- Input validation

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False` in `app.py`
2. Use strong secret key
3. Enable HTTPS
4. Set secure session cookies
5. Configure production database
6. Set up email service
7. Configure backup system
8. Enable logging
9. Set up monitoring

### Recommended Hosting
- **Backend:** Heroku, AWS, DigitalOcean, PythonAnywhere
- **Database:** AWS RDS, Google Cloud SQL, DigitalOcean Managed Database
- **Static Files:** AWS S3, Cloudinary

## 📈 Future Enhancements

- [ ] Real-time chat between customers and farmers
- [ ] Mobile app (React Native)
- [ ] Payment gateway integration (Razorpay, Stripe)
- [ ] SMS notifications
- [ ] Advanced analytics dashboard
- [ ] Inventory management system
- [ ] Delivery tracking with GPS
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Progressive Web App (PWA)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Project Lead:** [Your Name]
- **Backend Developer:** [Name]
- **Frontend Developer:** [Name]
- **Database Administrator:** [Name]

## 📞 Support

For support and queries:
- **Email:** support@shaaka.com
- **Phone:** +91 1800-123-4567
- **Website:** https://shaaka.com

## 🙏 Acknowledgments

- Bootstrap team for the UI framework
- Flask community for the web framework
- All contributors and testers

---

**Made with ❤️ for farmers and healthy living**

## 📸 Screenshots

### Home Page
![Home Page](docs/screenshots/home.png)

### Customer Dashboard
![Customer Dashboard](docs/screenshots/customer-dashboard.png)

### Farmer Dashboard
![Farmer Dashboard](docs/screenshots/farmer-dashboard.png)

### Admin Dashboard
![Admin Dashboard](docs/screenshots/admin-dashboard.png)

---

**Version:** 1.0.0  
**Last Updated:** November 7, 2025
