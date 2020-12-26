from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import ValidationError, DataRequired
from app.models import User

class KickoffForm(FlaskForm):
    choose_player1 = BooleanField('')
    choose_player2 = BooleanField('')
    submit = SubmitField('Choose!')

