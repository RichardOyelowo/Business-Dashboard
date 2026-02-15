from os import wait
from flask import Blueprint, render_template, redirect, request, flash, url_for, g
from app.auth import login_required
from app.models.customer import Customer
from app.forms.order import OrderForm
from app.models.order import Order
from app.extensions import db


orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

@orders_bp.route("/")
@login_required
def orders():
    page = request.args.get("page",1,type=int)
    user = g.user

    pagination = (Order.query.join(Customer).filter(Customer.user_id == user.id)
                  .order_by(Order.created.desc()).paginate(page=page, per_page=10, error_out=False))

    return render_template("orders.html", orders=pagination.items, pagination=pagination)


@orders_bp.route("/new", methods=["GET", "POST"])
@login_required
def order_new():
    form = OrderForm()
    # for order's form customer dropdown
    user = g.user
    form.customer_id.choices = [(c.id, c.name) for c in Customer.query.filter(Customer.user_id == user.id).all()]

    if len(form.customer_id.choices) == 0:
        flash("Please Add customers before orders", "info")
        
    if form.validate_on_submit():
        order = Order(
            order_number = form.order_number.data,
            customer_id = form.customer_id.data,
            product = form.product.data,
            quantity = form.quantity.data,
            price = form.price.data,
            status = form.status.data
        )

        db.session.add(order)
        db.session.commit()

        flash('Order added successfully!', 'success')
        return redirect(url_for("index.index"))

    return render_template("order_form.html", form=form, edit_form=False)


@orders_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def order_edit(id):
    user = g.user
    form = OrderForm()

    if request.method == "post":
        order = Order.query.join(Customer).filter(Customer.user_id == user.id, Order.id == id).first_or_404()

        form = OrderForm(order_id=order.id,obj=order)

        # SelectField options
        form.customer_id.choices = [(c.id, c.name) for c in Customer.query.filter(Customer.user_id == user.id).all()]
        form.populate_obj(order)
        
        if form.validate_on_submit():
            db.session.commit()

            flash('Order updated successfully!', 'success')
            return redirect(url_for('orders.orders'))

    return render_template("order_form.html", form=form, edit_form=True, order_id=id)


@orders_bp.route("/<int:id>/delete", methods=["GET","POST"])
@login_required
def order_delete(id):
    user = g.user
    if request.method == "post":
        order = Order.query.join(Customer).filter(Customer.user_id == user.id, Order.id == id).first_or_404()

        db.session.delete(order)
        db.session.commit()

        flash('Order deleted successfully!', 'success')

    return redirect(url_for('orders.orders'))
