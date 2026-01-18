from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class PayoutRequestForm(FlaskForm):
    amount = DecimalField(
        "Amount (€)",
        validators=[DataRequired(), NumberRange(min=0, max=10000)],
        places=2,
        render_kw={"placeholder": "e.g. 120"},
    )
    method = SelectField(
        "Preferred contact channel",
        choices=[
            ("telegram", "Telegram"),
            ("whatsapp", "WhatsApp"),
            ("phone", "Phone call"),
        ],
        validators=[DataRequired()],
    )
    details = StringField(
        "Contact handle",
        validators=[DataRequired(), Length(max=255)],
        render_kw={"placeholder": "@nickname or +41 79 123 45 67"},
    )
    submit = SubmitField("Request payout")
