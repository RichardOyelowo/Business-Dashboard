from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Order, Customer


class BaseForm(FlaskForm):
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

    def __init__(self, user_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id
    
        if user_id:
            self.customer_id.choices = [(c.id,c.name) for c in Customer.query.filter(Customer.user_id == self.user_id).all()]
        else:
            self.customer_id.choices = []


class OrderCreate(BaseForm):    
    submit = SubmitField('Save Order')

    def validate_order_number(self, order_number):
        order = Order.query.join(Customer).filter(
            Order.order_number == order_number.data,
            Customer.user_id == self.user_id
        ).first()

        if order:
            raise ValidationError('Order number already registered. Please use a different order number.')


class OrderEdit(BaseForm):
    submit = SubmitField("Update Order")

    def __init__(self, order_id=None, user_id=None, *args, **kwargs):
        self.order_id = order_id
        super().__init__(user_id=user_id, *args, **kwargs)

    def validate_order_number(self, order_number):
        order = Order.query.join(Customer).filter(
            Order.order_number == order_number.data,
            Order.id != self.order_id,
            Customer.user_id == self.user_id
        ).first()

        if order:
            raise ValidationError('Order number already registered. Please use a different order.')