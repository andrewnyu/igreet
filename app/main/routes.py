from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import MessageForm, PasskeyForm
from app.models import User, Message
from app.main import bp

@bp.route('/', methods={'GET','POST'})
@bp.route('/index', methods={'GET','POST'})
def index():
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(body=form.Message.data)
        #message.set_recipient_hash(form.Recipient.data)
        db.session.add(message)
        db.session.commit()
        link = "iGreet.com/"+str(10)
        flash("Your message has been posted!")
        return render_template('submission.html', link=link)
    
    return render_template('index.html', form=form)

@bp.route('/display/<message_id>', methods={'GET','POST'})
def display_message(message_id):
    #message = Message.query.get(int(message_id))
    #message_body = message.body
    #recipient = message.restore_recipient_name()
    form = PasskeyForm()

    if form.validate_on_submit():
        passkey = form.passkey.data
        #validated = message.check_passkey(passkey)
        validated = True

        if validated:
            return render_template('message.html', validated=True, name='Linte', message_body='placeholder')
        else:
            return render_template('message.html', form=form, validated=False, name='Linte')

    return render_template('message.html', form=form, validated=False, name='Linte')