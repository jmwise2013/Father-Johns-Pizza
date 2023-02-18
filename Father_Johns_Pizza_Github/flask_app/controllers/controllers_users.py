from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.models_user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/go_to_login')
def go_to_login():
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():

    if not User.validate_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    #print(pw_hash)
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "address" : request.form['address'],
        "city" : request.form['city'],
        "state" : request.form['state'],
        "password" : pw_hash
    }
    id = User.create_user(data)

    session['user_id'] = id
    session['qty'] = 0
    session['order_status'] = 'clear'

    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    user = User.get_user_by_email(request.form)
    if not user:
        flash("Invalid Email", "login")
        return redirect('/go_to_login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/go_to_login')
    session['user_id'] = user.id
    session['qty'] = 0
    session['order_status'] = 'clear'
    return redirect('/dashboard')


@app.route('/update_user/<int:user_id>', methods =['POST'])
def update_user(user_id):
    user = request.form

    if not User.is_valid(user):
        return redirect(f"/edit_user")
    User.update_user(request.form, user_id)
    return redirect('/edit_user')

@app.route('/finalize_order_page')
def finalize_order_page():
    user_data = {
        'id': session['user_id']
    } 
    user = User.get_user_by_id(user_data)
    return render_template('place_order.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/go_to_login')