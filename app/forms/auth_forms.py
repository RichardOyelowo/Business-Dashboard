from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError, EqualTo
from wtforms import StringField, IntegerField, PasswordField, SubmitField, validators
from flask_wtf import FlaskForm
from app.models import User


class SignUp(FlaskForm):
    name = StringField('Name',render_kw={'placeholder': 'John Doe'} ,validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20), 
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).*$', 
            message='Password must contain at least 1 letter, 1 number and 1 symbol')])
    submit = SubmitField('SignUp')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError("Email already registered to a user")


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Login')


class ForgotPassword(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Send Email')


class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20), 
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).*$', 
            message='Password must contain at least 1 letter, 1 number and 1 symbol')])
    confirmation = PasswordField('Retype Password', validators=[DataRequired(), EqualTo("password", message="Password doesn't match.")])