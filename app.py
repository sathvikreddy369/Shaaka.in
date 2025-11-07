import csv
import datetime
import hashlib
import os
import zipfile
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import requests
from flask import session


# Initialize PayU client
MERCHANT_KEY = "5DFOHT"
MERCHANT_SALT = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDOBVSO3S7Wl31918rcnzQFjnN3n61xA4tS1ww8+7ahK6wvpJQZg0ZxeR92EaGM2RUuxzvmE6k4pwczjU3+7dlB5qCDiZLElSvpr50+P2sna1eBvkDO06hgTPx8mfYhEGrw/2uG45HoUVwSQiRCRqEihpMwqd1qcjcC1AH3SVkByepUfv7a+ysw11M5XptpXBbN2lfC3vPaveAd0/9ElSvHXT7D4tiDHEJJAEommT67A7ErvoZ49CX8i2o5is8JvB3tE593vc65nrjMgy9Z3WJbIknq8OhaNm/YN5sJU1ESYEoOUR0UBh8GgkcyyZVfjaKDfOs4Cwns8xGhFEuaMLl3AgMBAAECggEAHImUeu2cbVEyqtnXWdQbqqFe0TUnGz54cBMluNTNKWoZQcg0U4xhl5pFh19N12rCimZCn84dZKGOV8+8/BEKRRyjI1VNJTnciVQwHc0/FIjD6E7oPz4GVsCTQNc6xr21coiO5nJjZaDPdh//UcbizxuBC/6bkwEbKaMgWpaoY5zKtyaDPoa/8JqibTywHynKrPiylyEMCme5T2IZpabzih+5pJSBeb/vgrTF0dYaEk/ghcxGFYX+9RLpdlsj6+RAZMiOiV2KtIQdnA7DPl9aagLh9Mg/QsDEHTOnfj/EX0OG1P1/JpA95R1sI50CsHf5HX5w1dm3hzjxEWOzu9smoQ"
PAYMENT_URL = "https://test.payu.in/_payment"



# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'a_very_secure_and_consistent_key'
app.config['DEBUG'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'




UPLOAD_FOLDER = 'static/uploads'
CSV_ALLOWED_EXTENSIONS = {'csv'}
ZIP_ALLOWED_EXTENSIONS = {'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# MySQL Database Setup
db_config = {
    'host': 'localhost',
    'user': 'root',  
    'password': 'rootroot',  
    'database': 'farmer_market',
    'charset': 'utf8mb4'
}

# Setup Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Context processor to make cart_count available in all templates
@app.context_processor
def inject_cart_count():
    cart_count = 0
    if 'customer_id' in session:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT COUNT(*) AS count FROM cart WHERE customer_id = %s', (session['customer_id'],))
            result = cursor.fetchone()
            cart_count = result['count'] if result else 0
            conn.close()
        except:
            cart_count = 0
    return dict(cart_count=cart_count)

# MySQL connection function
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# User class for Flask-Login

class Customer(UserMixin):
    def __init__(self, id, name, phone, email, password, profile_pic=None, latitude=None, longitude=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.profile_pic = profile_pic
        self.latitude = latitude
        self.longitude = longitude

    def get_id(self):
        return str(self.id)


# User Loader for Flask-Login
from flask_login import UserMixin

# Define User class
class User(UserMixin):
    def __init__(self, id, name, phone, password, is_admin=False, profile_pic=None, latitude=None, longitude=None):
        self.id = id
        self.is_admin = is_admin
        self.name = name
        self.phone = phone
        self.password = password
        self.profile_pic = profile_pic  # Add profile_pic
        self.latitude = latitude  # Add latitude
        self.longitude = longitude  # Add longitude

    def get_id(self):
        return str(self.id)

# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM farmers WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return User(id=user['id'], name=user['name'], phone=user['phone'], password=user['password'], profile_pic=user['profile_pic'])
    return None


# Route to Home Page
@app.route('/')
def home():
    return render_template('index_new.html')

# Static Pages Routes
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Here you could save to database or send email
        flash('Thank you for contacting us! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/faq')
def faq():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM faqs WHERE is_active = 1 ORDER BY display_order, id')
    faqs = cursor.fetchall()
    conn.close()
    
    # Group FAQs by category
    faq_categories = {}
    for faq in faqs:
        category = faq['category']
        if category not in faq_categories:
            faq_categories[category] = []
        faq_categories[category].append(faq)
    
    return render_template('faq.html', faq_categories=faq_categories)

# Blog Routes
@app.route('/blog')
def blog():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT b.*, a.username as author_name 
        FROM blogs b 
        JOIN admin a ON b.author_id = a.id 
        WHERE b.status = 'published' 
        ORDER BY b.created_at DESC
    ''')
    blogs = cursor.fetchall()
    conn.close()
    return render_template('blog.html', blogs=blogs)

@app.route('/blog/<slug>')
def blog_post(slug):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get blog post
    cursor.execute('''
        SELECT b.*, a.username as author_name 
        FROM blogs b 
        JOIN admin a ON b.author_id = a.id 
        WHERE b.slug = %s AND b.status = 'published'
    ''', (slug,))
    blog = cursor.fetchone()
    
    if not blog:
        flash('Blog post not found', 'danger')
        return redirect(url_for('blog'))
    
    # Increment views
    cursor.execute('UPDATE blogs SET views = views + 1 WHERE id = %s', (blog['id'],))
    conn.commit()
    
    # Get related posts
    cursor.execute('''
        SELECT id, title, slug, excerpt, created_at 
        FROM blogs 
        WHERE status = 'published' AND id != %s 
        ORDER BY created_at DESC 
        LIMIT 3
    ''', (blog['id'],))
    related_posts = cursor.fetchall()
    
    conn.close()
    return render_template('blog_post.html', blog=blog, related_posts=related_posts)

# Admin Blog Management
@app.route('/admin/blogs')
def admin_blogs():
    if 'admin_id' not in session:
        flash('Please login as admin', 'danger')
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT b.*, a.username as author_name 
        FROM blogs b 
        JOIN admin a ON b.author_id = a.id 
        ORDER BY b.created_at DESC
    ''')
    blogs = cursor.fetchall()
    conn.close()
    return render_template('admin_blogs.html', blogs=blogs)

@app.route('/admin/blog/create', methods=['GET', 'POST'])
def admin_blog_create():
    if 'admin_id' not in session:
        flash('Please login as admin', 'danger')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        tags = request.form.get('tags')
        status = request.form.get('status', 'draft')
        meta_description = request.form.get('meta_description')
        
        # Generate slug from title
        slug = title.lower().replace(' ', '-').replace('/', '-')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO blogs (title, slug, content, excerpt, author_id, status, tags, meta_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (title, slug, content, excerpt, session['admin_id'], status, tags, meta_description))
            conn.commit()
            flash('Blog post created successfully!', 'success')
            return redirect(url_for('admin_blogs'))
        except Exception as e:
            conn.rollback()
            flash(f'Error creating blog post: {str(e)}', 'danger')
        finally:
            conn.close()
    
    return render_template('admin_blog_form.html', blog=None)

@app.route('/admin/blog/edit/<int:blog_id>', methods=['GET', 'POST'])
def admin_blog_edit(blog_id):
    if 'admin_id' not in session:
        flash('Please login as admin', 'danger')
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        tags = request.form.get('tags')
        status = request.form.get('status', 'draft')
        meta_description = request.form.get('meta_description')
        
        # Generate slug from title
        slug = title.lower().replace(' ', '-').replace('/', '-')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        try:
            cursor.execute('''
                UPDATE blogs 
                SET title = %s, slug = %s, content = %s, excerpt = %s, 
                    status = %s, tags = %s, meta_description = %s
                WHERE id = %s
            ''', (title, slug, content, excerpt, status, tags, meta_description, blog_id))
            conn.commit()
            flash('Blog post updated successfully!', 'success')
            return redirect(url_for('admin_blogs'))
        except Exception as e:
            conn.rollback()
            flash(f'Error updating blog post: {str(e)}', 'danger')
        finally:
            conn.close()
    
    cursor.execute('SELECT * FROM blogs WHERE id = %s', (blog_id,))
    blog = cursor.fetchone()
    conn.close()
    
    if not blog:
        flash('Blog post not found', 'danger')
        return redirect(url_for('admin_blogs'))
    
    return render_template('admin_blog_form.html', blog=blog)

@app.route('/admin/blog/delete/<int:blog_id>', methods=['POST'])
def admin_blog_delete(blog_id):
    if 'admin_id' not in session:
        flash('Please login as admin', 'danger')
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM blogs WHERE id = %s', (blog_id,))
    conn.commit()
    conn.close()
    
    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('admin_blogs'))

# Admin FAQ Management
@app.route('/admin/faqs')
def admin_faqs():
    if 'admin_id' not in session:
        flash('Please login as admin', 'danger')
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM faqs ORDER BY category, display_order')
    faqs = cursor.fetchall()
    conn.close()
    return render_template('admin_faqs.html', faqs=faqs)

@app.route('/admin/faq/create', methods=['GET', 'POST'])
def admin_faq_create():
    if 'admin_id' not in session:
        flash('Please login as admin', 'danger')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        category = request.form.get('category', 'General')
        display_order = request.form.get('display_order', 0)
        is_active = 1 if request.form.get('is_active') else 0
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO faqs (question, answer, category, display_order, is_active)
            VALUES (%s, %s, %s, %s, %s)
        ''', (question, answer, category, display_order, is_active))
        conn.commit()
        conn.close()
        
        flash('FAQ created successfully!', 'success')
        return redirect(url_for('admin_faqs'))
    
    return render_template('admin_faq_form.html', faq=None)

@app.route('/admin/faq/edit/<int:faq_id>', methods=['GET', 'POST'])
def admin_faq_edit(faq_id):
    if 'admin_id' not in session:
        flash('Please login as admin', 'danger')
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        category = request.form.get('category', 'General')
        display_order = request.form.get('display_order', 0)
        is_active = 1 if request.form.get('is_active') else 0
        
        cursor.execute('''
            UPDATE faqs 
            SET question = %s, answer = %s, category = %s, display_order = %s, is_active = %s
            WHERE id = %s
        ''', (question, answer, category, display_order, is_active, faq_id))
        conn.commit()
        conn.close()
        
        flash('FAQ updated successfully!', 'success')
        return redirect(url_for('admin_faqs'))
    
    cursor.execute('SELECT * FROM faqs WHERE id = %s', (faq_id,))
    faq = cursor.fetchone()
    conn.close()
    
    if not faq:
        flash('FAQ not found', 'danger')
        return redirect(url_for('admin_faqs'))
    
    return render_template('admin_faq_form.html', faq=faq)

@app.route('/admin/faq/delete/<int:faq_id>', methods=['POST'])
def admin_faq_delete(faq_id):
    if 'admin_id' not in session:
        flash('Please login as admin', 'danger')
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM faqs WHERE id = %s', (faq_id,))
    conn.commit()
    conn.close()
    
    flash('FAQ deleted successfully!', 'success')
    return redirect(url_for('admin_faqs'))

@app.route('/farmer')
def farmer():
    return render_template('farmer.html')

@app.route('/hunger')
def hunger():
    return render_template('hunger.html')

@app.route('/admin')
def admin_home():
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))

# Admin Register Route
@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if 'admin_id' in session:  # Prevent logged-in admin from registering again
        flash('You are already logged in as an admin.', 'info')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO admin (username, email, password) VALUES (%s, %s, %s)',
                (username, email, hashed_password)
            )
            conn.commit()
            flash('Admin registered successfully!', 'success')
            return redirect(url_for('admin_login'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            conn.close()

    return render_template('admin_register.html')

# Admin Login Route
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM admin WHERE email = %s', (email,))
            admin = cursor.fetchone()
            conn.close()
            
            if admin and check_password_hash(admin['password'], password):
                session['admin_id'] = admin['id']
                session['admin_username'] = admin['username']
                session['admin_email'] = admin['email']
                session.permanent = True
                
                flash(f'Welcome back, {admin["username"]}!', 'success')
                
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid email or password!', 'danger')
                
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')

    return render_template('admin_login.html')

# Admin Dashboard Route
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash('Please log in as an admin to access this page.', 'danger')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch counts
    cursor.execute('SELECT COUNT(*) AS recipe_count FROM recipes')
    recipe_count = cursor.fetchone()['recipe_count']

    cursor.execute('SELECT COUNT(*) AS customer_count FROM customers')
    customer_count = cursor.fetchone()['customer_count']

    cursor.execute('SELECT COUNT(*) AS farmer_count FROM farmers')
    farmer_count = cursor.fetchone()['farmer_count']
    
    cursor.execute('SELECT COUNT(*) AS crop_count FROM crops')
    crop_count = cursor.fetchone()['crop_count']

    # Fetch all farmers with product count
    cursor.execute('''
        SELECT f.*, COUNT(c.id) as product_count
        FROM farmers f
        LEFT JOIN crops c ON f.id = c.farmer_id
        GROUP BY f.id
        ORDER BY f.name
    ''')
    farmers = cursor.fetchall()

    # Fetch all products with farmer info
    cursor.execute('''
        SELECT c.*, f.name as farmer_name, f.location as farmer_location
        FROM crops c
        JOIN farmers f ON c.farmer_id = f.id
        ORDER BY c.created_at DESC
    ''')
    products = cursor.fetchall()

    # Fetch all customers
    cursor.execute('SELECT * FROM customers ORDER BY created_at DESC')
    customers = cursor.fetchall()

    # Fetch all recipes
    cursor.execute('SELECT * FROM recipes ORDER BY created_at DESC')
    recipes = cursor.fetchall()

    conn.close()

    return render_template(
        'admin_dashboard_enhanced.html',
        recipe_count=recipe_count,
        customer_count=customer_count,
        farmer_count=farmer_count,
        crop_count=crop_count,
        farmers=farmers,
        products=products,
        customers=customers,
        recipes=recipes
    )

# Admin Logout Route
@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin_login'))


# Route to Farmer Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('farmer_dashboard'))
    
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM farmers WHERE phone = %s", (phone,))
        user = cursor.fetchone()
        conn.close()

        if user:
            stored_password = user['password']
            if check_password_hash(stored_password, password):
                user_obj = User(id=user['id'], name=user['name'], phone=user['phone'], password=user['password'])
                login_user(user_obj, remember=True)
                flash(f'Welcome back, {user["name"]}!', 'success')
                
                # Redirect to next page or dashboard
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('farmer_dashboard'))
            else:
                flash('Invalid password. Please try again.', 'danger')
        else:
            flash('No account found with that phone number.', 'danger')

    return render_template('login.html')


# Route to Farmer Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        aadhar = request.form['aadhar']
        phone = request.form['phone']
        location = request.form['location']
        password = request.form['password']
        profile_pic = request.files.get('profile_pic')  # Use .get() to avoid KeyError

        # Hash the password before saving
        hashed_password = generate_password_hash(password)

        # Handle profile picture
        if profile_pic and profile_pic.filename:
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join('static/uploads', filename))
        else:
            filename = 'default.jpg'

        # Save data to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO farmers (name, age, aadhar, phone, location, password, profile_pic) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                       (name, age, aadhar, phone, location, hashed_password, filename))
        conn.commit()
        conn.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/customer_register', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        location = request.form.get('location', '').strip()
        address = request.form.get('address', '').strip()
        password = request.form.get('password', '')

        # Validation
        if not all([name, email, phone, location, address, password]):
            flash('All fields are required.', 'danger')
            return render_template('customer_register.html')

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''INSERT INTO customers (name, email, phone, location, address, password) 
                              VALUES (%s, %s, %s, %s, %s, %s)''', 
                           (name, email, phone, location, address, hashed_password))
            conn.commit()
            cursor.close()
            conn.close()

            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('customer_login'))
            
        except mysql.connector.IntegrityError as e:
            if 'Duplicate entry' in str(e):
                if 'email' in str(e):
                    flash('Email already registered. Please login or use a different email.', 'danger')
                elif 'phone' in str(e):
                    flash('Phone number already registered. Please use a different number.', 'danger')
                else:
                    flash('Account already exists. Please login.', 'danger')
            else:
                flash('Registration error. Please try again.', 'danger')
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            flash('Database error. Please try again later.', 'danger')
        except Exception as e:
            print(f"Unexpected error: {e}")
            flash('Registration failed. Please try again.', 'danger')

    return render_template('customer_register.html')


