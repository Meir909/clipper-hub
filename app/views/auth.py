from __future__ import annotations

import hmac
import hashlib
import os
from urllib.parse import parse_qs

from flask import Blueprint, flash, redirect, render_template, request, url_for, session, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from authlib.integrations.flask_client import OAuth

from app.extensions import db, oauth
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


# Google OAuth
@auth_bp.route("/login/google")
def google_login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route("/login/google/callback")
def google_callback():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            flash("Failed to get user info from Google", "danger")
            return redirect(url_for("auth.login"))
        
        # Получаем email и имя пользователя
        email = user_info.get('email')
        if not email:
            flash("Email is required from Google", "danger")
            return redirect(url_for("auth.login"))
        
        # Ищем пользователя по email
        user = User.query.filter_by(email=email.lower()).first()
        
        if not user:
            # Создаем нового пользователя
            given_name = user_info.get('given_name', '')
            family_name = user_info.get('family_name', '')
            display_name = f"{given_name} {family_name}".strip() or user_info.get('name', 'Google User')
            
            user = User(
                email=email.lower(),
                role=Role.CLIPPER,
                display_name=display_name,
                google_id=user_info.get('sub'),
                avatar_url=user_info.get('picture')
            )
            user.set_password(os.urandom(24).hex())  # Случайный пароль
            db.session.add(user)
            db.session.commit()
            flash(f"Welcome to Clipper platform, {display_name}!", "success")
        else:
            # Обновляем информацию о пользователе
            if not user.google_id:
                user.google_id = user_info.get('sub')
            if not user.avatar_url:
                user.avatar_url = user_info.get('picture')
            db.session.commit()
            flash("Welcome back!", "success")
        
        login_user(user)
        next_url = request.args.get("next") or url_for("dashboard.index")
        return redirect(next_url)
        
    except Exception as e:
        flash(f"Google login failed: {str(e)}", "danger")
        return redirect(url_for("auth.login"))
