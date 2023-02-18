from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.models.models_user import User
from flask_app.models.models_order import Order
from flask_app.config.mysqlconnection import connectToMySQL
import random

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user_data = {
        'id': session['user_id']
    }
    all = Order.all_orders()
    all_orders_owner = Order.all_orders_owner()
    # orders_with_owners = Order.get_orders_with_owners()
    return render_template("dashboard.html")

@app.route('/craft_pizza')
def craft_pizza():
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    return render_template('craft_pizza.html', user=user)


@app.route('/create_session_pizza', methods=['POST'])
def create_session_pizza():
    user_data = {
        'id': session['user_id']
    }
    print('At beginning of create session pizza')
    session['order_status'] = 'started'
    session['method'] = request.form['method']
    session['size'] = request.form['size']
    session['crust'] = request.form['crust']
    session['qty'] = int(request.form['qty'])
    session['topping_1'] = request.form['topping_1']
    session['topping_2'] = request.form['topping_2']

    if(session['size']=='personal'):
        session['individual_price'] = 9.99;
    elif(session['size']=='medium'):
        session['individual_price'] = 11.99; 
    elif(session['size']=='large'):
        session['individual_price'] = 13.99;
    session['total_price'] = int(session['qty']) * session['individual_price'] 
    user = User.get_user_by_id(user_data)
    print('Created a Session Pizza')
    print(session['method'], session['qty'], session['total_price'])

    # user = User.get_user_by_id(user_data)
    return redirect('/go_to_place_order')

@app.route('/create_favorite_session_pizza')
def create_favorite_session_pizza():
    user_data = {
        'id': session['user_id']
    }
    print('At beginning of create favorite session pizza')
    fav_order = Order.get_favorite_order(user_data)
    print(fav_order)
    print('Fav Information ', fav_order.method, fav_order.size, fav_order.crust, fav_order.qty, fav_order.topping_1, fav_order.topping_2)
    session['order_status'] = 'started'
    session['method'] = fav_order.method
    session['size'] = fav_order.size
    session['crust'] = fav_order.crust
    session['qty'] = fav_order.qty
    session['topping_1'] = fav_order.topping_1
    session['topping_2'] = fav_order.topping_2

    if(session['size']=='personal'):
        session['individual_price'] = 9.99;
    elif(session['size']=='medium'):
        session['individual_price'] = 11.99; 
    elif(session['size']=='large'):
        session['individual_price'] = 13.99;
    session['total_price'] = int(session['qty']) * session['individual_price'] 
    print('Created Your Favorite Session Pizza')
    print(session['method'], session['qty'], session['total_price'])

    # user = User.get_user_by_id(user_data)
    return redirect('/go_to_place_order')

