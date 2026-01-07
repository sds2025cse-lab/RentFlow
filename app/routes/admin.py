from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import User, Product, Category, Order, UserRole, OrderStatus
from app.forms import AdminProductForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != UserRole.ADMIN:
            flash('Admin access required', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total)).filter(
        Order.status == OrderStatus.DELIVERED
    ).scalar() or 0
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                          total_users=total_users,
                          total_products=total_products,
                          total_orders=total_orders,
                          total_revenue=total_revenue,
                          recent_orders=recent_orders)


@admin_bp.route('/products')
@login_required
@admin_required
def products():
    """Manage products"""
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=20)
    return render_template('admin/products.html', products=products)


@admin_bp.route('/products/new', methods=['GET', 'POST'])
@login_required
@admin_required
def create_product():
    """Create new product"""
    form = AdminProductForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            slug=form.name.data.lower().replace(' ', '-'),
            description=form.description.data,
            price=form.price.data,
            category_id=form.category.data,
            stock=form.stock.data,
            sku=form.sku.data,
            rental_period_days=form.rental_period_days.data or 7,
            is_active=True
        )
        db.session.add(product)
        db.session.commit()
        
        flash('Product created successfully', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/create_product.html', form=form)


@admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    """Edit product"""
    product = Product.query.get_or_404(product_id)
    form = AdminProductForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.slug = form.name.data.lower().replace(' ', '-')
        product.description = form.description.data
        product.price = form.price.data
        product.category_id = form.category.data
        product.stock = form.stock.data
        product.sku = form.sku.data
        product.rental_period_days = form.rental_period_days.data or 7
        
        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin.products'))
    elif request.method == 'GET':
        form.name.data = product.name
        form.description.data = product.description
        form.price.data = product.price
        form.category.data = product.category_id
        form.stock.data = product.stock
        form.sku.data = product.sku
        form.rental_period_days.data = product.rental_period_days
    
    return render_template('admin/edit_product.html', form=form, product=product)


@admin_bp.route('/products/<int:product_id>/delete')
@login_required
@admin_required
def delete_product(product_id):
    """Delete product"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('admin.products'))


@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    """Manage orders"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')
    
    query = Order.query
    if status:
        query = query.filter_by(status=OrderStatus[status.upper()])
    
    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=20)
    statuses = [s.name for s in OrderStatus]
    
    return render_template('admin/orders.html', orders=orders, statuses=statuses, selected_status=status)


@admin_bp.route('/orders/<int:order_id>')
@login_required
@admin_required
def order_detail(order_id):
    """View order details"""
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)


@admin_bp.route('/orders/<int:order_id>/update-status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    """Update order status"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    try:
        order.status = OrderStatus[new_status.upper()]
        db.session.commit()
        flash('Order status updated', 'success')
    except (KeyError, ValueError):
        flash('Invalid status', 'danger')
    
    return redirect(url_for('admin.order_detail', order_id=order_id))


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Manage users"""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return render_template('admin/users.html', users=users)


@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    """Manage categories"""
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)
