from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (DateField, IntegerField, SelectField, SelectMultipleField,
                      StringField, SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Length, Optional, URL, NumberRange

from app.models import PaymentType, ProjectAccess


class ProjectForm(FlaskForm):
    title = StringField("Project title", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField(
        "Description",
        validators=[DataRequired(), Length(max=1000)],
        render_kw={"rows": 4},
    )
    earning_conditions = TextAreaField(
        "Earning conditions",
        validators=[DataRequired(), Length(max=500)],
        render_kw={"rows": 3},
    )
    payment_type = SelectField(
        "Payment type",
        choices=[(p.value, p.name.replace("_", " ").title()) for p in PaymentType],
        validators=[DataRequired()],
    )
    rate_per_view_cents = IntegerField(
        "Rate per view (cents)",
        validators=[Optional(), NumberRange(min=0)],
    )
    fixed_reward_cents = IntegerField(
        "Fixed reward (cents)",
        validators=[Optional(), NumberRange(min=0)],
    )
    kpi_views = IntegerField("KPI views", validators=[Optional(), NumberRange(min=0)])
    instruction_url = StringField("Instruction link", validators=[Optional(), URL()])
    access_mode = SelectField(
        "Access mode",
        choices=[(mode.value, mode.name.title()) for mode in ProjectAccess],
        validators=[DataRequired()],
    )
    submission_limit_per_user = IntegerField(
        "Submission limit per clipper",
        validators=[Optional(), NumberRange(min=1, max=10)],
    )
    start_date = DateField("Starts", validators=[Optional()])
    end_date = DateField("Ends", validators=[Optional()])
    manager_id = SelectField("Project manager", coerce=int, validators=[Optional()])
    submit = SubmitField("Save project")
