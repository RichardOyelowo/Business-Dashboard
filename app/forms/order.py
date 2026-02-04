from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import Order


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