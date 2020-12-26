from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    team = db.Column(db.String(64))
    player = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Message(db.Model):
    body = db.Column(db.String(256))
    message_id = db.Column(db.Integer, primary_key=True)
    recipient_hash = db.Column(db.String(64))

    def simple_hash(name, restore=False):
        #Simple hash for masking recipient name in url string
        dir = 1 if restore else -1
        for i in range(len(name)):
            name[i] = chr(ord(name[i])+restore)
        return name

    def set_recipient_hash(self, recipient, restore=False):
        self.recipient_hash = simple_hash(recipient, restore)


