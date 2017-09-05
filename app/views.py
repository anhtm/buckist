from app import app, db
from flask import render_template, redirect, url_for, request, json, flash, session, g
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
                session['email'] = newuser.email
                session['firstname'] = newuser.first_name
                session['id'] = newuser.id
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
        return render_template('profile.html', user=user, lists=user.lists)

@app.route('/newlist', methods=["GET", "POST"])
def add_list():

    user = User.query.filter_by(email = session['email']).first()
    if request.method == 'GET':
        return render_template('add_list.html', list=list)
    elif request.method == 'POST':
        list_name = request.form['list_name']
        new_list = List(name=list_name, user_id=user.id)
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('profile'))


@app.route('/updatelist/<int:id>', methods=["GET"])
def update_list(id):

    list = List.query.get(id)
    return render_template('update_list.html', list=list)
    
@app.route('/renamelist/<int:id>', methods=["POST"])
def rename_list(id):
    list = List.query.get(id)
    if 'list_name' in request.form:
        list.name = request.form['list_name']
        db.session.add(list)
        db.session.commit()
        return redirect(url_for('profile'))

         
@app.route('/deletelist/<int:id>', methods=["POST"])
def delete_list(id):
    list = List.query.get(id)
    db.session.delete(list)
    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/additem/<int:listid>', methods=["GET", "POST"])
def add_item(listid):
    list = List.query.get(listid)
    user = User.query.filter_by(email = session['email']).first()
    if request.method == 'GET':
        return render_template('add_item.html', list=list)
    elif request.method == 'POST':
        item_content = request.form['item_content']
        new_item = Item(content=item_content, list_id=list.id, user_id=user.id)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('profile'))

@app.route('/updateitem/<int:id>', methods=["GET"])
def update_item(id):
    item = Item.query.get(id)
    return render_template('update_item.html', item=item)

@app.route('/renameitem/<int:id>', methods=["POST"])
def rename_item(id):
    item = Item.query.get(id)
    if 'item_content' in request.form:
        item.content = request.form['item_content']
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('profile'))

@app.route('/deleteitem/<int:id>', methods=["POST"])
def delete_item(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/changestatus/<int:id>', methods=["POST"])
def change_status(id):
    item = Item.query.get(id)
    status = request.form['status']
    if status == 'yes': 
        item.is_done = True
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('profile'))
        