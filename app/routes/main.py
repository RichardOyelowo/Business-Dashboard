from flask import render_template, Blueprint, g
from app.models.customer import Customer
from app.models.order import Order
from app.auth import login_required
from app.extensions import db

index_bp = Blueprint("index",__name__)

@index_bp.route('/')
@login_required
def index():
    """Dashboard Page with Stats"""
    user = g.user

    customers =  Customer.query.filter_by(user_id=user.id).all()
    orders = Order.query.join(Customer).filter(Customer.user_id == user.id).all()

    total_customers = len(customers)
    total_orders = len(orders)
    pending_orders = sum(1 for order in orders if order.status == "pending")

    revenue = sum((order.price * order.quantity) for order in orders)

    return render_template("index.html", total_customers=total_customers, total_orders=total_orders, 
        pending_orders=pending_orders, total_revenue=revenue)
