from app import app, db
from flask import render_template, redirect, url_for, request, json
from .models import List, Item, User
from .forms import SignupForm


@app.route('/')
def index():
#    return render_template('index.html')
    return render_template('index.html')

@app.route('/signup', methods=["GET", "POST"])
def sign_up():
    form = SignupForm()
    if request.method == "GET":
        return render_template('signup.html', form = form)
    elif request.method == "POST":
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
        
    
@app.route('/lists', methods=["GET"])
def show_lists():
    # show all lists
    all_lists = List.query.all()
    return render_template('show_lists.html', lists = all_lists)


@app.route('/list/new', methods=["GET", "POST"])
def add_list():
# add a new list
    if request.method == "POST":
        list_name = request.form['list_name']
        new_list = List(name=list_name)
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('show_lists'))
    elif request.method == "GET":
        return render_template('add_list.html')


@app.route('/list/<int:id>/update', methods=["GET", "POST"])
def chosen_list(id):

    chosen_list = List.query.get(id)
    if request.method == "GET":
        return render_template('edit_delete_list.html', list=chosen_list)
    
    if request.method == "POST":
    # edit the list
    
        if 'list_name' in request.form:
            chosen_list.name = request.form['list_name']
            db.session.add(chosen_list)
            db.session.commit()
            return redirect(url_for('show_lists'))
            
@app.route('/list/<int:id>/delete', methods=["POST"])
def delete_list(id):
    chosen_list = List.query.get(id)
    db.session.delete(chosen_list)
    db.session.commit()
    return redirect(url_for('show_lists'))


@app.route('/list/<int:list_id>/items', methods=["GET"])
def show_items(list_id):
# show all items in the list
    chosen_list = List.query.get(list_id)
    items = item.query.filter_by(list_id=list_id).all()
    return render_template('show_items.html', list=chosen_list, items=items)


@app.route('/list/<int:list_id>/items/new', methods=["GET", "POST"])
def add_item(list_id):
    chosen_list = List.query.get(list_id)
    if request.method == "GET":
        return render_template('add_item.html', list=chosen_list )
        
    if request.method == "POST":
    # add a new item
        item_content = request.form['item_content']
        new_item = item(content=item_content, list_id=list_id)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('show_items',list_id=list_id))
        

@app.route('/list/<int:list_id>/items/<int:item_id>/update', methods=["GET", "POST"])
def chosen_item(list_id, item_id):

    chosen_list = List.query.get(list_id)
    chosen_item = Item.query.get(item_id)

    if request.method == "GET":
        return render_template('edit_delete_item.html', list=chosen_list, item=chosen_item)
        
    elif request.method == "POST":
    # edit the item content & status
        if 'item_content' in request.form:
            chosen_item.content = request.form['item_content']
            db.session.add(chosen_item)
            db.session.commit()
            return redirect(url_for('show_items', list_id=list_id))       
     
@app.route('/items/<int:item_id>/delete', methods=["POST"])
def delete_item(item_id):
    chosen_item = Item.query.get(item_id)
    list_id = chosen_item.list_id
    db.session.delete(chosen_item)
    db.session.commit()
    return redirect(url_for('show_items', list_id=list_id))