from flask_app.models.models_user import User
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask import session



class Order:
    db = 'pizza_orders'
    def __init__(self, data):
        self.id = data['id']
        self.method = data['method']
        self.size = data['size']
        self.crust = data['crust']
        self.qty = data['qty']
        self.topping_1 = data['topping_1']
        self.topping_2 = data['topping_2']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_favorite = data['user_favorite']
        self.total_price = data['total_price']
        self.owner = None



    @classmethod
    def is_valid(cls, order):
        valid = True
        return valid

    #Create an Order
    @classmethod
    def create_order(cls, data):
        query = """
                INSERT INTO orders (method, size, crust, qty, topping_1, topping_2, user_favorite, total_price, user_id)
                VALUES (%(method)s, %(size)s, %(crust)s, %(qty)s, %(topping_1)s, %(topping_2)s, %(user_favorite)s, %(total_price)s, %(user_id)s);
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        # Update User with id of favorite order
        if data['user_favorite'] == 1:
            print("This is a user favorite")
            query2 = """
                    SELECT id FROM orders ORDER BY id DESC LIMIT 1;
                    """ 
            fav_id = connectToMySQL(cls.db).query_db(query2, data)
           
            print("Fav id = ", fav_id)
         
            fav_id_num = fav_id[0]['id']
            print( "Fav id num = ", fav_id_num)     
            u_id = session['user_id'];
            query3 = query = f"UPDATE users SET favorite_order = {fav_id_num} WHERE id = {u_id};"
            connectToMySQL(cls.db).query_db(query3, data)
        return results


    @classmethod
    def all_orders(cls):
        query = "SELECT * FROM orders"
        results = connectToMySQL(cls.db).query_db(query)
        orders = []
        for order in results:
            orders.append(cls(order))
        return orders

    @classmethod
    def get_one_order(cls, data):
        query = """
                SELECT * FROM orders
                JOIN users ON users.id = orders.user_id
                WHERE orders.id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        order = cls(results[0])
        owner_data = {
            'id' : results[0]['id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'address' : results[0]['address'],
            'city' : results[0]['city'],
            'state' : results[0]['state'],
            'password' : results[0]['password'],
            'favorite_order' : results[0]['favorite_order'],
            'created_at' : results[0]['created_at'],
            'updated_at' : results[0]['updated_at']
        }
        order.owner = User(owner_data)
        return order

    @classmethod
    def get_favorite_order(cls, data):
        query = """
                SELECT * FROM orders
                JOIN users ON users.id = orders.user_id
                WHERE orders.id = users.favorite_order AND orders.user_id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        order = cls(results[0])
        owner_data = {
            'id' : results[0]['id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'address' : results[0]['address'],
            'city' : results[0]['city'],
            'state' : results[0]['state'],
            'password' : results[0]['password'],
            'favorite_order' : results[0]['favorite_order'],
            'created_at' : results[0]['created_at'],
            'updated_at' : results[0]['updated_at']
        }
        order.owner = User(owner_data)
        return order

    @classmethod
    def all_orders_owner(cls):
        query = """
                SELECT * FROM orders
                LEFT JOIN users
                ON users.id = orders.user_id
                """
        results = connectToMySQL(cls.db).query_db(query)
        orders = []
        for order in results:
            order_owner = cls(order)
            owner_data = {
                'id' : results[0]['id'],
                'first_name' : results[0]['first_name'],
                'last_name' : results[0]['last_name'],
                'email' : results[0]['email'],
                'address' : results[0]['address'],
                'city' : results[0]['city'],
                'state' : results[0]['state'],
                'password' : results[0]['password'],
                'favorite_order' : results[0]['favorite_order'],
                'created_at' : results[0]['created_at'],
                'updated_at' : results[0]['updated_at']
            }
            order_owner.owner = User(owner_data)
            orders.append(order_owner)
        return orders

# Don't need, but might need later
    @classmethod
    def update_order(cls, form_data, order_id):
        query = f"UPDATE orders SET method = %(method)s, size = %(size)s, crust = %(crust)s, qty = %(qty)s, topping_1 = %(topping_1)s, topping_2 = %(topping_2)s, user_favorite = %(user_favorite)s, total_price = %(total_price)s WHERE id = {order_id};"
        return connectToMySQL(cls.db).query_db(query, form_data)

#Don't need, but might need later
    @classmethod
    def delete_order(cls, data):
        query = """
                DELETE FROM orders
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query, data)