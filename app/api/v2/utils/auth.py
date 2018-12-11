import jwt
from app.instance.config import secret_key
from functools import wraps
from ..models.user_auth_models import User
from flask import request, jsonify, make_response

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        message = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            message = User.decode_auth_token(token)

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
            message = User.decode_auth_token(token)

        if not token:
            return {'message' : 'Token is missing.'}, 401

        if message == 'Invalid token. Please log in again.':
            return {'message' : message}, 401

        if message == 'Signature expired. Please log in again.':
            return {'message' : message}, 401

        # print('IDENTITY: {}'.format(token))

        return f(*args, **kwargs)
    return decorated  
