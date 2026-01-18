from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

from app.models import Role


ROLE_CHOICES = [(role.value, role.name.title()) for role in Role]


class CreateUserForm(FlaskForm):
    display_name = StringField(
        "Display name",
        validators=[Length(max=120)],
        render_kw={"placeholder": "Optional public name"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
    )
    role = SelectField(
        "Role",
        choices=ROLE_CHOICES,
        validators=[DataRequired()],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8)],
    )
    submit = SubmitField("Create user")


class UserRoleForm(FlaskForm):
    role = SelectField("Role", choices=ROLE_CHOICES, validators=[DataRequired()])
    submit = SubmitField("Update role")


class PayoutDecisionForm(FlaskForm):
    note = TextAreaField(
        "Note",
        validators=[Length(max=255)],
        render_kw={"rows": 2, "placeholder": "Optional note"},
    )
    submit = SubmitField("Confirm")
