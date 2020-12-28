from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import ValidationError, DataRequired
from app.models import User

class MessageForm(FlaskForm):
    Message = TextAreaField('Message', render_kw={"rows": 11, "cols": 60})
    Recipient = StringField('Recepient')
    submit = SubmitField('Send')

