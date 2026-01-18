from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.forms.auth_forms import ClipperRegisterForm, LoginForm
from app.models import Role, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def redirect_authenticated_user():
    next_url = request.args.get("next") or url_for("dashboard.index")
    return redirect(next_url)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect_authenticated_user()

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Welcome back!", "success")
            next_url = request.args.get("next") or url_for("dashboard.index")
            return redirect(next_url)
        flash("Invalid credentials", "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect_authenticated_user()

    form = ClipperRegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("Email already registered", "warning")
            return render_template("auth/register.html", form=form)
        user = User(
            email=form.email.data.lower(),
            role=Role.CLIPPER,
            display_name=form.display_name.data.strip(),
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Welcome to Clipper platform!", "success")
        return redirect(url_for("dashboard.index"))
    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Signed out", "info")
    return redirect(url_for("auth.login"))
