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
        message = Message(body=form.Message.data, recipient=form.Recipient.data)
        message.set_passkey(form.Password.data)

        db.session.add(message)
        db.session.commit()

        id = Message.query.count()
        link = "igreet.live/display/"+str(id)
        flash("Your message has been posted!")
        return render_template('submission.html', link=link)
    
    return render_template('index.html', form=form)

@bp.route('/display/<message_id>', methods={'GET','POST'})
def display_message(message_id):
    message = Message.query.get(int(message_id))
    message_body = message.body
    recipient = message.recipient
    form = PasskeyForm()

    if form.validate_on_submit():
        passkey = form.passkey.data
        validated = message.check_passkey(passkey)

        import sys
        print(passkey, file=sys.stderr)
        

        if validated:
            return render_template('message.html', validated=True, name=recipient, message_body=message_body)
        else:
            return render_template('message.html', form=form, validated=False, name=recipient)

    return render_template('message.html', form=form, validated=False, name=recipient)