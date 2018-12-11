from flask import jsonify
from passlib.hash import pbkdf2_sha256 as sha256
from app.instance.config import secret_key
from datetime import datetime, timedelta
import jwt
import re
import psycopg2
import uuid

class User():
    users = []

    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname='ireporter' user='postgres' host='localhost' password='F31+35e9' port='5432'")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

        except:
            print("Cannot connect to database")

    def create_user(self, first_name, last_name, email, phone, username, password, role):
        user = dict(
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone = phone, 
            username = username,
            password = password,
            role = role
        )

        empty_field = User.check_if_empty(user)
        if empty_field:
            return empty_field

        data_type = self.validate_data(first_name, last_name, email, phone, username, password, role)
        if data_type:
            return data_type

        hashed_password = User.generate_hash(password)

        query = "SELECT * FROM users WHERE email='{}'" .format(email)
        self.cursor.execute(query)
        user = self.cursor.fetchone()

        if not user:
            _id = uuid.uuid4()
            _id = str(_id)
            create_user_query = "INSERT INTO users(id, first_name, last_name, email, phone, username, password, role,\
             registered_on)\
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(create_user_query, (_id, first_name, last_name, email, phone, username, hashed_password, role, datetime.now()))

            response_user = dict(
                id = _id,
                first_name = first_name,
                last_name = last_name,
                username = username,
                role = role
            )
            return response_user
        else:
            return dict(error = "User already exists, signup with another email")

    def get_single_user(self, email):
        query = "SELECT * FROM users WHERE email='{}'" .format(email)
        self.cursor.execute(query)
        user = self.cursor.fetchone()

        if user:
            return dict(
                id = user[0],
                role = user[7],
                password = user[6]
            )

        else:
            return "User not found"

    def get_cursor(self):
        try:
            connection = psycopg2.connect(
                "dbname='ireporter' user='postgres' host='localhost' password='F31+35e9' port='5432'")
            connection.autocommit = True
            cursor = connection.cursor()
            return cursor
        except:
            return "Cannot connect to database"

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @staticmethod
    def validate_password(password):
        if re.match(r"(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{8,})", password):
            return True
        return False

    @staticmethod
    def validate_email(email):
        if re.match(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        return False

    @staticmethod
    def encode_auth_token(id, email, role):
        """ Generates an Auth token"""
        try:
            token = jwt.encode({'id' : id, 'user' : email, 'role' : role, 'exp' : datetime.utcnow() + timedelta(minutes=1440)}, secret_key)
    
            return token

        except Exception as e:
            return e 

    @staticmethod
    def decode_auth_token(auth_token):
        """Method to decode the auth token"""
        try:
            payload = jwt.decode(auth_token, secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def check_if_empty(incident):
        for key, value in incident.items():
            if value is None or value == "":
                return "Field should not be empty"

    @staticmethod
    def check_if_role(role):
        if role == "admin":
            return True
        elif role == "user":
            return True
        else:
            return False

    def validate_data(self, first_name, last_name, email, phone, username, password, role):

        error_response = {}
        error = False

        if not re.match(r"(^[a-zA-Z]+$)", first_name):
            error = True
            error_response['first_name'] = "First name should contain letters only"
        elif not re.match(r"(^[a-zA-Z]+$)", last_name):
            error = True
            error_response['last_name'] = "Last name should contain letters only"
        elif not User.validate_email(email):
            error = True
            error_response['email'] = "Invalid email"
        elif not re.match(r"^([\s\d]+)$", phone):
            error = True
            error_response['phone'] = "Invalid phone number"
        elif not re.match(r"[a-z A-Z0-9\_\"]+$", username):
            error = True
            error_response['username'] = "Username should contain only numbers, letters and underscore"
        elif not User.validate_password(password):
            error = True
            error_response['password'] = "The password should contain a small and a capital letter, a number and a special character"
        elif not User.check_if_role(role):
            error = True
            error_response['role'] = "Role should be admin or user"

        if error:
            print ("ERROR : {}" .format(error_response))
            error_message = dict( error = error_response )
            return error_message


