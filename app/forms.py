from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, TextField, SubmitField, validators, ValidationError, PasswordField, RadioField
from wtforms.validators import DataRequired, Length
from app.models import User
from app import db

class SignupForm(Form):
    firstname = TextField("First name", [validators.Required("Please enter your first name.")])
    lastname = TextField("Last name", [validators.Required("Please enter your last name.")])
    email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password."), validators.Length(min=8, max=25)])
    submit = SubmitField("Create account")
 
    def validate(self):
        if not Form.validate(self):
            return False
     
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class SigninForm(Form):
    email = TextField("Email", [validators.Required("Please enter your email address.")])
    password = PasswordField("Password", [validators.Required("Please enter your password.")])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        
    def validate(self):
        if not Form.validate(self):
            return False
    
        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False

class UpdateItemForm(Form):
    change_content = TextField("Change Content")
    change_status = RadioField("Completed?", choices=[('no','No'),('yes','Yes')], default='no')
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        
    def validate(self):
        if not Form.validate(self):
            return False