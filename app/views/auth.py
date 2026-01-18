from __future__ import annotations

import hmac
import hashlib
from urllib.parse import parse_qs

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


@auth_bp.route("/tg")
def tg_auth():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return render_template("auth/tg_auth.html")


@auth_bp.route("/tg-login", methods=["POST"])
def tg_login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    init_data = request.form.get("initData", "")
    if not init_data:
        flash("Telegram data missing", "danger")
        return redirect(url_for("auth.login"))

    # Simple validation (replace with proper HMAC check in production)
    parsed = parse_qs(init_data)
    user_data = parsed.get("user", [None])[0]
    if not user_data:
        flash("Invalid user data", "danger")
        return redirect(url_for("auth.login"))

    try:
        from urllib.parse import unquote_plus
        import json
        user = json.loads(unquote_plus(user_data))
        tg_id = str(user.get("id"))
        first_name = user.get("first_name", "")
        last_name = user.get("last_name", "")
        username = user.get("username", "")
    except Exception:
        flash("Failed to parse Telegram user", "danger")
        return redirect(url_for("auth.login"))

    # Find or create user by Telegram ID
    user = User.query.filter_by(telegram_id=tg_id).first()
    if not user:
        # Auto-create user as clipper
        display_name = f"{first_name} {last_name}".strip() or username or f"User{tg_id}"
        user = User(
            telegram_id=tg_id,
            email=f"tg{tg_id}@clipper.local",  # placeholder
            role=Role.CLIPPER,
            display_name=display_name,
        )
        user.set_password(str(tg_id))  # placeholder password
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome, {display_name}!", "success")
    else:
        flash("Welcome back!", "success")

    login_user(user)
    return redirect(url_for("dashboard.index"))
