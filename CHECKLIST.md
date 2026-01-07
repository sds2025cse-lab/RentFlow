# RentFlow Configuration Checklist

## Pre-Deployment Checklist

### 1. Installation ✅
- [ ] Clone or download project
- [ ] Create virtual environment
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env`

### 2. Environment Configuration
- [ ] Set `FLASK_ENV` (development/production)
- [ ] Set `SECRET_KEY` to random secure string
- [ ] Set database URL (SQLite by default)
- [ ] Configure Stripe keys:
  - [ ] Get API keys from https://stripe.com
  - [ ] Add `STRIPE_PUBLIC_KEY`
  - [ ] Add `STRIPE_SECRET_KEY`

### 3. Database Setup ✅
- [ ] Database will auto-create on first run
- [ ] Tables: User, Product, Category, CartItem, Order, OrderItem, Review
- [ ] Create admin user (see SETUP.md)
- [ ] Add sample products (see SETUP.md)

### 4. Email Configuration (Optional)
- [ ] Set MAIL_SERVER (for notifications)
- [ ] Set MAIL_PORT
- [ ] Set MAIL_USERNAME
- [ ] Set MAIL_PASSWORD

### 5. Testing
- [ ] Test user registration
- [ ] Test user login
- [ ] Test product browsing
- [ ] Test add to cart
- [ ] Test checkout with test Stripe card:
  - Card: 4242 4242 4242 4242
  - Expiry: 12/25 (any future date)
  - CVC: 123
- [ ] Test order creation
- [ ] Test admin panel access

### 6. Customization
- [ ] Change brand name/logo in templates
- [ ] Update colors in base.html CSS
- [ ] Customize product categories
- [ ] Add company information
- [ ] Update contact information
- [ ] Configure tax rates (if needed)

### 7. Security (For Production)
- [ ] Change `SECRET_KEY` (never use default)
- [ ] Set `FLASK_ENV=production`
- [ ] Enable HTTPS
- [ ] Set strong password requirements
- [ ] Configure CORS if needed
- [ ] Set up rate limiting
- [ ] Configure session timeout
- [ ] Enable SQL injection prevention (built-in with SQLAlchemy)

### 8. Performance (For Production)
- [ ] Enable caching
- [ ] Configure database for production (PostgreSQL recommended)
- [ ] Set up logging
- [ ] Configure backups
- [ ] Monitor application errors
- [ ] Set up CDN for static files

### 9. Deployment
- [ ] Choose hosting platform (AWS, Heroku, DigitalOcean, etc.)
- [ ] Install production WSGI server (Gunicorn)
- [ ] Configure environment variables on server
- [ ] Set up database on production server
- [ ] Run migrations if needed
- [ ] Configure domain name
- [ ] Set up SSL certificate
- [ ] Configure email service

### 10. Monitoring & Maintenance
- [ ] Set up error logging
- [ ] Monitor server resources
- [ ] Regular database backups
- [ ] Keep dependencies updated
- [ ] Monitor Stripe transactions
- [ ] Check user feedback
- [ ] Update product inventory regularly

## Environment Variables Reference

```
# Flask Settings
FLASK_ENV=development|production
FLASK_DEBUG=True|False
SECRET_KEY=your-secure-key-here

# Database
DATABASE_URL=sqlite:///rentflow.db

# Stripe
STRIPE_PUBLIC_KEY=pk_test_xxxxx
STRIPE_SECRET_KEY=sk_test_xxxxx

# Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Application
ITEMS_PER_PAGE=12
MAX_CONTENT_LENGTH=16777216
```

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python run.py

# Flask shell (for database operations)
python -c "from app import create_app; app = create_app(); app.app_context().push()"

# Reset database
rm rentflow.db
python run.py

# Create admin user
python
>>> from app import create_app, db
>>> from app.models import User, UserRole
>>> app = create_app()
>>> with app.app_context():
>>>     admin = User(username='admin', email='admin@rentflow.com', role=UserRole.ADMIN)
>>>     admin.set_password('password123')
>>>     db.session.add(admin)
>>>     db.session.commit()

# Run with Gunicorn (production)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### Issue: Database locked
**Solution**: Delete database and restart
```bash
rm rentflow.db
python run.py
```

### Issue: Port 5000 already in use
**Solution**: Change port in run.py
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changed from 5000
```

### Issue: Stripe payments not working
**Solution**: 
1. Verify API keys in .env
2. Use test mode keys for development
3. Check Stripe dashboard for errors
4. Ensure test card is used: 4242 4242 4242 4242

### Issue: Import errors
**Solution**: Ensure virtual environment is activated
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## File Locations

- **Configuration**: `.env`
- **Database**: `rentflow.db`
- **Templates**: `app/templates/`
- **Static files**: `app/static/` (not included yet)
- **Database models**: `app/models.py`
- **Routes**: `app/routes/`

## Support Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Stripe API: https://stripe.com/docs/api
- Bootstrap: https://getbootstrap.com/
- Python: https://docs.python.org/3/

## Post-Launch Checklist

- [ ] Monitor user registrations
- [ ] Track payment transactions
- [ ] Respond to customer inquiries
- [ ] Update product inventory
- [ ] Review analytics
- [ ] Fix reported bugs
- [ ] Add new features based on feedback
- [ ] Regular security audits
- [ ] Update dependencies

---

**Status**: ✅ Complete and Ready to Deploy!

Start with Step 1-3 above to get running immediately.
