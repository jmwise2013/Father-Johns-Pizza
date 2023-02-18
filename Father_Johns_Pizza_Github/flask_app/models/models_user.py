from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db = "pizza_orders"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_order = data['favorite_order']

    @classmethod
    def create_user(cls,data):
        query = """
                INSERT INTO users (first_name, last_name, email, address, city, state, password)
                VALUES(%(first_name)s,%(last_name)s,%(email)s, %(address)s, %(city)s, %(state)s, %(password)s)
                """
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all_users(cls):
        query = """
                SELECT * FROM users;
                """
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_user_by_email(cls, data):
        query = """
                SELECT * FROM users WHERE email = %(email)s;
                """
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls,data):
        query = """
                SELECT * FROM users WHERE ID = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])


    @staticmethod
    def validate_registration(user):
        is_valid = True
        query = """
                SELECT * FROM users WHERE email = %(email)s;
                """
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >=1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email Address", "register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        if len(user['address']) < 8:
            flash("Address must be at least 8 characters", "register")
            is_valid = False
        if len(user['city']) < 2:
            flash("City must be at least 2 characters", "register")
            is_valid = False
        if user['state'] == 'NULL':
            flash("Must Select a State from Dropdown Menu", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match", "register")
            is_valid = False
        return is_valid

    @classmethod
    def update_user(cls, form_data, user_id):
        query = f"UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, address = %(address)s, city = %(city)s, state = %(state)s WHERE id = {user_id};"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def is_valid(cls, user):
        valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email Address", "register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        if len(user['address']) < 8:
            flash("Address must be at least 8 characters", "register")
            is_valid = False
        if len(user['city']) < 2:
            flash("City must be at least 2 characters", "register")
            is_valid = False
        if user['state'] == 'NULL':
            flash("Must Select a State from Dropdown Menu", "register")
            is_valid = False
        return valid