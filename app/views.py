from app import app, db
from flask import render_template, redirect, url_for, request, json, flash, session, g
from .models import List, Item, User
from .forms import SignupForm, SigninForm, UpdateItemForm


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

@app.route('/newlist', methods=["POST"])
def add_list():
    user = User.query.filter_by(email = session['email']).first()
    if user and 'newlist_name' in request.form:
        list_name = request.form['newlist_name']
        if list_name != '':
            new_list = List(name=list_name, user_id=user.id)
            db.session.add(new_list)
            db.session.commit()
            return json.dumps({'status':'OK','new_list_name':new_list.name})
        return 'Your input is empty!'
    return 'You are not authenticated', 403

    
@app.route('/renamelist/<int:id>', methods=["POST"])
def rename_list(id):
    chosen_list = List.query.get(id)
    if (chosen_list and is_authenticated(session, chosen_list)) and 'list_name' in request.form:
        chosen_list.name = request.form['list_name']
        if chosen_list.name != '':
            db.session.add(chosen_list)
            db.session.commit()
            return json.dumps({'status':'OK','edited_list_name':chosen_list.name})
        return 'Your input is empty!'
    return 'You are not authenticated', 403

         
@app.route('/deletelist/<int:id>', methods=["POST"])
def delete_list(id):
    chosen_list = List.query.get(id)
    if chosen_list and is_authenticated(session, chosen_list):
        db.session.delete(chosen_list)
        db.session.commit()
        return json.dumps({'status':'OK','deleted_list':chosen_list.name})
    return "You are not authenticated", 403


@app.route('/additem/<int:listid>', methods=["POST"])
def add_item(listid):
    the_list = List.query.get(listid)
    user = User.query.filter_by(email = session['email']).first()
    if (the_list and is_authenticated(session, the_list)) and 'item_content' in request.form:
        item_content = request.form['item_content']
        if item_content != '':
            new_item = Item(content=item_content, list_id=the_list.id, user_id=user.id)
            db.session.add(new_item)
            db.session.commit()
            return json.dumps({'status': 'OK', 'new_item_content': new_item.content})
        return "Your Input Is Empty!"
    return "You are not authenticated", 403


@app.route('/renameitem/<int:id>', methods=["POST"])
def rename_item(id):
    item = Item.query.get(id)
    if (item and is_authenticated(session,item)) and 'item_content' in request.form:
        item.content = request.form['item_content']
        if item.content != '':
            db.session.add(item)
            db.session.commit()
            return json.dumps({'status': 'OK', 'renamed_item': item.content})
        return 'Your Input Is Empty!'
    return "You are not authenticated", 403


@app.route('/changestatus/<int:id>', methods=["POST"])
def change_status(id):
    item = Item.query.get(id)
    status = request.form['status']
    if item and is_authenticated(session, item):
        if status == 'yes': 
            item.is_done = True
            db.session.add(item)
            db.session.commit()
            return json.dumps({'status': 'OK', 'item_content': item.content, 'is_completed': item.is_done})
        return redirect(url_for('profile'))
    return "You are not authenticated", 403
        
@app.route('/deleteitem/<int:id>', methods=["POST"])
def delete_item(id):
    item = Item.query.get(id)
    if item and is_authenticated(session, item):
        db.session.delete(item)
        db.session.commit()
        return json.dumps({'status': 'OK', 'deleted_item': item.content})
    return "You're not authenticated", 403

    
def is_authenticated(session, resource=None):

    if not 'email' in session:
        return False

    user = User.query.filter_by(email = session['email']).first()
    # if user:
    #     if not resource:
    #         return True
    #     else:
    #         if resource.user_id == user.id:
    #             return True
    return (user and ((not resource) or (resource.user_id == user.id)))

