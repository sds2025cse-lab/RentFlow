# RentFlow - Quick Reference Guide

## 🚀 Start Here

### 1. Installation (2 minutes)
```bash
cd RentFlow
pip install -r requirements.txt
python run.py
```

Open: http://localhost:5000

### 2. First Login
```
Email: admin@rentflow.com
Password: admin123
```

### 3. Test Payment
```
Card: 4242 4242 4242 4242
Expiry: 12/25
CVC: 123
```

---

## 📍 Navigation Map

```
HOME (/)
├── Products (/products)
│   ├── Category (/products/category/<slug>)
│   └── Detail (/products/<slug>)
├── Auth
│   ├── Register (/auth/register)
│   ├── Login (/auth/login)
│   └── Profile (/auth/profile)
├── Shopping
│   ├── Cart (/cart)
│   ├── Checkout (/cart/checkout)
│   └── Orders (/orders)
├── Admin (/admin)
│   ├── Dashboard
│   ├── Products
│   ├── Orders
│   ├── Users
│   └── Categories
├── About (/about)
└── Contact (/contact)
```

---

## 🗂️ File Quick Reference

### Important Files
- `run.py` - Start here
- `app/__init__.py` - App configuration
- `app/models.py` - Database structure
- `app/forms.py` - Form validation
- `.env.example` - Settings template

### Key Routes
- `app/routes/main.py` - Home pages
- `app/routes/auth.py` - Login/Register
- `app/routes/products.py` - Product browsing
- `app/routes/cart.py` - Shopping cart
- `app/routes/orders.py` - Orders & payments
- `app/routes/admin.py` - Admin panel

### Key Templates
- `base.html` - Navigation & layout
- `index.html` - Homepage
- `products/index.html` - Product list
- `cart/view.html` - Shopping cart
- `orders/payment.html` - Payment page
- `admin/dashboard.html` - Admin panel

---

## 💾 Database Tables

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| users | User accounts | email, password, role |
| products | Product catalog | name, price, stock |
| categories | Product categories | name, slug |
| cart_items | Shopping cart | user_id, product_id |
| orders | Order history | order_number, status |
| order_items | Items in orders | order_id, product_id |
| reviews | Product reviews | rating, content |

---

## 🔑 Key Features

### For Customers
- Browse products
- Search & filter
- Read reviews
- Add to cart
- Checkout
- Pay with Stripe
- Track orders

### For Admins
- Create products
- Edit/delete products
- Manage orders
- Manage users
- View analytics
- Update order status

---

## 📦 Dependencies

```
Flask              - Web framework
SQLAlchemy         - Database ORM
Flask-Login        - Authentication
Flask-WTF          - Forms & CSRF
Stripe             - Payments
Bootstrap 5        - UI framework
```

All included in `requirements.txt`

---

## 🛠️ Common Tasks

### Add a Product
1. Login as admin
2. Go to /admin
3. Click "Add Product"
4. Fill form and submit

### Create Admin User
```python
from app import create_app, db
from app.models import User, UserRole

app = create_app()
with app.app_context():
    admin = User(username='admin', email='admin@rentflow.com', role=UserRole.ADMIN)
    admin.set_password('password123')
    db.session.add(admin)
    db.session.commit()
```

### Reset Database
```bash
rm rentflow.db
python run.py
```

### Change Settings
Edit `.env` file:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
STRIPE_PUBLIC_KEY=your-key
STRIPE_SECRET_KEY=your-key
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | `pip install -r requirements.txt` |
| Port in use | Change port in run.py |
| Database error | Delete rentflow.db |
| Stripe error | Check API keys in .env |
| Template error | Check syntax in HTML files |

---

## 🔍 Testing Checklist

- [ ] Register new user
- [ ] Login as user
- [ ] Browse products
- [ ] Search for product
- [ ] Add to cart
- [ ] Proceed to checkout
- [ ] Complete Stripe payment
- [ ] View order
- [ ] Login as admin
- [ ] Add new product
- [ ] View admin dashboard

---

## 📚 Documentation

- **SETUP.md** - Full setup instructions
- **CHECKLIST.md** - Pre-launch checklist
- **PROJECT_COMPLETE.md** - Complete overview
- **BUILD_SUMMARY.md** - Build details

---

## 🚀 Deployment

### Local
```bash
python run.py
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### Heroku
1. Create Procfile
2. Add heroku remote
3. Push to Heroku

---

## 📞 Help

1. Read SETUP.md for installation
2. Check CHECKLIST.md for issues
3. Review code comments
4. Check framework documentation

---

## ✅ Status

- **Backend**: ✅ Complete
- **Frontend**: ✅ Complete
- **Database**: ✅ Complete
- **Admin**: ✅ Complete
- **Payments**: ✅ Complete
- **Authentication**: ✅ Complete

---

## 🎯 What's Next

1. Add email notifications
2. Deploy to cloud
3. Add more features
4. Scale the business
5. Expand product catalog

---

**Ready to launch? Start with: `python run.py`**

Questions? Check the documentation files.

**Happy coding! 🚀**
