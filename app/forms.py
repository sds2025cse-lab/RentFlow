from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange
from app.models import User


class LoginForm(FlaskForm):
    """Login form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                      validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    first_name = StringField('First Name', validators=[Length(max=120)])
    last_name = StringField('Last Name', validators=[Length(max=120)])
    submit = SubmitField('Register')
    
    def validate_username(self, field):
        """Check if username already exists"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken.')
    
    def validate_email(self, field):
        """Check if email already exists"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class UpdateProfileForm(FlaskForm):
    """Update user profile form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[Length(max=120)])
    last_name = StringField('Last Name', validators=[Length(max=120)])
    phone = StringField('Phone', validators=[Length(max=20)])
    address = TextAreaField('Address')
    city = StringField('City', validators=[Length(max=120)])
    state = StringField('State', validators=[Length(max=120)])
    postal_code = StringField('Postal Code', validators=[Length(max=20)])
    country = StringField('Country', validators=[Length(max=120)])
    submit = SubmitField('Update Profile')


class AddToCartForm(FlaskForm):
    """Add to cart form"""
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add to Cart')


class ReviewForm(FlaskForm):
    """Product review form"""
    title = StringField('Title', validators=[Length(max=200)])
    rating = SelectField('Rating', choices=[('5', '⭐ Excellent'), ('4', '⭐⭐⭐⭐ Very Good'), 
                                             ('3', '⭐⭐⭐ Good'), ('2', '⭐⭐ Fair'), 
                                             ('1', '⭐ Poor')], validators=[DataRequired()])
    content = TextAreaField('Review', validators=[DataRequired(), Length(min=10, max=5000)])
    submit = SubmitField('Submit Review')


class SearchForm(FlaskForm):
    """Search form"""
    q = StringField('Search', validators=[DataRequired()])
    category = SelectField('Category', coerce=int)
    sort_by = SelectField('Sort By', choices=[('newest', 'Newest'), ('price_low', 'Price: Low to High'),
                                               ('price_high', 'Price: High to Low'), ('rating', 'Top Rated')])
    submit = SubmitField('Search')


class CheckoutForm(FlaskForm):
    """Checkout form"""
    shipping_name = StringField('Full Name', validators=[DataRequired()])
    shipping_email = StringField('Email', validators=[DataRequired(), Email()])
    shipping_phone = StringField('Phone', validators=[DataRequired()])
    shipping_address = TextAreaField('Address', validators=[DataRequired()])
    shipping_city = StringField('City', validators=[DataRequired()])
    shipping_state = StringField('State/Province')
    shipping_postal_code = StringField('Postal Code', validators=[DataRequired()])
    shipping_country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Continue to Payment')


class AdminProductForm(FlaskForm):
    """Admin product creation/editing form"""
    name = StringField('Product Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    stock = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    sku = StringField('SKU')
    rental_period_days = IntegerField('Rental Period (days)', validators=[NumberRange(min=1)])
    submit = SubmitField('Save Product')
