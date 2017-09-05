from app import app, db
from sqlalchemy import Integer, String, ForeignKey, Boolean
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    pwdhash = db.Column(db.String(54))
    lists = db.relationship('List', backref='user', lazy='dynamic')
    items = db.relationship('Item', backref='user', lazy='dynamic')
    
    def __init__(self,first_name,last_name, email, password):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email.lower()
        self.set_password(password)
        
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
        
    def __repr__(self):
        return '<User %r>' % (self.first_name)
    
    
class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    items = db.relationship('Item', backref='list', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<List %r>' % (self.name)
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(264), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))