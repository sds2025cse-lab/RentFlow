from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Order, OrderItem, OrderStatus
import stripe

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/')
@login_required
def my_orders():
    """View user's orders"""
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(customer_id=current_user.id)\
        .order_by(Order.created_at.desc())\
        .paginate(page=page, per_page=10)
    
    return render_template('orders/list.html', orders=orders)


@orders_bp.route('/<int:order_id>')
@login_required
def detail(order_id):
    """View order details"""
    order = Order.query.get_or_404(order_id)
    
    if order.customer_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('orders.my_orders'))
    
    return render_template('orders/detail.html', order=order)


@orders_bp.route('/<int:order_id>/payment', methods=['GET', 'POST'])
@login_required
def payment(order_id):
    """Payment page (Stripe integration)"""
    order = Order.query.get_or_404(order_id)
    
    if order.customer_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('orders.my_orders'))
    
    if order.status != OrderStatus.PENDING:
        flash('This order cannot be paid', 'warning')
        return redirect(url_for('orders.detail', order_id=order_id))
    
    if request.method == 'POST':
        try:
            # Initialize Stripe
            stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(order.total * 100),  # Stripe uses cents
                currency='usd',
                metadata={'order_id': order.id}
            )
            
            order.stripe_payment_intent = intent.id
            order.status = OrderStatus.PROCESSING
            db.session.commit()
            
            return render_template('orders/payment.html',
                                  order=order,
                                  client_secret=intent.client_secret,
                                  stripe_public_key=current_app.config['STRIPE_PUBLIC_KEY'])
        
        except Exception as e:
            flash(f'Payment error: {str(e)}', 'danger')
            return redirect(url_for('orders.detail', order_id=order_id))
    
    return render_template('orders/payment.html', order=order)


@orders_bp.route('/<int:order_id>/payment-success')
@login_required
def payment_success(order_id):
    """Payment success"""
    order = Order.query.get_or_404(order_id)
    
    if order.customer_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('orders.my_orders'))
    
    order.status = OrderStatus.SHIPPED
    db.session.commit()
    
    flash('Payment successful! Your order is being prepared.', 'success')
    return render_template('orders/success.html', order=order)


@orders_bp.route('/<int:order_id>/payment-failed')
@login_required
def payment_failed(order_id):
    """Payment failed"""
    order = Order.query.get_or_404(order_id)
    
    if order.customer_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('orders.my_orders'))
    
    flash('Payment failed. Please try again.', 'danger')
    return redirect(url_for('orders.payment', order_id=order_id))


@orders_bp.route('/<int:order_id>/cancel')
@login_required
def cancel(order_id):
    """Cancel order"""
    order = Order.query.get_or_404(order_id)
    
    if order.customer_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('orders.my_orders'))
    
    if order.status not in [OrderStatus.PENDING, OrderStatus.PROCESSING]:
        flash('Cannot cancel this order', 'warning')
        return redirect(url_for('orders.detail', order_id=order_id))
    
    order.status = OrderStatus.CANCELLED
    
    # Restore product stock
    for item in order.items:
        item.product.stock += item.quantity
    
    db.session.commit()
    flash('Order cancelled successfully', 'success')
    return redirect(url_for('orders.detail', order_id=order_id))
