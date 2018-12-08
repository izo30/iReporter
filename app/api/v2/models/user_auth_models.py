from flask import jsonify
from passlib.hash import pbkdf2_sha256 as sha256
from app.instance.config import secret_key
from datetime import datetime, timedelta
import jwt
import re
import psycopg2

class User():
    users = []

    def __init__(self, first_name, last_name, email, phone, username, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.username = username
        self.password = password
        self.role = role
        self.registered_on = datetime.now()

        try:
            self.connection = psycopg2.connect(
                "dbname='ireporter' user='postgres' host='localhost' password='F31+35e9' port='5432'")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

        except:
            print("Cannot connect to database")

    def create_user(self):
        user = dict(
            first_name = self.first_name,
            last_name = self.last_name,
            email = self.email,
            phone = self.phone, 
            username = self.username,
            password = self.password,
            role = self.role,
            registered_on = self.registered_on
        )

        empty_field = User.check_if_empty(user)
        if empty_field:
            return empty_field

        data_type = self.validate_data()
        if data_type:
            return data_type

        hashed_password = User.generate_hash(self.password)

        query = "SELECT * FROM users WHERE email='{}'" .format(self.email)
        self.cursor.execute(query)
        user = self.cursor.fetchone()

        if not user:
            create_user_query = "INSERT INTO users(first_name, last_name, email, phone, username, password, role,\
             registered_on)\
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(create_user_query, (self.first_name, self.last_name, self.email, self.phone,\
            self.username, hashed_password, self.role, datetime.now()))

            response_user = dict(
                first_name = self.first_name,
                last_name = self.last_name,
                username = self.username,
                role = self.role,
                registered_on = self.registered_on
            )
            return response_user
        else:
            return response_user

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
    def encode_auth_token(email, role):
        """ Generates an Auth token"""
        try:
            token = jwt.encode({'user' : email, 'role' : role, 'exp' : datetime.utcnow() + timedelta(minutes=1440)}, secret_key)
    
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

    def validate_data(self):

        error_response = {}
        error = False

        if not re.match(r"(^[a-zA-Z]+$)", self.first_name):
            error = True
            error_response['first_name'] = "First name should contain letters only"
        elif not re.match(r"(^[a-zA-Z]+$)", self.last_name):
            error = True
            error_response['last_name'] = "Last name should contain letters only"
        elif not User.validate_email(self.email):
            error = True
            error_response['email'] = "Invalid email"
        elif not re.match(r"^([\s\d]+)$", self.phone):
            error = True
            error_response['phone'] = "Invalid phone number"
        elif not re.match(r"[a-z A-Z0-9\_\"]+$", self.username):
            error = True
            error_response['username'] = "Username should contain only numbers, letters and underscore"
        elif not User.validate_password(self.password):
            error = True
            error_response['password'] = "The password should contain a small and a capital letter, a number and a special character"
        elif not User.check_if_role(self.role):
            error = True
            error_response['role'] = "Role should be admin or user"

        if error:
            print ("ERROR : {}" .format(error_response))
            error_message = dict( error = error_response )
            return error_message


