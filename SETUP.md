# RentFlow E-Commerce Website - Installation & Setup Guide

## Complete E-Commerce Rental Platform

RentFlow is a full-featured e-commerce website built with Flask for equipment rental. It includes user authentication, product management, shopping cart, payments via Stripe, and an admin dashboard.

## What's Included

✅ **Complete Backend**
- Flask application with modular blueprint structure
- SQLAlchemy ORM with 7 database models
- User authentication with Flask-Login
- Form validation with Flask-WTF
- Stripe payment integration

✅ **Frontend Templates**
- 20+ HTML templates with Bootstrap 5
- Responsive design for all devices
- Product browsing & search
- Shopping cart & checkout
- User dashboard
- Admin dashboard

✅ **Features**
- User registration & login
- Product listing with filtering & search
- Shopping cart functionality
- Secure checkout process
- Stripe payment processing
- Order management
- Product reviews & ratings
- Admin panel for product/order/user management
- User profile management

## Quick Installation

### Step 1: Install Dependencies
```bash
cd RentFlow
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### Step 3: Run Application
```bash
python run.py
```

Application runs on: **http://localhost:5000**

## First-Time Setup

### Create Sample Data

Open Python shell and run:
```python
python
>>> from app import create_app, db
>>> from app.models import Category, Product, User, UserRole
>>> 
>>> app = create_app()
>>> with app.app_context():
>>>     # Create categories
>>>     tools = Category(name='Tools', slug='tools', description='Power tools and hand tools')
>>>     equipment = Category(name='Equipment', slug='equipment', description='Heavy equipment and machinery')
>>>     db.session.add_all([tools, equipment])
>>>     db.session.commit()
>>>     
>>>     # Create sample products
>>>     drill = Product(name='Power Drill', slug='power-drill', price=15.00, category_id=1, 
>>>                     stock=10, description='Professional power drill')
>>>     ladder = Product(name='Extension Ladder', slug='extension-ladder', price=10.00, 
>>>                     category_id=1, stock=5, description='20ft extension ladder')
>>>     db.session.add_all([drill, ladder])
>>>     db.session.commit()
>>>     
>>>     # Create admin user
>>>     admin = User(username='admin', email='admin@rentflow.com', role=UserRole.ADMIN)
>>>     admin.set_password('admin123')
>>>     db.session.add(admin)
>>>     db.session.commit()
>>>     
>>>     print('Sample data created!')
>>> exit()
```

### Test User Accounts

**Admin Account:**
- Email: `admin@rentflow.com`
- Password: `admin123`
- Access: http://localhost:5000/admin

**Register New User:**
- Go to Register page
- Create account and login
- Browse products and add to cart

## Stripe Testing

Use these test credentials in payment form:
- **Card Number**: 4242 4242 4242 4242
- **Expiry**: 12/25 (or any future date)
- **CVC**: 123

## Project Structure

```
RentFlow/
├── app/
│   ├── templates/              # 20+ HTML templates
│   │   ├── base.html          # Main layout template
│   │   ├── index.html         # Home page
│   │   ├── about.html         # About page
│   │   ├── contact.html       # Contact page
│   │   ├── auth/              # Login, Register, Profile
│   │   ├── products/          # Product listing, detail, category
│   │   ├── cart/              # Cart view, checkout
│   │   ├── orders/            # Order list, detail, payment
│   │   └── admin/             # Admin dashboard, product/order management
│   │
│   ├── routes/                 # Flask blueprints
│   │   ├── main.py           # Home, about, contact routes
│   │   ├── auth.py           # Authentication routes
│   │   ├── products.py       # Product routes
│   │   ├── cart.py           # Shopping cart routes
│   │   ├── orders.py         # Order routes
│   │   └── admin.py          # Admin routes
│   │
│   ├── __init__.py            # Flask app factory
│   ├── config.py              # Configuration settings
│   ├── models.py              # Database models (7 models)
│   ├── forms.py               # WTForms validation forms
│   └── static/                # CSS, JS, images (if added)
│
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # Original readme
```

## Database Models

1. **User** - User accounts with roles (Customer, Vendor, Admin)
2. **Category** - Product categories
3. **Product** - Products with pricing, stock, ratings
4. **CartItem** - Shopping cart items
5. **Order** - Order history with status tracking
6. **OrderItem** - Individual items in orders
7. **Review** - Product reviews and ratings

## File Count Summary

- **Templates**: 20+ HTML files
- **Routes**: 6 blueprint modules
- **Models**: 7 database models
- **Forms**: 10+ form classes
- **Total Python Files**: 20+
- **Total Configuration Files**: 2

## Key URLs

**Public Pages:**
- `/` - Home page
- `/products/` - Product listing
- `/products/<slug>` - Product detail
- `/products/category/<slug>` - Category products
- `/about` - About page
- `/contact` - Contact page

**Authentication:**
- `/auth/register` - User registration
- `/auth/login` - User login
- `/auth/logout` - User logout
- `/auth/profile` - User profile
- `/auth/profile/edit` - Edit profile

**Shopping:**
- `/cart/` - View cart
- `/cart/add/<id>` - Add to cart
- `/cart/checkout` - Checkout form
- `/orders/` - My orders
- `/orders/<id>` - Order details
- `/orders/<id>/payment` - Payment page

**Admin:**
- `/admin/` - Admin dashboard
- `/admin/products` - Manage products
- `/admin/products/new` - Create product
- `/admin/products/<id>/edit` - Edit product
- `/admin/orders` - Manage orders
- `/admin/users` - Manage users
- `/admin/categories` - Manage categories

## Environment Variables

```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=change-this-in-production

