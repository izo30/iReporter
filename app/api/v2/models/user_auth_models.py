from flask import jsonify
from passlib.hash import pbkdf2_sha256 as sha256
from app.instance.config import secret_key
from datetime import datetime, timedelta
import jwt
import re

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

        data_type = User.validate_data(user)
        if data_type:
            return data_type

        user['password'] = User.generate_hash(user['password'])

        print ("User : {}" .format(user))

        User.users.append(user)

        response_user = dict(
            first_name = self.first_name,
            last_name = self.last_name,
            username = self.username,
            role = self.role,
            registered_on = self.registered_on
        )

        return response_user

    def get_single_user(self, email):
        """Retrieve user details by email"""

        if email is None or email == "":
            return "Email should not be empty"

        single_user = [user for user in User.users if user['email'] == email]
        if single_user:
            return single_user[0]
        return 'Not found'

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

    @staticmethod
    def validate_data(user):

        error_response = {}
        error = False

        for key, value in user.items():
            if key == 'first_name' and not re.match(r"(^[a-zA-Z]+$)", value):
                error = True
                error_response[key] = "First name should contain letters only"
            elif key == 'last_name' and not re.match(r"(^[a-zA-Z]+$)", value):
                error = True
                error_response[key] = "Last name should contain letters only"
            elif key == 'email' and not User.validate_email(value):
                error = True
                error_response[key] = "Invalid email"
            elif key == 'phone' and not re.match(r"^([\s\d]+)$", value):
                error = True
                error_response[key] = "Invalid phone number"
            elif key == 'username' and not re.match(r"[a-z A-Z0-9\_\"]+$", value):
                error = True
                error_response[key] = "Username should contain only numbers, letters and underscore"
            elif key == 'password' and not User.validate_password(value):
                error = True
                error_response[key] = "The password should contain a small and a capital letter, a number and a special character"
            elif key == 'role' and not User.check_if_role(value):
                error = True
                error_response[key] = "Role should be admin or user"

        if error:
            print ("ERROR : {}" .format(error_response))
            error_message = dict( error = error_response )
            return error_message


