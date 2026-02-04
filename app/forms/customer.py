from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from app.models import Customer


class BaseForm(FlaskForm):
    name = StringField('Name', render_kw={"placeholder": "John Doe"}, validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Length(max=20)])
    company = StringField('Company', validators=[Length(max=100)])


class CustomerCreate(BaseForm):
    submit = SubmitField('Save Customer')

    def validate_email(self, email):
        customer = Customer.query.filter_by(email=email.data).first()

        if customer:
            raise ValidationError("Email already registered to a user")


class CustomerEdit(BaseForm):
    submit = SubmitField('Update Customer')

    def __init__(self, customer=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = customer

    def validate_email(self, email):
        if not self.customer:
            return
        
        customer = Customer.query.filter(Customer.email == email.data, self.customer.id != Customer.id).first()

        if customer:
            raise ValidationError('Email is connected to another customer')