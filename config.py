import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clipper-mvp-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{(BASE_DIR / 'clipper.db').as_posix()}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = None
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 7
    ADMIN_EMAIL_ALLOWLIST = {
        email.strip().lower()
        for email in os.environ.get("ADMIN_EMAILS", "admin@clipper.io").split(",")
        if email.strip()
    }
