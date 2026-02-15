from app.extensions import db
from app.models.order import Order
from app.models.customer import Customer
from app.auth import login_required
from app.forms.customer import CustomerCreate, CustomerEdit
from flask import Blueprint, render_template, redirect, request, flash, url_for, g


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("/")
@login_required
def customers():
    page = request.args.get("page",1,type=int)
    user = g.user

    pagination = Customer.query.filter_by(user_id=user.id).order_by(
        Customer.created_at.desc()
    ).paginate(page=page, per_page=10, error_out=False)

    return render_template("customers.html", customers=pagination.items, pagination=pagination)


@customers_bp.route("/new", methods=["GET", "POST"])
@login_required
def customer_new():
    form = CustomerCreate()
    user = g.user

    if form.validate_on_submit():
        customer = Customer(
            name = form.name.data,
            user_id = user.id,
            email = form.email.data,
            phone = form.phone.data,
            company = form.company.data
        )

        db.session.add(customer)
        db.session.commit()

        flash('Customer Added successfully!', 'success')
        return redirect(url_for("index.index"))

    return render_template("customer_form.html", form=form, edit_form=False)


@customers_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def customer_edit(id):
    user = g.user
    customer = Customer.query.filter(Customer.id == id, Customer.user_id == user.id).first_or_404(id)
    
    form = CustomerEdit(obj=customer, customer=customer)
    
    if form.validate_on_submit():
        form.populate_obj(customer)
        db.session.commit()

        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customers.customers'))

    return render_template("customer_form.html", form=form, edit_form=True, customer_id=id)


@customers_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def customer_delete(id):
    user = g.user
    customer = Customer.query.filter_by(user_id=user.id).first_or_404(id)

    if Order.query.filter_by(customer_id=customer.id).first():
        flash("Cannot delete customer with existing orders.", "danger")

        return redirect(url_for("customers.customers"))

    db.session.delete(customer)
    db.session.commit()

    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('customers'))