@app.route('/create_random_session_pizza')
def create_random_session_pizza():

    print('At beginning of create random session pizza')
    session['order_status'] = 'started'
    session['method'] = 'takeout'

    temp_int = random.randint(1,3)
    print('random int = ', temp_int)
    if temp_int == 1:
        session['size'] = 'personal'
    if temp_int == 2:
        session['size'] = 'medium'
    if temp_int == 3:
        session['size'] = 'large'

    temp_int = random.randint(1,3)
    print('random int = ', temp_int)
    if temp_int == 1:
        session['crust'] = 'thin'
    if temp_int == 2:
        session['crust'] = 'regular'
    if temp_int == 3:
        session['crust'] = 'stuffed'

    #Don't want the user to get 9 pizzas randomly
    session['qty'] = 1

    temp_int = random.randint(1,10)
    print('random int = ', temp_int)
    if temp_int == 1:
        session['topping_1'] = 'pepperoni'
    if temp_int == 2:
        session['topping_1'] = 'mushrooms'
    if temp_int == 3:
        session['topping_1'] = 'extra cheese'
    if temp_int == 4:
        session['topping_1'] = 'sausage'
    if temp_int == 5:
        session['topping_1'] = 'onions'
    if temp_int == 6:
        session['topping_1'] = 'black olives'
    if temp_int == 7:
        session['topping_1'] = 'green pepper'
    if temp_int == 8:
        session['topping_1'] = 'garlic'
    if temp_int == 9:
        session['topping_1'] = 'tomato'
    if temp_int == 10:
        session['topping_1'] = 'basil'

    temp_int = random.randint(1,10)
    print('random int = ', temp_int)
    if temp_int == 1:
        session['topping_2'] = 'pepperoni'
    if temp_int == 2:
        session['topping_2'] = 'mushrooms'
    if temp_int == 3:
        session['topping_2'] = 'extra cheese'
    if temp_int == 4:
        session['topping_2'] = 'sausage'
    if temp_int == 5:
        session['topping_2'] = 'onions'
    if temp_int == 6:
        session['topping_2'] = 'black olives'
    if temp_int == 7:
        session['topping_2'] = 'green pepper'
    if temp_int == 8:
        session['topping_2'] = 'garlic'
    if temp_int == 9:
        session['topping_2'] = 'tomato'
    if temp_int == 10:
        session['topping_2'] = 'basil'

    if(session['size']=='personal'):
        session['individual_price'] = 9.99;
    elif(session['size']=='medium'):
        session['individual_price'] = 11.99; 
    elif(session['size']=='large'):
        session['individual_price'] = 13.99;
    session['total_price'] = int(session['qty']) * session['individual_price'] 

    print('Created a Random Session Pizza')
    print(session['method'], session['qty'], session['total_price'])

    # user = User.get_user_by_id(user_data)
    return redirect('/go_to_place_order')

@app.route('/edit_user')
def edit_user():
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    all = Order.all_orders()
    return render_template('edit_account.html', user=user, all=all)

@app.route('/go_to_place_order')
def go_to_place_order():
    return render_template('place_order.html')

@app.route('/finalize_order')
def finalize_order():
    data = {
        'method' : session['method'],
        'size' : session['size'],
        'crust' : session['crust'],
        'qty' : session['qty'],
        'topping_1' : session['topping_1'],
        'topping_2' : session['topping_2'],
        'user_id' : session['user_id'],
        'total_price' : session['total_price'],
        'user_favorite' : 0 
    }
    if not Order.is_valid(data):
        return redirect("/craft_pizza")
    Order.create_order(data)
    session['order_status'] = 'clear'
    session['qty'] = 0
    return render_template('success.html')

@app.route('/finalize_and_favorite_order')
def finalize_and_favorite_order():
    data = {
        'method' : session['method'],
        'size' : session['size'],
        'crust' : session['crust'],
        'qty' : session['qty'],
        'topping_1' : session['topping_1'],
        'topping_2' : session['topping_2'],
        'user_id' : session['user_id'],
        'total_price' : session['total_price'],
        'user_favorite' : 1 
    }
    if not Order.is_valid(data):
        return redirect("/craft_pizza")
    Order.create_order(data)
    session['order_status'] = 'clear'
    session['qty'] = 0
    return render_template('success.html')


@app.route('/show/<int:order_id>')
def show_order(order_id):
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    order_data = {
        'id' : order_id
    }
    order = Order.get_one_order(order_data)
    user = User.get_user_by_id(user_data)
    return render_template('one_order.html', order = order, user = user)

@app.route('/user/order')
def show_my_order():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    all = Order.all_orders()
    return render_template("myorders.html", user = User.get_user_by_id(data), all=all)

@app.route('/start_over')
def start_over():
    temp_id = session['user_id']
    session.clear()
    session['user_id'] = temp_id
    session['qty'] = 0
    session['order_status'] = 'clear'
    return redirect('/dashboard')

#Don't need now, might need later

@app.route('/edit/<int:order_id>')
def edit_order(order_id):
    order_data = {
        'id' : order_id
    }
    user_data = {
        'id': session['user_id']
    }
    order = Order.get_one_order(order_data)
    user = User.get_user_by_id(user_data)
    return render_template('edit_order.html', order = order, user=user)

#Don't need now, might need later

@app.route('/delete/<int:order_id>')
def delete(order_id):
    data = {
        'id' : order_id
    }
    Order.delete_order(data)
    return redirect('/dashboard')