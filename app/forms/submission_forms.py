from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length

from app.models import PlatformType


class SubmissionForm(FlaskForm):
    video_url = StringField(
        "Video link",
        validators=[
            DataRequired(),
            URL(require_tld=True, message="Provide a valid URL"),
            Length(max=255),
        ],
    )
    platform = SelectField(
        "Platform",
        choices=[(p.value, p.name.title()) for p in PlatformType],
        validators=[DataRequired()],
    )
    submit = SubmitField("Send for review")