# Customer Login Route
@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    # If already logged in, redirect to dashboard
    if 'customer_id' in session:
        return redirect(url_for('customer_dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return render_template('customer_login.html')

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM customers WHERE email = %s', (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                try:
                    if check_password_hash(user['password'], password):
                        session['customer_id'] = user['id']
                        session['customer_name'] = user['name']
                        session['customer_email'] = user['email']
                        session.permanent = True
                        
                        flash(f'Welcome back, {user["name"]}!', 'success')
                        
                        next_page = request.args.get('next')
                        return redirect(next_page) if next_page else redirect(url_for('customer_dashboard'))
                    else:
                        flash('Invalid password. Please try again.', 'danger')
                except Exception as e:
                    print(f"Password verification error: {e}")
                    flash('Login error. Please contact support.', 'danger')
            else:
                flash('No account found with that email address.', 'danger')
                
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            flash('Database connection error. Please try again later.', 'danger')
        except Exception as e:
            print(f"Unexpected error: {e}")
            flash('An error occurred. Please try again.', 'danger')

    return render_template('customer_login.html')

# API endpoint for user's reviews
@app.route('/api/my_reviews')
def api_my_reviews():
    if 'customer_id' not in session:
        return jsonify({'success': False, 'message': 'Please login'}), 401
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT cr.*, c.crop_name, c.image as crop_image, c.id as crop_id
            FROM crop_reviews cr
            JOIN crops c ON cr.crop_id = c.id
            WHERE cr.customer_id = %s
            ORDER BY cr.created_at DESC
        ''', (session['customer_id'],))
        reviews = cursor.fetchall()
        conn.close()
        return jsonify({'success': True, 'reviews': reviews})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API endpoint for featured products
@app.route('/api/featured_products')
def api_featured_products():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT crops.*, farmers.name as farmer_name, farmers.location as farmer_location,
                   COALESCE(AVG(reviews.rating), 5.0) as average_rating
            FROM crops 
            JOIN farmers ON crops.farmer_id = farmers.id 
            LEFT JOIN reviews ON crops.id = reviews.crop_id
            WHERE crops.quantity > 0
            GROUP BY crops.id
            ORDER BY crops.created_at DESC
            LIMIT 6
        ''')
        products = cursor.fetchall()
        conn.close()
        return jsonify({'success': True, 'products': products})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/customer_dashboard', methods=['GET'])
def customer_dashboard():
    if 'customer_id' not in session:
        return redirect(url_for('login'))

    # Get crop type and search query from request arguments
    crop_type = request.args.get('type', 'All')
    search_query = request.args.get('search', '').lower()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch recipes (unchanged logic)
    cursor.execute("SELECT * FROM recipes")
    recipes = cursor.fetchall()

    # Fetch crops based on crop_type with search - including farmer name
    if crop_type == 'All':
        if search_query:
            cursor.execute('''SELECT crops.*, farmers.name as farmer_name, farmers.location as farmer_location 
                              FROM crops 
                              JOIN farmers ON crops.farmer_id = farmers.id 
                              WHERE crops.quantity > 0 
                              AND LOWER(crops.crop_name) LIKE %s''', 
                           (f'%{search_query}%',))
        else:
            cursor.execute('''SELECT crops.*, farmers.name as farmer_name, farmers.location as farmer_location 
                              FROM crops 
                              JOIN farmers ON crops.farmer_id = farmers.id 
                              WHERE crops.quantity > 0''')
    else:
        if search_query:
            cursor.execute('''SELECT crops.*, farmers.name as farmer_name, farmers.location as farmer_location 
                              FROM crops 
                              JOIN farmers ON crops.farmer_id = farmers.id 
                              WHERE crops.quantity > 0 AND crops.crop_type = %s
                              AND LOWER(crops.crop_name) LIKE %s''', 
                           (crop_type, f'%{search_query}%'))
        else:
            cursor.execute('''SELECT crops.*, farmers.name as farmer_name, farmers.location as farmer_location 
                              FROM crops 
                              JOIN farmers ON crops.farmer_id = farmers.id 
                              WHERE crops.quantity > 0 AND crops.crop_type = %s''', 
                           (crop_type,))
    crops = cursor.fetchall()

    # Fetch cooked food available within 12 hours of the cooked time
    cursor.execute('''
        SELECT cooked_foods.*, employees.location AS homemaker_location 
        FROM cooked_foods 
        JOIN employees ON cooked_foods.employee_id = employees.id 
        WHERE cooked_foods.cooked_time >= NOW() - INTERVAL 12 HOUR
        AND (LOWER(cooked_foods.food_name) LIKE %s OR %s = '')
    ''', (f'%{search_query}%', search_query))
    cooked_foods = cursor.fetchall()

    # Count items in the cart
    cursor.execute('SELECT COUNT(*) AS count FROM cart WHERE customer_id = %s', (session['customer_id'],))
    cart_count = cursor.fetchone()['count']

    conn.close()

    return render_template(
        'customer_dashboard_enhanced.html',
        crops=crops,
        crop_type=crop_type,
        cart_count=cart_count,
        recipes=recipes,
        cooked_foods=cooked_foods,
        search_query=search_query
    )

# Route to Farmer Dashboard (only for logged-in farmers)
@app.route('/farmer_dashboard')
@login_required
def farmer_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT crops.*, 
               COUNT(DISTINCT orders.customer_id) AS customer_count
        FROM crops 
        LEFT JOIN orders ON crops.id = orders.id
        WHERE crops.farmer_id = %s
        GROUP BY crops.id
    ''', (current_user.id,))
    crops = cursor.fetchall()
    conn.close()

    return render_template('farmer_dashboard_enhanced.html', farmer=current_user, crops=crops)


# Route to Add Crop (via Upload Form)
@app.route('/add_crop', methods=['GET', 'POST'])
@login_required
def add_crop():
    if request.method == 'POST':
        crop_name = request.form['crop_name']
        crop_type = request.form['crop_type']  # Fetch crop type from the form
        quantity = request.form['quantity']
        price_per_kg = request.form['price_per_kg']
        offer = request.form['offer']
        offer_details = request.form['offer_details']
        image = request.files['image']
        
        # Save the uploaded image
        filename = secure_filename(image.filename)
        image.save(os.path.join('static/uploads', filename))

        # Insert crop details into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO crops (farmer_id, crop_name, crop_type, quantity, price_per_kg, offer, offer_details, image)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', 
                       (current_user.id, crop_name, crop_type, quantity, price_per_kg, offer, offer_details, filename))
        conn.commit()
        conn.close()

        flash('Crop added successfully!', 'success')
        return redirect(url_for('farmer_dashboard'))

    return render_template('add_crop.html')


# Route to Edit/Delete Crop
@app.route('/edit_crop/<int:crop_id>', methods=['GET', 'POST'])
@login_required
def edit_crop(crop_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM crops WHERE id = %s', (crop_id,))
    crop = cursor.fetchone()

    if request.method == 'POST':
        crop_name = request.form['crop_name']
        quantity = request.form['quantity']
        price_per_kg = request.form['price_per_kg']
        offer = request.form['offer']
        offer_details = request.form['offer_details']

        cursor.execute('''UPDATE crops SET crop_name = %s, quantity = %s, price_per_kg = %s, 
                          offer = %s, offer_details = %s WHERE id = %s''', 
                       (crop_name, quantity, price_per_kg, offer, offer_details, crop_id))
        conn.commit()
        conn.close()

        flash('Crop updated successfully!', 'success')
        return redirect(url_for('farmer_dashboard'))

    conn.close()
    return render_template('edit_crop.html', crop=crop)

# Route to Delete Crop


@app.route('/delete_crop/<int:crop_id>', methods=['POST'])
@login_required
def delete_crop(crop_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verify the crop belongs to the logged-in farmer (using current_user.id)
    cursor.execute('SELECT id FROM crops WHERE id = %s AND farmer_id = %s', (crop_id, current_user.id))
    crop = cursor.fetchone()
    if not crop:
        conn.close()
        flash('Crop not found or does not belong to you.', 'danger')
        return redirect(url_for('farmer_dashboard'))

    # First, delete the crop from the cart
    cursor.execute('DELETE FROM cart WHERE crop_id = %s', (crop_id,))

    # Then, delete the crop from the crops table
    cursor.execute('DELETE FROM crops WHERE id = %s', (crop_id,))
    conn.commit()
    conn.close()

    flash('Crop and associated cart items deleted successfully!', 'success')
    return redirect(url_for('farmer_dashboard'))




@app.route('/customer_orders')
def customer_orders():
    if 'customer_id' not in session:
        flash('Please login to view your orders.', 'warning')
        return redirect(url_for('customer_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT orders.id AS order_id, crops.crop_name, orders.quantity, orders.total_price, orders.order_status, orders.order_date
        FROM orders 
        JOIN crops ON orders.crop_id = crops.id 
        WHERE orders.customer_id = %s
        ORDER BY orders.order_date DESC
    ''', (session['customer_id'],))
    orders = cursor.fetchall()
    conn.close()

    return render_template('customer_orders.html', orders=orders)

