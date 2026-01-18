from __future__ import annotations

from functools import wraps
from typing import Iterable

from flask import abort
from flask_login import current_user

from app.models import Role


def role_required(*allowed_roles: Role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            roles: Iterable[Role] = allowed_roles or (current_user.role,)
            if current_user.role not in roles:
                abort(403)
            return func(*args, **kwargs)

        return wrapper

    return decorator
