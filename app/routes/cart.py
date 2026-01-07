from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import CartItem, Product, Order, OrderItem, OrderStatus
from app.forms import CheckoutForm
import uuid
from datetime import datetime

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


@cart_bp.route('/')
def view():
    """View shopping cart"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(item.get_total() for item in cart_items)
    tax = subtotal * 0.1  # 10% tax
    shipping = 10.0 if subtotal > 0 else 0
    total = subtotal + tax + shipping
    
    return render_template('cart/view.html',
                          cart_items=cart_items,
                          subtotal=subtotal,
                          tax=tax,
                          shipping=shipping,
                          total=total)


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_item(product_id):
    """Add item to cart"""
    product = Product.query.get_or_404(product_id)
    
    if not product.is_active or product.stock <= 0:
        flash('Product is not available', 'danger')
        return redirect(url_for('products.detail', slug=product.slug))
    
    quantity = request.form.get('quantity', 1, type=int)
    
    if quantity <= 0 or quantity > product.stock:
        flash('Invalid quantity', 'danger')
        return redirect(url_for('products.detail', slug=product.slug))
    
    # Check if product already in cart
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{product.name} added to cart', 'success')
    return redirect(url_for('cart.view'))


@cart_bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update_item(item_id):
    """Update cart item quantity"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('cart.view'))
    
    quantity = request.form.get('quantity', 1, type=int)
    
    if quantity <= 0:
        return redirect(url_for('cart.remove_item', item_id=item_id))
    
    if quantity > cart_item.product.stock:
        flash('Insufficient stock', 'danger')
    else:
        cart_item.quantity = quantity
        db.session.commit()
        flash('Cart updated', 'success')
    
    return redirect(url_for('cart.view'))


@cart_bp.route('/remove/<int:item_id>')
@login_required
def remove_item(item_id):
    """Remove item from cart"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('cart.view'))
    
    product_name = cart_item.product.name
    db.session.delete(cart_item)
    db.session.commit()
    flash(f'{product_name} removed from cart', 'success')
    return redirect(url_for('cart.view'))


@cart_bp.route('/clear')
@login_required
def clear():
    """Clear entire cart"""
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Cart cleared', 'success')
    return redirect(url_for('cart.view'))


@cart_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart.view'))
    
    form = CheckoutForm()
    
    if form.validate_on_submit():
        # Calculate totals
        subtotal = sum(item.get_total() for item in cart_items)
        tax = subtotal * 0.1
        shipping = 10.0
        total = subtotal + tax + shipping
        
        # Create order
        order = Order(
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            customer_id=current_user.id,
            shipping_name=form.shipping_name.data,
            shipping_email=form.shipping_email.data,
            shipping_phone=form.shipping_phone.data,
            shipping_address=form.shipping_address.data,
            shipping_city=form.shipping_city.data,
            shipping_state=form.shipping_state.data,
            shipping_postal_code=form.shipping_postal_code.data,
            shipping_country=form.shipping_country.data,
            subtotal=subtotal,
            tax=tax,
            shipping_cost=shipping,
            total=total,
            payment_method='stripe'
        )
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            order.items.append(order_item)
            
            # Reduce product stock
            cart_item.product.stock -= cart_item.quantity
        
        db.session.add(order)
        db.session.commit()
        
        # Clear cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        
        flash('Order created! Proceeding to payment...', 'success')
        return redirect(url_for('orders.payment', order_id=order.id))
    
    # Pre-fill form with user data
    if request.method == 'GET':
        form.shipping_name.data = current_user.get_full_name()
        form.shipping_email.data = current_user.email
        form.shipping_phone.data = current_user.phone
        form.shipping_address.data = current_user.address
        form.shipping_city.data = current_user.city
        form.shipping_state.data = current_user.state
        form.shipping_postal_code.data = current_user.postal_code
        form.shipping_country.data = current_user.country
    
    subtotal = sum(item.get_total() for item in cart_items)
    tax = subtotal * 0.1
    shipping = 10.0
    total = subtotal + tax + shipping
    
    return render_template('cart/checkout.html',
                          form=form,
                          cart_items=cart_items,
                          subtotal=subtotal,
                          tax=tax,
                          shipping=shipping,
                          total=total)