# Proceed to Pay (GET)
@app.route('/proceed_to_pay', methods=['GET'])
def proceed_to_pay():
    if 'customer_id' not in session:
        flash('Please log in to proceed to payment.', 'danger')
        return redirect(url_for('customer_login'))

    # Fetch the customer's cart total
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT SUM(cart.quantity * cart.price) AS grand_total
        FROM cart
        WHERE customer_id = %s
    ''', (session['customer_id'],))
    total = cursor.fetchone()
    conn.close()

    grand_total = total['grand_total'] if total['grand_total'] else 0

    if grand_total <= 0:
        flash('Your cart is empty. Add items to proceed.', 'warning')
        return redirect(url_for('view_cart'))

    # Redirect to payment page with grand total
    return render_template('payment_page.html', grand_total=grand_total)

# Proceed to Pay (POST)
@app.route('/proceed_to_pay', methods=['POST'])
def proceed_to_pay_post():
    if 'customer_id' not in session:
        flash('Please log in to complete your order.', 'danger')
        return redirect(url_for('customer_login'))

    # Calculate the total amount from the cart
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT SUM(cart.quantity * crops.price_per_kg) AS total_amount 
        FROM cart 
        JOIN crops ON cart.crop_id = crops.id
        WHERE cart.customer_id = %s
    ''', (session['customer_id'],))
    total_amount = cursor.fetchone()['total_amount']
    conn.close()

    if not total_amount:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('view_cart'))

    # Prepare the payment data
    customer_id = session['customer_id']
    txnid = f"TXN{customer_id}{int(total_amount * 100)}"  # Unique transaction ID
    email = "customer@example.com"  # Replace with customer email
    phone = "9876543210"  # Replace with customer phone number

    # Merchant details
    key = "5DFOHT"  # Merchant Key
    amount = f"{total_amount:.2f}"  # Amount to be paid
    productinfo = "Cart Purchase"  # Product description
    firstname = "Customer"  # Use actual customer first name
    salt = "PBrGrGOZrwMEPbpiQ2EKneFWw4269eLM"  # Merchant Salt

    # Construct the data dictionary
   
    data = {
        "key": key,
        "txnid": txnid,
        "amount": amount,
        "productinfo": productinfo,
        "firstname": firstname,
        "email": email,
        "surl": url_for('payment_success', _external=True),  # Success URL
        "furl": url_for('payment_failure', _external=True),  # Failure URL
        "service_provider": "payu_paisa"  # Service provider
    }

    # Construct the hash string according to PayU's formula
    hash_string = f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|||||||||||{salt}"

    # Generate the SHA-512 hash
    generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()

    # Add the hash to the data dictionary
    data["hash"] = generated_hash

    return render_template('payu_checkout.html', data=data, payment_url=PAYMENT_URL)



