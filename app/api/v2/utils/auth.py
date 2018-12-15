import jwt
from app.instance.config import secret_key
from functools import wraps
from flask import request, jsonify, make_response
from datetime import datetime, timedelta

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        message = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            message = AuthToken().decode_auth_token(token)

        if not token:
            return {'message' : 'Token is missing.'}, 401

        if message == 'Invalid token. Please log in again.':
            return {'message' : message}, 401

        if message == 'Signature expired. Please log in again.':
            return {'message' : message}, 401

        print('IDENTITY: {}'.format(message))

        if message['role'] == 'user':
            return {'message' : "You are not an admin"}, 401

        return f(*args, **kwargs)
    return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        message = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            message = AuthToken().decode_auth_token(token)

        if not token:
            return {'message' : 'Token is missing.'}, 401

        if message == 'Invalid token. Please log in again.':
            return {'message' : message}, 401

        if message == 'Signature expired. Please log in again.':
            return {'message' : message}, 401

        # print('IDENTITY: {}'.format(token))

        return f(*args, **kwargs)
    return decorated  

class AuthToken():

    def __init__(self):
        pass

    def encode_auth_token(self, id, email, role):
        """ Generates an Auth token"""
        try:
            token = jwt.encode({'id' : id, 'user' : email, 'role' : role, 'exp' : datetime.utcnow() + timedelta(minutes=1440)}, secret_key)
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