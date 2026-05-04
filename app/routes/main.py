from collections import Counter, defaultdict
from flask import render_template, Blueprint, g
from app.models.customer import Customer
from app.models.order import Order
from app.auth import login_required

index_bp = Blueprint("index",__name__)

@index_bp.route('/')
def index():
    """Public marketing page."""
    return render_template("home.html")


@index_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page with business stats and charts."""
    user = g.user

    customers = Customer.query.filter_by(user_id=user.id).order_by(Customer.created_at.asc()).all()
    orders = (
        Order.query.join(Customer)
        .filter(Customer.user_id == user.id)
        .order_by(Order.created.asc())
        .all()
    )

    total_customers = len(customers)
    total_orders = len(orders)
    pending_orders = sum(1 for order in orders if order.status == "pending")

    revenue = sum((order.price * order.quantity) for order in orders)
    completed_orders = sum(1 for order in orders if order.status == "completed")
    average_order_value = revenue / total_orders if total_orders else 0

    revenue_by_day = defaultdict(float)
    customer_growth = Counter()
    status_counts = Counter()
    customer_totals = defaultdict(float)

    for order in orders:
        created_day = order.created.strftime("%b %d")
        revenue_by_day[created_day] += order.total_amount
        status_counts[order.status or "pending"] += 1
        customer_totals[order.customer.name] += order.total_amount

    for customer in customers:
        created_day = customer.created_at.strftime("%b %d")
        customer_growth[created_day] += 1

    recent_orders = sorted(orders, key=lambda order: order.created, reverse=True)[:5]
    top_customers = sorted(
        customer_totals.items(), key=lambda item: item[1], reverse=True
    )[:5]

    chart_data = {
        "revenue": {
            "labels": list(revenue_by_day.keys()),
            "values": [round(value, 2) for value in revenue_by_day.values()],
        },
        "statuses": {
            "labels": [status.title() for status in status_counts.keys()],
            "values": list(status_counts.values()),
        },
        "customers": {
            "labels": list(customer_growth.keys()),
            "values": list(customer_growth.values()),
        },
    }

    return render_template(
        "dashboard.html",
        total_customers=total_customers,
        total_orders=total_orders,
        pending_orders=pending_orders,
        completed_orders=completed_orders,
        total_revenue=revenue,
        average_order_value=average_order_value,
        chart_data=chart_data,
        recent_orders=recent_orders,
        top_customers=top_customers,
    )
