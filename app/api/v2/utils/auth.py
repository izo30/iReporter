import jwt
from instance.config import secret_key
from app.api.v2.utils.validations import Validations
from functools import wraps
from flask import request, jsonify, make_response
from datetime import datetime, timedelta

EXPIRED_SIGNATURE = "Signature expired. Please log in again."
INVALID_TOKEN = "Invalid token. Please log in again."
ADMIN = "admin"
USER = "user"

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        message = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            message = AuthToken().decode_auth_token(token)

        if not Validations().token_present(token):
            return {'message' : 'Token is missing.'}, 401

        if Validations().check_token_error(message):
            return {'message' : message}, 401

        if not Validations().check_if_admin(message['role']):
            return {'message' : "You are not an admin"}, 401

        return f(*args, **kwargs)
    return decorated

def user_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        message = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            message = AuthToken().decode_auth_token(token)

        if not Validations().token_present(token):
            return {'message' : 'Token is missing.'}, 401

        if Validations().check_token_error(message):
            return {'message' : message}, 401

        if not Validations().check_if_user(message['role']):
            return {'message' : "You are not a normal user"}, 401

        return f(*args, **kwargs)
    return decorated  

class AuthToken():

    def __init__(self):
        pass

    def encode_auth_token(self, _id, email, role):
        """ Generates an Auth token"""
        try:
            token = jwt.encode({'id' : _id, 'user' : email, 'role' : role, 'exp' : datetime.utcnow() + timedelta(minutes=1440)}, secret_key)
            return token
        except Exception as e:
            return e 

    def decode_auth_token(self, auth_token):
        """Method to decode the auth token"""
        try:
            payload = jwt.decode(auth_token, secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def get_user_id(self):
        token = None
        content = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            content = self.decode_auth_token(token)

        _id = content['id']
        if _id: return _id