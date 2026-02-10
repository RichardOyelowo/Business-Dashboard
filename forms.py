from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from models import Customer, Order


class CustomerForm(FlaskForm):
    name = StringField('Name', render_kw={"placeholder": "John Doe"}, validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Length(max=20)])
    company = StringField('Company', validators=[Length(max=100)])
    submit = SubmitField('Save Customer')

    def __init__(self, customer_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer_id = customer_id

    def validate_email(self, email):
        customer = Customer.query.filter(Customer.email == email.data, Customer.id != self.customer_id).first()
        if customer:
            raise ValidationError('Email already registered. Please use a different email.')


class OrderForm(FlaskForm):
    order_number = StringField('Order ID', validators=[DataRequired(), Length(min=2, max=100)])
    customer_id = SelectField('Customer ID', coerce=int, validators=[DataRequired()])
    product = StringField('Product', validators=[DataRequired(), Length(max=200)])
    quantity = IntegerField('Quantity', validators=[DataRequired()], default=1)
    price = FloatField('Price', validators=[DataRequired()])
    status = SelectField('Status', validators=[DataRequired()], choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    submit = SubmitField('Save Order')

    def __init__(self, order_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_id = order_id

    def validate_order_number(self, order_number):
        order = Order.query.filter(Order.order_number == order_number.data, Order.id != self.order_id).first()
        if order:
            raise ValidationError('Order number already registered. Please use a different order.')