# Payment Success
@app.route('/payment_success', methods=['POST'])
def payment_success():
    payment_id = request.form.get('payment_id')
    txnid = request.form.get('txnid')
    status = request.form.get('status')

    # Verify payment status
    if status == 'success':
        # Update order status in the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            UPDATE payment_transactions 
            SET payment_status = 'Success' 
            WHERE txnid = %s
        ''', (txnid,))
        conn.commit()

        flash('Payment successful! Your order has been placed.', 'success')
    else:
        flash('Payment failed. Please try again.', 'danger')
    return redirect(url_for('customer_dashboard'))

# Payment Failure
@app.route('/payment_failure', methods=['POST'])
def payment_failure():
    flash('Payment failed. Please try again.', 'danger')
    return redirect(url_for('view_cart'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    if 'customer_id' not in session:
        flash('Please log in to manage your cart.', 'danger')
        return redirect(url_for('customer_login'))

    action = request.form['action']
    customer_id = session['customer_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    if action.startswith('increase-'):
        crop_id = action.split('-')[1]
        cursor.execute('UPDATE cart SET quantity = quantity + 1 WHERE customer_id = %s AND crop_id = %s', (customer_id, crop_id))
    elif action.startswith('decrease-'):
        crop_id = action.split('-')[1]
        cursor.execute('UPDATE cart SET quantity = quantity - 1 WHERE customer_id = %s AND crop_id = %s AND quantity > 1', (customer_id, crop_id))
    elif action.startswith('remove-'):
        crop_id = action.split('-')[1]
        cursor.execute('DELETE FROM cart WHERE customer_id = %s AND crop_id = %s', (customer_id, crop_id))

    conn.commit()
    conn.close()

    flash('Cart updated successfully.', 'success')
    return redirect(url_for('view_cart'))


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'customer_id' not in session:
        flash('You must log in to add items to your cart.', 'danger')
        return redirect(url_for('customer_login'))

    customer_id = session['customer_id']
    crop_id = request.form.get('crop_id')  # For crops
    recipe_id = request.form.get('recipe_id')  # For recipes
    quantity = int(request.form.get('quantity', 1))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if item already exists in the cart
    cursor.execute('''
        SELECT id, quantity FROM cart
        WHERE customer_id = %s AND (
            (crop_id = %s AND %s IS NOT NULL) OR 
            (recipe_id = %s AND %s IS NOT NULL)
        )
    ''', (customer_id, crop_id, crop_id, recipe_id, recipe_id))
    existing_item = cursor.fetchone()

    if existing_item:
        # Update quantity for existing item
        new_quantity = existing_item['quantity'] + quantity
        cursor.execute('UPDATE cart SET quantity = %s WHERE id = %s',
                       (new_quantity, existing_item['id']))
    else:
        # Determine price based on crop or recipe
        if crop_id:
            cursor.execute('SELECT price_per_kg FROM crops WHERE id = %s', (crop_id,))
            result = cursor.fetchone()
            if not result:
                flash('Crop not found.', 'danger')
                conn.close()
                return redirect(url_for('customer_dashboard'))
            price_per_unit = result['price_per_kg']
        elif recipe_id:
            cursor.execute('SELECT masala_cost FROM recipes WHERE recipe_id = %s', (recipe_id,))
            result = cursor.fetchone()
            if not result:
                flash('Recipe not found.', 'danger')
                conn.close()
                return redirect(url_for('customer_dashboard'))
            price_per_unit = result['masala_cost']
        else:
            flash('Invalid item.', 'danger')
            conn.close()
            return redirect(url_for('customer_dashboard'))

        # Insert the item into the cart
        cursor.execute('''
            INSERT INTO cart (customer_id, crop_id, recipe_id, quantity, price)
            VALUES (%s, %s, %s, %s, %s)
        ''', (customer_id, crop_id, recipe_id, quantity, quantity * price_per_unit))

    conn.commit()
    conn.close()

    flash('Item added to your cart!', 'success')
    return redirect(url_for('customer_dashboard'))



@app.route('/view_cart')
def view_cart():
    if 'customer_id' not in session:
        flash('Please log in to view your cart.', 'danger')
        return redirect(url_for('customer_login'))

    customer_id = session['customer_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch crops cart items
    cursor.execute('''
        SELECT c.id, cr.crop_name, cr.image, c.quantity, c.price, cr.price_per_kg, 
               (c.quantity * cr.price_per_kg) as total_cost
        FROM cart c
        JOIN crops cr ON c.crop_id = cr.id
        WHERE c.customer_id = %s
    ''', (customer_id,))
    crops_cart = cursor.fetchall()

    # Fetch recipes cart items
    cursor.execute('''
        SELECT id, recipe_name, image, masala_cost, quantity, total_cost
        FROM recipe_cart
        WHERE customer_id = %s
    ''', (customer_id,))
    recipes_cart = cursor.fetchall()

    # Calculate grand total
    crops_total = sum(item['total_cost'] for item in crops_cart)
    recipes_total = sum(item['total_cost'] for item in recipes_cart)
    grand_total = crops_total + recipes_total
    
    # Count items in the cart
    cart_count = len(crops_cart) + len(recipes_cart)

    conn.close()

    return render_template('view_cart_enhanced.html', crops_cart=crops_cart, recipes_cart=recipes_cart, 
                         grand_total=grand_total, cart_count=cart_count)

    #add recipes
@app.route('/upload_recipes', methods=['GET', 'POST'])
def upload_recipes():
    if request.method == 'POST':
        # Check if a file is selected
        if 'csv_file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        csv_file = request.files['csv_file']
        
        if csv_file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        # Ensure the file is a CSV
        if csv_file and csv_file.filename.endswith('.csv'):
            filename = secure_filename(csv_file.filename)
            # Save the file to the 'uploads' folder (inside the 'static' folder if applicable)
            file_path = os.path.join('static', 'uploads', filename)  # Ensure you save it to the correct path
            csv_file.save(file_path)

            # Open and read the CSV file
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                conn = get_db_connection()
                cursor = conn.cursor()

                # Loop through each row in the CSV and insert into MySQL
                for row in reader:
                    recipe_name = row['recipe_name']
                    image = row['image']  # Image filename, it should match the image in 'uploads'
                    ingredients = row['ingredients']
                    masala_cost = float(row['masala_cost'])
                    cooking_instructions = row['cooking_instructions']
                    main_items = row.get('main_items', '')  # Optional field, default to empty if not present

                    # Prepare the SQL insert query
                    cursor.execute('''
                        INSERT INTO recipes (recipe_name, image, ingredients, masala_cost, cooking_instructions, main_items)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (recipe_name, image, ingredients, masala_cost, cooking_instructions, main_items))

                conn.commit()  # Commit the transaction
                conn.close()

            flash('Recipes uploaded successfully!', 'success')
            return redirect(url_for('admin_dashboard'))  # Redirect to the admin dashboard

    # Render the upload form for CSV
    return render_template('upload_recipes.html')  # Ensure you have a proper template for this page

@app.route('/add_recipe_to_cart', methods=['POST'])
def add_recipe_to_cart():
    if 'customer_id' not in session:
        flash('Please log in to add recipes to the cart.', 'danger')
        return redirect(url_for('customer_login'))

    customer_id = session['customer_id']
    recipe_id = request.form.get('recipe_id')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if the recipe exists
    cursor.execute('SELECT * FROM recipes WHERE id = %s', (recipe_id,))
    recipe = cursor.fetchone()
    if not recipe:
        flash('Recipe not found.', 'danger')
        return redirect(url_for('customer_dashboard'))

    # Check if the recipe is already in the cart
    cursor.execute('SELECT * FROM recipe_cart WHERE customer_id = %s AND recipe_id = %s', (customer_id, recipe_id))
    cart_item = cursor.fetchone()

    if cart_item:
        # Increase quantity if already in the cart
        new_quantity = cart_item['quantity'] + 1
        cursor.execute('UPDATE recipe_cart SET quantity = %s WHERE id = %s', (new_quantity, cart_item['id']))
    else:
        # Add new recipe to the cart
        cursor.execute('''
            INSERT INTO recipe_cart (customer_id, recipe_id, recipe_name, image, masala_cost, quantity)
            VALUES (%s, %s, %s, %s, %s, 1)
        ''', (customer_id, recipe_id, recipe['recipe_name'], recipe['image'], recipe['masala_cost']))

    conn.commit()
    conn.close()

    flash('Recipe added to the cart.', 'success')
    return redirect(url_for('customer_dashboard'))


