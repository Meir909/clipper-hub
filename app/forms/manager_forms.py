from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

from app.models import SubmissionStatus


class SubmissionReviewForm(FlaskForm):
    views = IntegerField(
        "Views",
        validators=[DataRequired(), NumberRange(min=0)],
    )
    status = SelectField(
        "Decision",
        choices=[
            (SubmissionStatus.APPROVED.value, "Approve"),
            (SubmissionStatus.REJECTED.value, "Reject"),
        ],
        validators=[DataRequired()],
    )
    reject_reason = StringField(
        "Reason",
        validators=[Optional()],
        render_kw={"placeholder": "E.g. brand guideline mismatch"},
    )
    submit = SubmitField("Update submission")
