from flask import jsonify
from passlib.hash import pbkdf2_sha256 as sha256
from app.instance.config import secret_key
from datetime import datetime, timedelta
import jwt
import re

class User():
    user_id = 1
    users = []

    def __init__(self, first_name, last_name, email, phone, username, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.username = username
        self.password =password
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
        User.users.append(user)
        return user

    def get_single_user(self, email):
        """Retrieve user details by email"""
        single_user = [user for user in User.users if user['email'] == email]
        if single_user:
            return single_user[0]
        return 'not found'

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