@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    if 'customer_id' not in session:
        return jsonify({'error': 'You must log in to get recipes.'}), 403

    customer_id = session['customer_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch crop names in the cart
    cursor.execute('''
        SELECT cr.crop_name 
        FROM cart c
        JOIN crops cr ON c.crop_id = cr.id
        WHERE c.customer_id = %s
    ''', (customer_id,))
    cart_crops = [item['crop_name'].lower() for item in cursor.fetchall()]

    if not cart_crops:
        return jsonify({'recipes': []})

    # Fetch recipes
    cursor.execute('SELECT id, recipe_name, main_items, image FROM recipes')
    recipes = cursor.fetchall()

    # Filter recipes based on partial matches with cart crops
    matching_recipes = []
    for recipe in recipes:
        main_items = [item.strip().lower() for item in recipe['main_items'].split(',')]
        if any(crop in main_items for crop in cart_crops):
            matching_recipes.append(recipe)

    conn.close()
    return jsonify({'recipes': matching_recipes})



@app.route('/buy_combo/<int:recipe_id>', methods=['POST'])
def buy_combo(recipe_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM recipes WHERE id = %s', (recipe_id,))
    recipe = cursor.fetchone()
    conn.close()

    if not recipe:
        flash('Recipe not found!', 'danger')
        return redirect(url_for('customer_dashboard'))

    # Email the recipe to the customer
    customer_email = session.get('email')
    send_email(customer_email, f"Recipe for {recipe['recipe_name']}", f"""
        <h3>{recipe['recipe_name']}</h3>
        <p><strong>Ingredients:</strong></p>
        <ul>
            {"".join([f"<li>{ing}</li>" for ing in recipe['ingredients'].split(',')])}
        </ul>
        <p><strong>Cooking Instructions:</strong></p>
        <p>{recipe['cooking_instructions']}</p>
    """)
    flash('Recipe sent to your email!', 'success')
    return redirect(url_for('customer_dashboard'))

@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe_details(recipe_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch recipe details
    cursor.execute('''
        SELECT id, recipe_name, main_items, cooking_instructions, image 
        FROM recipes 
        WHERE id = %s
    ''', (recipe_id,))
    recipe = cursor.fetchone()
    conn.close()

    if not recipe:
        flash('Recipe not found.', 'danger')
        return redirect(url_for('customer_dashboard'))

    return render_template('recipe_details.html', recipe=recipe)

@app.route('/update_crop_quantity', methods=['POST'])
def update_crop_quantity():
    if 'customer_id' not in session:
        flash('Please log in to update the cart.', 'danger')
        return redirect(url_for('customer_login'))

    customer_id = session['customer_id']
    cart_id = request.form.get('cart_id')
    action = request.form.get('action')  # 'increase' or 'decrease'

    conn = get_db_connection()
    cursor = conn.cursor()

    if action == 'increase':
        cursor.execute('UPDATE cart SET quantity = quantity + 1, total_cost = quantity * price WHERE id = %s AND customer_id = %s', (cart_id, customer_id))
    elif action == 'decrease':
        cursor.execute('UPDATE cart SET quantity = GREATEST(quantity - 1, 1), total_cost = quantity * price WHERE id = %s AND customer_id = %s', (cart_id, customer_id))

    conn.commit()
    conn.close()
    return redirect(url_for('view_cart'))


@app.route('/update_recipe_quantity', methods=['POST'])
def update_recipe_quantity():
    if 'customer_id' not in session:
        flash('Please log in to update the cart.', 'danger')
        return redirect(url_for('customer_login'))

    customer_id = session['customer_id']
    cart_id = request.form.get('cart_id')
    action = request.form.get('action')  # 'increase' or 'decrease'

    conn = get_db_connection()
    cursor = conn.cursor()

    if action == 'increase':
        cursor.execute('UPDATE recipe_cart SET quantity = quantity + 1 WHERE id = %s AND customer_id = %s', (cart_id, customer_id))
    elif action == 'decrease':
        cursor.execute('UPDATE recipe_cart SET quantity = GREATEST(quantity - 1, 1) WHERE id = %s AND customer_id = %s', (cart_id, customer_id))

    conn.commit()
    conn.close()
    return redirect(url_for('view_cart'))

@app.route('/delete_crop_cart', methods=['POST'])
def delete_crop_cart():
    if 'customer_id' not in session:
        flash('Please log in to update the cart.', 'danger')
        return redirect(url_for('customer_login'))

    customer_id = session['customer_id']
    cart_id = request.form.get('cart_id')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart WHERE id = %s AND customer_id = %s', (cart_id, customer_id))

    conn.commit()
    conn.close()
    return redirect(url_for('view_cart'))


@app.route('/delete_recipe', methods=['POST'])
def delete_recipe():
    if 'customer_id' not in session:
        flash('Please log in to update the cart.', 'danger')
        return redirect(url_for('customer_login'))

    customer_id = session['customer_id']
    cart_id = request.form.get('cart_id')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM recipe_cart WHERE id = %s AND customer_id = %s', (cart_id, customer_id))

    conn.commit()
    conn.close()
    return redirect(url_for('view_cart'))


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    # Ensure admin is logged in
    if 'admin_id' not in session:
        flash('Please log in as an admin to access this page.', 'danger')
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join('static/uploads', filename))

        main_items = request.form['main_items']  # Comma-separated list
        ingredients = request.form['ingredients']  # Comma-separated list
        masala_cost = request.form['masala_cost']
        cooking_instructions = request.form['cooking_instructions']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recipes (recipe_name, image, main_items, ingredients, masala_cost, cooking_instructions, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (recipe_name, filename, main_items, ingredients, masala_cost, cooking_instructions, session['admin_id']))
            conn.commit()
            flash('Recipe added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            conn.close()

    return render_template('add_recipe.html')

@app.route('/add_masala_to_cart', methods=['POST'])
def add_masala_to_cart():
    if 'customer_id' not in session:
        flash('You must log in to add items to the cart.', 'danger')
        return redirect(url_for('customer_login'))

    customer_id = session['customer_id']

    # Debugging: Log form data
    print("Form Data:", request.form)

    recipe_id = request.form.get('recipe_id')
    if not recipe_id:
        flash('Invalid request: recipe ID is missing.', 'danger')
        return redirect(url_for('customer_dashboard'))

    # Fetch recipe details from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT id AS recipe_id, recipe_name, image, masala_cost FROM recipes WHERE id = %s', (recipe_id,))
    recipe = cursor.fetchone()

    # Debugging: Log recipe data
    print("Fetched Recipe:", recipe)

    if not recipe:
        flash('Recipe not found.', 'danger')
        return redirect(url_for('customer_dashboard'))

    # Check if masala combo already exists in the cart
    cursor.execute('''
        SELECT id FROM cart
        WHERE customer_id = %s AND crop_id = %s AND is_masala = 1
    ''', (customer_id, recipe_id))
    existing_combo = cursor.fetchone()

    if existing_combo:
        flash('Masala combo already in your cart.', 'warning')
    else:
        # Add masala combo to the cart
        cursor.execute('''
            INSERT INTO cart (customer_id, crop_id, name, image, quantity, price, is_masala)
            VALUES (%s, %s, %s, %s, %s, %s, 1)
        ''', (customer_id, recipe_id, f"{recipe['recipe_name']} Masala", recipe['image'], 1, recipe['masala_cost']))
        conn.commit()
        flash('Masala combo added to cart.', 'success')

    conn.close()
    return redirect(url_for('view_cart'))

#Employee all routes
@app.route('/employee_register', methods=['GET', 'POST'])
def employee_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        house_address = request.form['address']
        location = request.form['location']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO employees (name, email, phone, house_address, location, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (name, email, phone, house_address, location, password))
            conn.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('employee_login'))
        except mysql.connector.IntegrityError:
            flash('Email already exists. Try a different one.', 'danger')
        finally:
            conn.close()

    return render_template('employee_register.html')

@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    # If already logged in, redirect to dashboard
    if 'employee_id' in session:
        return redirect(url_for('employee_dashboard'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM employees WHERE email = %s', (email,))
        employee = cursor.fetchone()
        conn.close()

        if employee and check_password_hash(employee['password'], password):
            session['employee_id'] = employee['id']
            session['employee_name'] = employee['name']
            session['employee_email'] = employee['email']
            session.permanent = True
            
            flash(f'Welcome back, {employee["name"]}!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('employee_dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('employee_login.html')

@app.route('/employee_orders')
def employee_orders():
    if 'employee_id' not in session:
        return redirect(url_for('login'))

    employee_id = session['employee_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch orders with food_name and image from cooked_foods
    cursor.execute("""
        SELECT co.id AS order_id, co.total_cost,co.quantity, co.ordered_time, co.status, co.address, 
               cf.food_name, cf.image
        FROM customer_orders co
        JOIN cooked_foods cf ON co.food_id = cf.id
        WHERE co.employee_id = %s
        ORDER BY co.ordered_time DESC
    """, (employee_id,))
    orders = cursor.fetchall()

    # Separate orders based on status
    pending_orders = [order for order in orders if order['status'] == 'pending']
    delivered_orders = [order for order in orders if order['status'] == 'ready to dispatch']

    return render_template(
        'employee_orders.html',
        pending_orders=pending_orders,
        delivered_orders=delivered_orders
    )

@app.route('/employee_dashboard')
def employee_dashboard():
    if 'employee_id' not in session:
        return redirect(url_for('login'))

    employee_id = session['employee_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch uploaded foods by the employee
    cursor.execute("SELECT * FROM cooked_foods WHERE employee_id = %s", (employee_id,))
    uploaded_foods = cursor.fetchall()

    # Fetch count of pending orders for this employee
    cursor.execute(
        "SELECT COUNT(*) AS order_count FROM customer_orders WHERE employee_id = %s AND status = 'Pending'", 
        (employee_id,)
    )
    order_count = cursor.fetchone()['order_count']

    return render_template(
        'employee_dashboard.html',
        uploaded_foods=uploaded_foods,
        order_count=order_count
    )


@app.route('/upload_food', methods=['GET', 'POST'])
def upload_food():
    if 'employee_id' not in session:
        flash('Please login as a homemaker to upload food.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        employee_id = session['employee_id']
        food_name = request.form['food_name']
        if food_name == 'other':
            food_name = request.form['custom_food_name']
        image = request.files['image']
        main_items = request.form['main_items']
        cooked_time = request.form['cooked_time']
        price = float(request.form['price'])

        

        # Save image
        filename = secure_filename(image.filename)
        image_path = os.path.join('static/uploads', filename)
        image.save(image_path)

        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cooked_foods (employee_id, food_name, image, main_items, cooked_time, price)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (employee_id, food_name, filename, main_items, cooked_time, price))
        conn.commit()
        conn.close()

        flash('Cooked food uploaded successfully!', 'success')
        return redirect(url_for('employee_dashboard'))

    # Fetch available dishes for dropdown
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT food_name FROM cooked_foods')
    available_dishes = [row[0] for row in cursor.fetchall()]
    conn.close()

    return render_template('upload_food.html', available_dishes=available_dishes)

@app.route('/delete_cooked_food', methods=['POST'])
def delete_cooked_food():
    if 'employee_id' not in session:
        return redirect(url_for('employee_login'))

    food_id = request.form.get('food_id')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cooked_foods WHERE id = %s AND employee_id = %s', (food_id, session['employee_id']))
    conn.commit()
    conn.close()

    flash('Food item deleted successfully.', 'success')
    return redirect(url_for('employee_dashboard'))

@app.route('/cooked_foods', methods=['GET'])
def cooked_foods():
    if 'customer_id' not in session:
        flash("Please log in to view foods.", "danger")
        return redirect(url_for('login'))

    customer_id = session['customer_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    search_query = request.args.get('search', '').strip().lower()
    filters = []
    params = []

    try:
        # Get customer's locality
        cursor.execute("SELECT location FROM customers WHERE id = %s", (customer_id,))
        customer_locality = cursor.fetchone()['location']

        # Build the query
        query = """
            SELECT f.*, e.location AS employee_locality
            FROM cooked_foods f
            JOIN employees e ON f.employee_id = e.id
        """
  # Count items in the cart
        cursor.execute('SELECT COUNT(*) AS count FROM cart WHERE customer_id = %s', (session['customer_id'],))
        cart_count = cursor.fetchone()['count']
        # Handle search logic
        if search_query and len(search_query) >= 4:
            query += """
                WHERE LOWER(f.food_name) LIKE %s
                OR LOWER(e.location) LIKE %s
            """
            search_term = f"%{search_query}%"
            filters.extend([search_term, search_term])
        else:
            # Default: prioritize customer's locality
            query += """
                ORDER BY
                    CASE
                        WHEN LOWER(e.location) LIKE %s THEN 1
                        ELSE 2
                    END, f.food_name
            """
            filters.append(f"%{customer_locality.lower()}%")

        cursor.execute(query, filters)
        cooked_foods = cursor.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        flash("An error occurred while fetching the cooked foods.", "danger")
        cooked_foods = []
    finally:
        conn.close()

    return render_template(
        'cooked_foods.html',
        cooked_foods=cooked_foods,
        search_query=search_query,
        locality=customer_locality,
        cart_count=cart_count
    )



@app.route('/add_cooked_to_cart', methods=['POST'])
def add_cooked_to_cart():
    if 'customer_id' not in session:
        return redirect(url_for('login'))

    food_id = request.form.get('food_id')
    customer_id = session['customer_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Check if the item is already in the cart
        query = "SELECT * FROM food_cart WHERE customer_id = %s AND food_id = %s"
        cursor.execute(query, (customer_id, food_id))
        cart_item = cursor.fetchone()

        if cart_item:
            # If the item exists, increment its quantity
            update_query = "UPDATE food_cart SET quantity = quantity + 1 WHERE customer_id = %s AND food_id = %s"
            cursor.execute(update_query, (customer_id, food_id))
        else:
            # If the item is not in the cart, add it
            insert_query = """
                INSERT INTO food_cart (customer_id, food_id, quantity) 
                VALUES (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE quantity = quantity + 1
            """
            cursor.execute(insert_query, (customer_id, food_id, 1))

        conn.commit()

        flash("Item added to cart!", "success")
    finally:
        conn.close()

    return redirect(url_for('cooked_foods'))



@app.route('/view_food_cart')
def view_food_cart():
    if 'customer_id' not in session:
        return redirect(url_for('customer_login'))

    customer_id = session['customer_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch cart items for the logged-in customer
        query = """
        SELECT food_cart.id AS cart_id, cooked_foods.food_name, cooked_foods.image, cooked_foods.price, 
               food_cart.quantity, (cooked_foods.price * food_cart.quantity) AS total_price
        FROM food_cart 
        JOIN cooked_foods ON food_cart.food_id = cooked_foods.id
        WHERE food_cart.customer_id = %s
        """
        cursor.execute(query, (customer_id,))
        cart_items = cursor.fetchall()

        # Calculate total amount
        total_amount = sum(item['total_price'] for item in cart_items)

    finally:
        conn.close()

    return render_template('food_cart.html', cart_items=cart_items, total_amount=total_amount)


@app.route('/update_cart_quantity', methods=['POST'])
def update_cart_quantity():
    if 'customer_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized access'}), 403

    cart_id = request.form.get('cart_id')
    action = request.form.get('action')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch current quantity and food price
        cursor.execute("SELECT quantity, food_id FROM food_cart WHERE id = %s", (cart_id,))
        cart_item = cursor.fetchone()

        if not cart_item:
            return jsonify({'status': 'error', 'message': 'Cart item not found'}), 404

        new_quantity = cart_item['quantity'] + (1 if action == 'increment' else -1)

        # Remove the item if quantity falls below 1
        if new_quantity < 1:
            cursor.execute("DELETE FROM food_cart WHERE id = %s", (cart_id,))
        else:
            # Update the new quantity
            cursor.execute("UPDATE food_cart SET quantity = %s WHERE id = %s", (new_quantity, cart_id))

        # Calculate total amount
        cursor.execute("""
            SELECT SUM(fc.quantity * cf.price) AS total_amount
            FROM food_cart fc
            JOIN cooked_foods cf ON fc.food_id = cf.id
            WHERE fc.customer_id = %s
        """, (session['customer_id'],))
        total_amount = cursor.fetchone()['total_amount'] or 0.0

        conn.commit()
        return jsonify({'status': 'success', 'total_amount': total_amount})
    except Exception as e:
        print(f"Error updating cart quantity: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred'}), 500
    finally:
        conn.close()

@app.route('/delete_cart_item', methods=['POST'])
def delete_cart_item():
    if 'customer_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized access'}), 403

    cart_id = request.form.get('cart_id')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Delete the cart item
        cursor.execute("DELETE FROM food_cart WHERE id = %s", (cart_id,))

        # Calculate total amount
        cursor.execute("""
            SELECT SUM(fc.quantity * cf.price) AS total_amount
            FROM food_cart fc
            JOIN cooked_foods cf ON fc.food_id = cf.id
            WHERE fc.customer_id = %s
        """, (session['customer_id'],))
        total_amount = cursor.fetchone()['total_amount'] or 0.0

        conn.commit()
        return jsonify({'status': 'success', 'total_amount': total_amount})
    except Exception as e:
        print(f"Error deleting cart item: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred'}), 500
    finally:
        conn.close()


def get_food_price(food_id, cursor):
    cursor.execute("SELECT price FROM cooked_foods WHERE id = %s", (food_id,))
    return cursor.fetchone()['price']

def send_email(subject, recipient, body):
    import smtplib
    from email.mime.text import MIMEText

    sender_email = "karthiku1904@gmail.com"
    sender_password = "orvg lawx wwhz ccyn"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'customer_id' not in session:
        return redirect(url_for('login'))

    customer_id = session['customer_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        address_id = request.form.get('address_id')
        
        if not address_id:
            flash("Please select a delivery address", "danger")
            return redirect(url_for('checkout'))
        
        # Get the selected address
        cursor.execute('SELECT * FROM customer_addresses WHERE id = %s AND customer_id = %s',
                      (address_id, customer_id))
        address = cursor.fetchone()
        
        if not address:
            flash("Invalid address selected", "danger")
            return redirect(url_for('checkout'))
        
        # Format address string
        address_str = f"{address['house_number']}, {address['area']}, {address['city']}, {address['state']} - {address['pincode']}"

        # Fetch cart items
        cursor.execute("SELECT * FROM food_cart WHERE customer_id = %s", (customer_id,))
        cart_items = cursor.fetchall()

        if not cart_items:
            flash("Your cart is empty!", "danger")
            return redirect(url_for('customer_dashboard'))

        # Calculate the total cost
        total_cost = 0
        for item in cart_items:
            cursor.execute("SELECT * FROM cooked_foods WHERE id = %s", (item['food_id'],))
            food = cursor.fetchone()

            if not food or 'price' not in food:
                flash("Invalid item in cart. Please refresh and try again.", "danger")
                return redirect(url_for('customer_dashboard'))

            total_cost += food['price'] * item['quantity']

        # Insert the order
        cursor.execute(
            "INSERT INTO orders (customer_id, address, total_cost, status) VALUES (%s, %s, %s, %s)",
            (customer_id, address_str, total_cost, 'Placed')
        )
        order_id = cursor.lastrowid

        # Process each item
        for item in cart_items:
            cursor.execute("SELECT * FROM cooked_foods WHERE id = %s", (item['food_id'],))
            food = cursor.fetchone()

            if not food or 'price' not in food:
                continue

            # Insert into order_items
            cursor.execute(
                "INSERT INTO order_items (order_id, food_id, quantity) VALUES (%s, %s, %s)",
                (order_id, item['food_id'], item['quantity'])
            )

            # Insert into customer_orders for employee
            cursor.execute(
                """
                INSERT INTO customer_orders (food_id, customer_id, quantity, ordered_time, status, employee_id, address, total_cost)
                VALUES (%s, %s, %s, NOW(), 'pending', %s, %s, %s)
                """,
                (item['food_id'], customer_id, item['quantity'], food['employee_id'], address_str, item['quantity'] * food['price'])
            )

        # Clear the cart
        cursor.execute("DELETE FROM food_cart WHERE customer_id = %s", (customer_id,))
        conn.commit()
        conn.close()

        flash("Order placed successfully!", "success")
        return redirect(url_for('my_orders'))

    # GET request - show checkout page
    # Get customer addresses
    cursor.execute('''
        SELECT * FROM customer_addresses 
        WHERE customer_id = %s 
        ORDER BY is_default DESC, created_at DESC
    ''', (customer_id,))
    addresses = cursor.fetchall()
    
    # Get cart details
    cursor.execute("SELECT * FROM food_cart WHERE customer_id = %s", (customer_id,))
    cart_items = cursor.fetchall()

    cart_details = []
    total_cost = 0

    for item in cart_items:
        cursor.execute("SELECT * FROM cooked_foods WHERE id = %s", (item['food_id'],))
        food = cursor.fetchone()

        if food and 'price' in food:
            food['quantity'] = item['quantity']
            total_cost += food['price'] * item['quantity']
            cart_details.append(food)

    conn.close()

    return render_template(
        'checkout_new.html',
        cart=cart_details,
        total_cost=total_cost,
        addresses=addresses
    )

@app.route('/mark_as_delivered/<int:order_id>', methods=['GET','POST'])
def mark_as_delivered(order_id):
    if 'employee_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customer_orders SET status = 'ready to dispatch' WHERE id = %s", (order_id,))
    conn.commit()
    flash("Order marked as ready to dispatch!", "success")
    return redirect(url_for('employee_orders'))


@app.route('/my_orders')
def my_orders():
    if 'customer_id' not in session:
        return redirect(url_for('login'))

    customer_id = session['customer_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch all orders for the logged-in customer
        cursor.execute(
            "SELECT * FROM orders WHERE customer_id = %s ORDER BY created_at DESC", (customer_id,)
        )
        orders = cursor.fetchall()  # Ensure fetchall() is called and result assigned.

        # Initialize an empty list if no orders
        if not orders:
            orders = []

        # Fetch items for each order
        for order in orders:
            cursor.execute(
                """
                SELECT oi.quantity, cf.food_name, cf.price
                FROM order_items oi
                JOIN cooked_foods cf ON oi.food_id = cf.id
                WHERE oi.order_id = %s
                """,
                (order['id'],)
            )
            order_items = cursor.fetchall()
            order['items'] = order_items if order_items else []  # Default to an empty list if no items.

    except Exception as e:
        print(f"Error fetching orders: {e}")
        orders = []  # Fall back to an empty list in case of error.

    return render_template('my_orders.html', orders=orders)



@app.route('/cancel_order/<int:order_id>', methods=['GET'])
def cancel_order(order_id):
    if 'customer_id' not in session:
        return redirect(url_for('login'))

    customer_id = session['customer_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Ensure the order belongs to the logged-in customer
        cursor.execute(
            "SELECT id FROM orders WHERE id = %s AND customer_id = %s", (order_id, customer_id)
        )
        order = cursor.fetchone()

        if not order:
            flash("Order not found or you don't have permission to cancel this order.", "danger")
            return redirect(url_for('my_orders'))

        # Delete associated order items first
        cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))

        # Delete the order itself
        cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        conn.commit()

        flash("Order successfully canceled.", "success")
    except Exception as e:
        conn.rollback()
        print(f"Error canceling order: {e}")
        flash("An error occurred while canceling the order. Please try again.", "danger")
    finally:
        conn.close()

    return redirect(url_for('my_orders'))

@app.route('/confirm_order/<int:order_id>', methods=['POST'])
def confirm_order(order_id):
    if 'employee_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Update the order status to 'Delivered'
    cursor.execute(
        "UPDATE customer_orders SET status = 'Delivered' WHERE id = %s AND employee_id = %s",
        (order_id, session['employee_id'])
    )
    conn.commit()

    flash("Order confirmed and marked as delivered.", "success")
    return redirect(url_for('employee_orders'))


# Route to Logout
@app.route('/logout')
def logout():
    # Clear all session data
    if 'customer_id' in session:
        session.pop('customer_id', None)
        session.pop('customer_name', None)
        session.pop('customer_email', None)
        flash('You have been logged out successfully.', 'success')
    elif 'employee_id' in session:
        session.pop('employee_id', None)
        session.pop('employee_name', None)
        session.pop('employee_email', None)
        flash('You have been logged out successfully.', 'success')
    elif current_user.is_authenticated:
        logout_user()
        flash('You have been logged out successfully.', 'success')
    
    return redirect(url_for('home'))

# Rating and Review Routes
@app.route('/add_review/<int:crop_id>', methods=['POST'])
def add_review(crop_id):
    if 'customer_id' not in session:
        return jsonify({'success': False, 'message': 'Please login to add a review'}), 401
    
    customer_id = session['customer_id']
    rating = request.form.get('rating', type=int)
    review_text = request.form.get('review_text', '').strip()
    
    if not rating or rating < 1 or rating > 5:
        return jsonify({'success': False, 'message': 'Invalid rating'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Check if user already reviewed this crop
        cursor.execute('SELECT id FROM crop_reviews WHERE crop_id = %s AND customer_id = %s', 
                      (crop_id, customer_id))
        existing_review = cursor.fetchone()
        
        if existing_review:
            return jsonify({'success': False, 'message': 'You have already reviewed this crop'}), 400
        
        # Insert new review
        cursor.execute('''
            INSERT INTO crop_reviews (crop_id, customer_id, rating, review_text)
            VALUES (%s, %s, %s, %s)
        ''', (crop_id, customer_id, rating, review_text))
        
        # Update crop average rating
        cursor.execute('''
            UPDATE crops SET 
                average_rating = (SELECT AVG(rating) FROM crop_reviews WHERE crop_id = %s),
                review_count = (SELECT COUNT(*) FROM crop_reviews WHERE crop_id = %s)
            WHERE id = %s
        ''', (crop_id, crop_id, crop_id))
        
        conn.commit()
        flash('Review added successfully!', 'success')
        return jsonify({'success': True, 'message': 'Review added successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/update_review/<int:review_id>', methods=['POST'])
def update_review(review_id):
    if 'customer_id' not in session:
        return jsonify({'success': False, 'message': 'Please login'}), 401
    
    customer_id = session['customer_id']
    rating = request.form.get('rating', type=int)
    review_text = request.form.get('review_text', '').strip()
    
    if not rating or rating < 1 or rating > 5:
        return jsonify({'success': False, 'message': 'Invalid rating'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Verify ownership
        cursor.execute('SELECT crop_id FROM crop_reviews WHERE id = %s AND customer_id = %s', 
                      (review_id, customer_id))
        review = cursor.fetchone()
        
        if not review:
            return jsonify({'success': False, 'message': 'Review not found'}), 404
        
        crop_id = review['crop_id']
        
        # Update review
        cursor.execute('''
            UPDATE crop_reviews 
            SET rating = %s, review_text = %s, updated_at = NOW()
            WHERE id = %s AND customer_id = %s
        ''', (rating, review_text, review_id, customer_id))
        
        # Update crop average rating
        cursor.execute('''
            UPDATE crops SET 
                average_rating = (SELECT AVG(rating) FROM crop_reviews WHERE crop_id = %s),
                review_count = (SELECT COUNT(*) FROM crop_reviews WHERE crop_id = %s)
            WHERE id = %s
        ''', (crop_id, crop_id, crop_id))
        
        conn.commit()
        flash('Review updated successfully!', 'success')
        return jsonify({'success': True, 'message': 'Review updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    if 'customer_id' not in session:
        return jsonify({'success': False, 'message': 'Please login'}), 401
    
    customer_id = session['customer_id']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get crop_id before deleting
        cursor.execute('SELECT crop_id FROM crop_reviews WHERE id = %s AND customer_id = %s', 
                      (review_id, customer_id))
        review = cursor.fetchone()
        
        if not review:
            return jsonify({'success': False, 'message': 'Review not found'}), 404
        
        crop_id = review['crop_id']
        
        # Delete review
        cursor.execute('DELETE FROM crop_reviews WHERE id = %s AND customer_id = %s', 
                      (review_id, customer_id))
        
        # Update crop average rating
        cursor.execute('''
            UPDATE crops SET 
                average_rating = COALESCE((SELECT AVG(rating) FROM crop_reviews WHERE crop_id = %s), 0),
                review_count = (SELECT COUNT(*) FROM crop_reviews WHERE crop_id = %s)
            WHERE id = %s
        ''', (crop_id, crop_id, crop_id))
        
        conn.commit()
        flash('Review deleted successfully!', 'success')
        return jsonify({'success': True, 'message': 'Review deleted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/get_reviews/<int:crop_id>')
def get_reviews(crop_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute('''
            SELECT cr.*, c.name as customer_name, cr.id as id
            FROM crop_reviews cr
            JOIN customers c ON cr.customer_id = c.id
            WHERE cr.crop_id = %s
            ORDER BY cr.created_at DESC
        ''', (crop_id,))
        reviews = cursor.fetchall()
        
        # Mark user's own reviews
        current_customer_id = session.get('customer_id')
        if current_customer_id:
            for review in reviews:
                review['is_own_review'] = (review['customer_id'] == current_customer_id)
        
        return jsonify({
            'success': True, 
            'reviews': reviews
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

# Customer Profile Routes
@app.route('/customer_profile')
def customer_profile():
    if 'customer_id' not in session:
        flash('Please login to view profile', 'danger')
        return redirect(url_for('customer_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get customer details
    cursor.execute('SELECT * FROM customers WHERE id = %s', (session['customer_id'],))
    customer = cursor.fetchone()
    
    # Get customer addresses
    cursor.execute('''
        SELECT * FROM customer_addresses 
        WHERE customer_id = %s 
        ORDER BY is_default DESC, created_at DESC
    ''', (session['customer_id'],))
    addresses = cursor.fetchall()
    
    conn.close()
    return render_template('customer_profile.html', customer=customer, addresses=addresses)

@app.route('/update_customer_profile', methods=['POST'])
def update_customer_profile():
    if 'customer_id' not in session:
        flash('Please login to update profile', 'danger')
        return redirect(url_for('customer_login'))
    
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    location = request.form.get('location')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE customers 
            SET name = %s, email = %s, phone = %s, location = %s
            WHERE id = %s
        ''', (name, email, phone, location, session['customer_id']))
        
        conn.commit()
        
        # Update session data
        session['customer_name'] = name
        session['customer_email'] = email
        
        flash('Profile updated successfully!', 'success')
    except mysql.connector.IntegrityError as e:
        conn.rollback()
        if 'Duplicate entry' in str(e):
            if 'email' in str(e):
                flash('Email already in use by another account', 'danger')
            elif 'phone' in str(e):
                flash('Phone number already in use by another account', 'danger')
        else:
            flash('Error updating profile', 'danger')
    except Exception as e:
        conn.rollback()
        flash(f'Error updating profile: {str(e)}', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('customer_profile'))

@app.route('/add_address', methods=['POST'])
def add_address():
    if 'customer_id' not in session:
        return jsonify({'success': False, 'message': 'Please login'}), 401
    
    customer_id = session['customer_id']
    address_type = request.form.get('address_type', 'Home')
    house_number = request.form.get('house_number')
    area = request.form.get('area')
    landmark = request.form.get('landmark')
    pincode = request.form.get('pincode')
    city = request.form.get('city')
    district = request.form.get('district')
    state = request.form.get('state')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    is_default = request.form.get('is_default', 0)
    redirect_to = request.form.get('redirect_to', 'profile')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # If this is default, unset other defaults
        if is_default:
            cursor.execute('UPDATE customer_addresses SET is_default = 0 WHERE customer_id = %s', 
                         (customer_id,))
        
        cursor.execute('''
            INSERT INTO customer_addresses 
            (customer_id, address_type, house_number, area, landmark, pincode, 
             city, district, state, latitude, longitude, is_default)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (customer_id, address_type, house_number, area, landmark, pincode,
              city, district, state, latitude, longitude, is_default))
        
        conn.commit()
        flash('Address added successfully!', 'success')
        
        # Redirect based on where user came from
        if redirect_to == 'checkout':
            return redirect(url_for('checkout'))
        else:
            return redirect(url_for('customer_profile'))
    except Exception as e:
        conn.rollback()
        flash(f'Error adding address: {str(e)}', 'danger')
        return redirect(url_for('customer_profile'))
    finally:
        conn.close()

@app.route('/delete_address/<int:address_id>', methods=['POST'])
def delete_address(address_id):
    if 'customer_id' not in session:
        return jsonify({'success': False}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM customer_addresses WHERE id = %s AND customer_id = %s',
                  (address_id, session['customer_id']))
    conn.commit()
    conn.close()
    
    flash('Address deleted successfully!', 'success')
    return redirect(url_for('customer_profile'))

@app.route('/set_default_address/<int:address_id>', methods=['POST'])
def set_default_address(address_id):
    if 'customer_id' not in session:
        return jsonify({'success': False}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Unset all defaults
    cursor.execute('UPDATE customer_addresses SET is_default = 0 WHERE customer_id = %s',
                  (session['customer_id'],))
    # Set new default
    cursor.execute('UPDATE customer_addresses SET is_default = 1 WHERE id = %s AND customer_id = %s',
                  (address_id, session['customer_id']))
    
    conn.commit()
    conn.close()
    
    flash('Default address updated!', 'success')
    return redirect(url_for('customer_profile'))

# Farmer Analytics Routes
@app.route('/farmer_analytics')
@login_required
def farmer_analytics():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get sales data
    cursor.execute('''
        SELECT 
            DATE(sale_date) as date,
            SUM(quantity_sold) as total_quantity,
            SUM(sale_amount) as total_revenue
        FROM sales_analytics
        WHERE farmer_id = %s
        GROUP BY DATE(sale_date)
        ORDER BY date DESC
        LIMIT 30
    ''', (current_user.id,))
    sales_data = cursor.fetchall()
    
    # Get top selling products
    cursor.execute('''
        SELECT 
            c.crop_name,
            SUM(sa.quantity_sold) as total_sold,
            SUM(sa.sale_amount) as revenue
        FROM sales_analytics sa
        JOIN crops c ON sa.crop_id = c.id
        WHERE sa.farmer_id = %s
        GROUP BY c.id
        ORDER BY total_sold DESC
        LIMIT 5
    ''', (current_user.id,))
    top_products = cursor.fetchall()
    
    # Get overall stats
    cursor.execute('''
        SELECT 
            COUNT(DISTINCT customer_id) as total_customers,
            SUM(quantity_sold) as total_quantity,
            SUM(sale_amount) as total_revenue
        FROM sales_analytics
        WHERE farmer_id = %s
    ''', (current_user.id,))
    stats = cursor.fetchone()
    
    conn.close()
    return render_template('farmer_analytics.html', 
                         sales_data=sales_data, 
                         top_products=top_products,
                         stats=stats)

@app.route('/toggle_crop_availability/<int:crop_id>', methods=['POST'])
@login_required
def toggle_crop_availability(crop_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Verify ownership
    cursor.execute('SELECT is_available FROM crops WHERE id = %s AND farmer_id = %s',
                  (crop_id, current_user.id))
    crop = cursor.fetchone()
    
    if not crop:
        flash('Crop not found', 'danger')
        return redirect(url_for('farmer_dashboard'))
    
    new_status = 0 if crop['is_available'] else 1
    cursor.execute('UPDATE crops SET is_available = %s WHERE id = %s',
                  (new_status, crop_id))
    conn.commit()
    conn.close()
    
    status_text = 'available' if new_status else 'unavailable'
    flash(f'Crop marked as {status_text}!', 'success')
    return redirect(url_for('farmer_dashboard'))

@app.route('/update_crop_quantity/<int:crop_id>', methods=['POST'])
@login_required
def update_crop_quantity_route(crop_id):
    quantity = request.form.get('quantity', type=int)
    
    if quantity is None or quantity < 0:
        flash('Invalid quantity', 'danger')
        return redirect(url_for('farmer_dashboard'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE crops 
        SET quantity = %s, is_available = IF(%s > 0, 1, 0)
        WHERE id = %s AND farmer_id = %s
    ''', (quantity, quantity, crop_id, current_user.id))
    
    conn.commit()
    conn.close()
    
    flash('Quantity updated successfully!', 'success')
    return redirect(url_for('farmer_dashboard'))

# Admin Product Management Routes
@app.route('/admin_products')
def admin_products():
    if 'admin_id' not in session:
        flash('Please login as admin', 'danger')
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('''
        SELECT c.*, f.name as farmer_name, f.location as farmer_location
        FROM crops c
        JOIN farmers f ON c.farmer_id = f.id
        ORDER BY c.created_at DESC
    ''')
    products = cursor.fetchall()
    
    conn.close()
    return render_template('admin_products.html', products=products)

@app.route('/admin_toggle_product/<int:crop_id>', methods=['POST'])
def admin_toggle_product(crop_id):
    if 'admin_id' not in session:
        return jsonify({'success': False}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT is_available FROM crops WHERE id = %s', (crop_id,))
    crop = cursor.fetchone()
    
    new_status = 0 if crop['is_available'] else 1
    cursor.execute('UPDATE crops SET is_available = %s WHERE id = %s',
                  (new_status, crop_id))
    
    # Log admin activity
    cursor.execute('''
        INSERT INTO admin_activity_log (admin_id, action_type, description, target_id, target_type)
        VALUES (%s, %s, %s, %s, %s)
    ''', (session['admin_id'], 'toggle_availability', 
          f'Changed product availability to {new_status}', crop_id, 'crop'))
    
    conn.commit()
    conn.close()
    
    flash('Product availability updated!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin_add_offer/<int:crop_id>', methods=['POST'])
def admin_add_offer(crop_id):
    if 'admin_id' not in session:
        return jsonify({'success': False}), 401
    
    offer_name = request.form.get('offer_name')
    discount = request.form.get('discount', type=float)
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO product_offers 
        (crop_id, offer_name, discount_percentage, start_date, end_date, created_by)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (crop_id, offer_name, discount, start_date, end_date, session['admin_id']))
    
    # Update crop discount
    cursor.execute('UPDATE crops SET discount = %s WHERE id = %s', (discount, crop_id))
    
    conn.commit()
    conn.close()
    
    flash('Offer added successfully!', 'success')
    return redirect(url_for('admin_products'))

# Admin View/Edit Routes
@app.route('/admin/farmer/<int:farmer_id>')
def admin_view_farmer(farmer_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get farmer details
    cursor.execute('SELECT * FROM farmers WHERE id = %s', (farmer_id,))
    farmer = cursor.fetchone()
    
    # Get farmer's products
    cursor.execute('''
        SELECT * FROM crops 
        WHERE farmer_id = %s 
        ORDER BY created_at DESC
    ''', (farmer_id,))
    products = cursor.fetchall()
    
    conn.close()
    
    if not farmer:
        return jsonify({'success': False, 'message': 'Farmer not found'}), 404
    
    return jsonify({
        'success': True,
        'farmer': farmer,
        'products': products
    })

@app.route('/admin/farmer/<int:farmer_id>/edit', methods=['POST'])
def admin_edit_farmer(farmer_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    name = request.form.get('name')
    phone = request.form.get('phone')
    location = request.form.get('location')
    age = request.form.get('age')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE farmers 
            SET name = %s, phone = %s, location = %s, age = %s
            WHERE id = %s
        ''', (name, phone, location, age, farmer_id))
        
        conn.commit()
        conn.close()
        
        flash('Farmer updated successfully!', 'success')
        return jsonify({'success': True, 'message': 'Farmer updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/customer/<int:customer_id>')
def admin_view_customer(customer_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get customer details
    cursor.execute('SELECT * FROM customers WHERE id = %s', (customer_id,))
    customer = cursor.fetchone()
    
    # Get customer's addresses
    cursor.execute('''
        SELECT * FROM customer_addresses 
        WHERE customer_id = %s 
        ORDER BY is_default DESC
    ''', (customer_id,))
    addresses = cursor.fetchall()
    
    # Get customer's orders
    cursor.execute('''
        SELECT * FROM orders 
        WHERE customer_id = %s 
        ORDER BY created_at DESC 
        LIMIT 10
    ''', (customer_id,))
    orders = cursor.fetchall()
    
    conn.close()
    
    if not customer:
        return jsonify({'success': False, 'message': 'Customer not found'}), 404
    
    return jsonify({
        'success': True,
        'customer': customer,
        'addresses': addresses,
        'orders': orders
    })

@app.route('/admin/product/<int:product_id>')
def admin_view_product(product_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get product details with farmer info
    cursor.execute('''
        SELECT c.*, f.name as farmer_name, f.phone as farmer_phone, f.location as farmer_location
        FROM crops c
        JOIN farmers f ON c.farmer_id = f.id
        WHERE c.id = %s
    ''', (product_id,))
    product = cursor.fetchone()
    
    # Get product reviews
    cursor.execute('''
        SELECT cr.*, cu.name as customer_name
        FROM crop_reviews cr
        JOIN customers cu ON cr.customer_id = cu.id
        WHERE cr.crop_id = %s
        ORDER BY cr.created_at DESC
    ''', (product_id,))
    reviews = cursor.fetchall()
    
    conn.close()
    
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404
    
    return jsonify({
        'success': True,
        'product': product,
        'reviews': reviews
    })

@app.route('/admin/product/<int:product_id>/edit', methods=['POST'])
def admin_edit_product(product_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    crop_name = request.form.get('crop_name')
    price_per_kg = request.form.get('price_per_kg')
    quantity = request.form.get('quantity')
    discount = request.form.get('discount', 0)
    description = request.form.get('description')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE crops 
            SET crop_name = %s, price_per_kg = %s, quantity = %s, 
                discount = %s, description = %s,
                mrp = %s, is_available = %s
            WHERE id = %s
        ''', (crop_name, price_per_kg, quantity, discount, description,
              float(price_per_kg) * 1.2, 1 if int(quantity) > 0 else 0, product_id))
        
        conn.commit()
        conn.close()
        
        flash('Product updated successfully!', 'success')
        return jsonify({'success': True, 'message': 'Product updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
