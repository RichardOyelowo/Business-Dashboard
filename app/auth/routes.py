from app.extensions import db
from .decorators import login_required
from itsdangerous import URLSafeTimedSerializer
from app.mail_utils import send_reset_email
from app.models import User, hash_password, validate_password
from app.forms import SignUp, Login, ForgotPassword, ResetPassword
from flask import Blueprint, render_template, redirect, request, session, url_for, flash, current_app


auth = Blueprint('auth', __name__)

@auth.route("/signup", methods=["GET","POST"])
def signup():
    form = SignUp()

    if form.validate_on_submit():
        user = User(
            name = (form.name.data or "").strip(),
            email = (form.email.data).lower(),
            password_hash = hash_password(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
       
        session["user_id"] = user.id
        return redirect(url_for("index.index"))

    return render_template("auth/signup.html", form=form)


@auth.route("/login", methods=["GET","POST"])
def login():
    form = Login()

    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.filter(User.email == email).first()

        if user and validate_password(user.password_hash, form.password.data):
            session["user_id"] = user.id
            return redirect(url_for("index.index"))
        
        flash('Invalid login info', 'info')

    return render_template("auth/login.html", form=form)


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()

    return redirect(url_for("auth.login"))


@auth.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPassword()

    if form.validate_on_submit():
        email = form.email.data.strip()

        if email is not None:
            user = User.query.filter(User.email == email.lower()).first()

            if user: # Send email only if user exists
                s = URLSafeTimedSerializer(current_app.secret_key)
                token = s.dumps(user.id, salt="password-reset-salt")
                reset_link = url_for("auth.reset_password", token=token, _external=True)

                try:
                    send_reset_email(user.email,reset_link)
                except Exception as e:
                    return render_template("auth/forgot_password.html", form_type="error",form=form, error="An Error Occured. Try Again Later.")

            return render_template("auth/forgot_password.html", form_type="sent_or_not_found")
    
    return render_template("auth/forgot_password.html", form_type="forgot", form=form)
    

@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    form = ResetPassword()

    s = URLSafeTimedSerializer(current_app.secret_key)
    try:
        id = s.loads(token, salt="password-reset-salt", max_age=3600)
    except (BadSignature, SignatureExpired):
        return render_template("auth/reset_password.html", token=token, form_type="error")

    if form.validate_on_submit():
        user = User.query.filter(User.id == id).first()

        if not user:
            return render_template("auth/reset_password.html", token=token, form_type="error")

        password = form.password.data.strip()
        user.password = hash_password(password)
        db.session.commit()
        
        return render_template("auth/reset_password.html", token=token, form_type="success")

    return render_template("auth/reset_password.html", token=token, form_type="reset", form=form)

