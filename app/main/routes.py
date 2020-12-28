from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import MessageForm
from app.models import User, Message
from app.main import bp
import random
import os

@bp.route('/')
@bp.route('/index')
def index():
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(body=form.Message.data)
        message.set_recipient_hash(form.Recipient.data)
        db.session.add(message)
        db.session.commit()
        flash("Your message has been posted!")
        return render_template('index.html', form = form)
    
    return render_template('index.html', form = form)

@bp.route('/display/<message_id>/<recipient_hash>')
def display_message(message_id, recipient_hash):
    message = Message.query.get(int(message_id))
    message_body = message.body
    recipient = message.restore_recipient_name()

    return render_template('message.html')