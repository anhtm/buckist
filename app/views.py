from app import app, db
from flask import render_template, redirect, url_for, request, json, flash, session
from .models import List, Item, User
from .forms import SignupForm, SigninForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=["GET", "POST"])
def sign_up():
    form = SignupForm()
    if 'email' in session:
        return redirect(url_for('profile'))
    else:
        if request.method == "GET":
            return render_template('signup.html', form=form)
        elif request.method == "POST":
            if form.validate() == False:
                return render_template('signup.html', form=form)
            else:
                newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
                db.session.add(newuser)
                db.session.commit()
                flash('You have successfully signed up!')
                session['email'] = newuser.email
                session['firstname'] = newuser.first_name
                return redirect(url_for('profile')) 


@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    form = SigninForm()
    if 'email' in session:
        return redirect(url_for('profile'))
    else:
        if request.method == 'POST':
            if form.validate() == False:
                return render_template('signin.html', form=form)
            else:
                session['email'] = form.email.data
                return redirect(url_for('profile'))
                     
        elif request.method == 'GET':
            return render_template('signin.html', form=form)  


@app.route('/signout')
def sign_out():
 
    if 'email' not in session:
        return redirect(url_for('sign_in'))
     
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/profile', methods=["GET"])
def profile():
    if 'email' not in session:
        return redirect(url_for('sign_in'))
 
    user = User.query.filter_by(email = session['email']).first()
 
    if user is None:
        return redirect(url_for('sign_in'))
    else:
        return render_template('profile.html')

  
