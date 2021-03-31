from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import MessageForm, PasskeyForm
from app.models import User, Message
from app.main import bp
from sqlalchemy import func

@bp.route('/', methods={'GET','POST'})
@bp.route('/index', methods={'GET','POST'})
def index():
    form = MessageForm()
    if form.validate_on_submit():
        import string
        import random
        url_mask = random.choice(string.ascii_letters)+random.choice(string.ascii_letters)
        message = Message(body=form.Message.data, recipient=form.Recipient.data, url_mask = url_mask)
        message.set_passkey(form.Password.data)

        db.session.add(message)
        db.session.commit()

        id = db.session.query(func.max(Message.id)).scalar()

        link = "igreet.live/display/"+str(id)+"/"+url_mask
        flash("Your message has been posted!")
        return render_template('submission.html', link=link)
    
    return render_template('index.html', form=form)

@bp.route('/display/<message_id>', methods={'GET','POST'}, defaults={'url_mask':None})
@bp.route('/display/<message_id>/<url_mask>', methods={'GET','POST'})
def display_message(message_id,url_mask):
    #Split url argument to take relevant parts

    message = Message.query.get(int(message_id))

    #Add account for invalid IDs
    if message is None:
        return render_template('404.html', link=None)
    else:
        message_body = message.body
        message_url_mask = message.url_mask
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


    if url_mask == message_url_mask:
        return render_template('message.html', form=form, validated=False, name=recipient)
    else:
        return render_template('404.html', link=None)
