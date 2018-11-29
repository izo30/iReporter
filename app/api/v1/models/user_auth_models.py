from passlib.hash import pbkdf2_sha256 as sha256
from app.instance.config import secret_key
from datetime import datetime, timedelta
import jwt

class User():
    user_id = 1
    users = []

    def __init__(self, first_name, last_name, email, phone, username, password, is_admin, registered_on):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.username = username
        self.password =password
        self.is_admin = is_admin
        self.registered_on = registered_on

    def create_user(self):
        user = dict(
            first_name = self.first_name,
            last_name = self.last_name,
            email = self.email,
            phone = self.phone, 
            username = self.username,
            password = self.password,
            is_admin = self.is_admin,
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