DATABASE_URL=sqlite:///rentflow.db

STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key

ITEMS_PER_PAGE=12
MAX_CONTENT_LENGTH=16777216
```

## Features Breakdown

### User Features
✅ Registration with email validation
✅ Login/logout with session management
✅ Profile management
✅ Browse products by category
✅ Search products
✅ Filter & sort products
✅ View product details & reviews
✅ Leave product reviews
✅ Add/remove items to cart
✅ Update cart quantities
✅ Checkout process
✅ Stripe payment integration
✅ View order history
✅ Track order status
✅ Cancel orders

### Admin Features
✅ Dashboard with analytics
✅ View total users, products, orders, revenue
✅ Create new products
✅ Edit product details
✅ Delete products
✅ View all orders
✅ Update order status
✅ View customer list
✅ Manage categories
✅ View recent orders

## Database

Default: SQLite (`rentflow.db`)
Can be upgraded to PostgreSQL by changing `DATABASE_URL`

## Deployment

### Development
```bash
python run.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## Customization

### Change Brand Name
Search `RentFlow` in templates and replace with your brand

### Customize Colors
Edit CSS in `base.html` `:root` variables:
- `--primary-color`
- `--secondary-color`
- `--dark-color`
- `--light-color`

### Add More Products
Use admin panel or Python shell with sample data script

### Configure Stripe
1. Go to https://stripe.com
2. Get test API keys
3. Add to `.env` file

## Troubleshooting

**Cannot import modules**
- Run: `pip install -r requirements.txt`

**Database errors**
- Delete `rentflow.db`
- Restart application

**Port already in use**
- Change port in `run.py`: `app.run(port=5001)`

**Stripe errors**
- Verify API keys in `.env`
- Check Stripe dashboard for test mode

## Production Checklist

- [ ] Change `SECRET_KEY` to random string
- [ ] Set `FLASK_ENV=production`
- [ ] Add real Stripe keys
- [ ] Configure database (PostgreSQL recommended)
- [ ] Enable HTTPS
- [ ] Set up email for notifications
- [ ] Configure logging
- [ ] Run on production WSGI server
- [ ] Set up backups
- [ ] Monitor application

## Support & Resources

- Flask Documentation: https://flask.palletsprojects.com
- SQLAlchemy: https://www.sqlalchemy.org
- Stripe API: https://stripe.com/docs
- Bootstrap: https://getbootstrap.com

---

**RentFlow E-Commerce Platform** - Complete and ready to deploy! 🚀
