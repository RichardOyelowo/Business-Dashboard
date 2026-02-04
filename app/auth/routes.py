from app.extensions import db
from app.forms import SignUp, Login
from .decorators import login_required
from app.models import User, hash_password, validate_password
from flask import Blueprint, render_template, redirect, session, url_for, flash


auth = Blueprint('auth', __name__)

@auth.route("/signup", methods=["GET","POST"])
def signup():
    form = SignUp()

    if form.validate_on_submit():
        user = User(
            name = form.name.data.lower(),
            email = form.email.data.lower(),
            password_hash = hash_password(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        
            
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", form=form)


@auth.route("/login", methods=["GET","POST"])
def login():
    form = Login()

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data.lower()).first()

        if user and validate_password(user.password_hash, form.password.data):
            session["user_id"] = user.id
            return redirect(url_for("customers.customers"))
        
        flash('Invalid login info', 'info')

    return render_template("auth/login.html", form=form)


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()

    return redirect(url_for("auth.login"))