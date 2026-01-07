from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_, desc
from app import db
from app.models import Product, Category, CartItem, Review, Order, OrderItem, OrderStatus
from app.forms import AddToCartForm, ReviewForm, SearchForm
import uuid
from datetime import datetime

products_bp = Blueprint('products', __name__, url_prefix='/products')


@products_bp.route('/')
def index():
    """Product listing with filters"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search_q = request.args.get('q', '')
    sort_by = request.args.get('sort', 'newest')
    
    query = Product.query.filter_by(is_active=True)
    
    # Category filter
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Search filter
    if search_q:
        query = query.filter(or_(
            Product.name.ilike(f'%{search_q}%'),
            Product.description.ilike(f'%{search_q}%')
        ))
    
    # Sorting
    if sort_by == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'rating':
        query = query.order_by(desc(Product.rating))
    else:  # newest
        query = query.order_by(desc(Product.created_at))
    
    products = query.paginate(page=page, per_page=12)
    categories = Category.query.all()
    
    return render_template('products/index.html', 
                          products=products, 
                          categories=categories,
                          search_q=search_q,
                          selected_category=category_id)


@products_bp.route('/<slug>')
def detail(slug):
    """Product detail page"""
    product = Product.query.filter_by(slug=slug).first_or_404()
    
    if not product.is_active:
        return redirect(url_for('products.index'))
    
    form = AddToCartForm()
    reviews = Review.query.filter_by(product_id=product.id).order_by(desc(Review.created_at)).all()
    avg_rating = product.get_average_rating()
    review_form = ReviewForm()
    
    return render_template('products/detail.html',
                          product=product,
                          form=form,
                          reviews=reviews,
                          avg_rating=avg_rating,
                          review_form=review_form)


@products_bp.route('/<int:product_id>/add-review', methods=['POST'])
@login_required
def add_review(product_id):
    """Add product review"""
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()
    
    if form.validate_on_submit():
        review = Review(
            title=form.title.data,
            content=form.content.data,
            rating=int(form.rating.data),
            product_id=product_id,
            user_id=current_user.id
        )
        db.session.add(review)
        
        # Update product rating
        product.review_count += 1
        product.rating = product.get_average_rating()
        
        db.session.commit()
        flash('Review added successfully', 'success')
    else:
        flash('Error adding review', 'danger')
    
    return redirect(url_for('products.detail', slug=product.slug))


@products_bp.route('/category/<slug>')
def category(slug):
    """View products by category"""
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    
    products = Product.query.filter_by(
        category_id=category.id,
        is_active=True
    ).order_by(desc(Product.created_at)).paginate(page=page, per_page=12)
    
    categories = Category.query.all()
    
    return render_template('products/category.html',
                          category=category,
                          products=products,
                          categories=categories)
