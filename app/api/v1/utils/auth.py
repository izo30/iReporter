import jwt
from app.instance.config import secret_key
from functools import wraps
from app.api.v1.models.user_auth_models import User
from flask import request, jsonify, make_response

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = None
        authentication_header = request.headers.get('Authorization')
        if authentication_header:    
            try:
                auth_token = authentication_header.split(" ")[1]
                    
                identity = User.decode_auth_token(auth_token)
                print('TOKEN: {}'.format(identity))
                if identity == 'Invalid token. Please log in again.':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'Invalid token. Please log in again.'
                    }), 401)

            except Exception:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'You are not authorized'
                }), 401)
                
            if auth_token:
                
                if identity['role'] == 'user':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'You are not an admin'
                    }), 401)
        return f(*args, **kwargs)
    return decorated


def token_required(j):
    @wraps(j)
    @classmethod
    def decorated_token(*args, **kwargs):
        auth_token = None
        authentication_header = request.headers.get('Authorization')
        if authentication_header:    
            try:
                auth_token = authentication_header.split(" ")[1]
                    
                identity = User.decode_auth_token(auth_token)
                
                if identity == 'Invalid token. Please log in again.':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'Invalid token. Please log in again.'
                    }), 401)

            except Exception:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'You are not authorized'
                }), 401)
        return j(*args, **kwargs)
    return decorated_token

def tokenRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        identity = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            identity = User.decode_auth_token(token)

        if not token:
            return {'message' : 'Token is missing.'}, 401

        # if identity['message'] == 'Invalid token. Please log in again.':
        #     return {'message' : 'Invalid token. Please log in again.'}, 401

        # if identity['message'] == 'Signature expired. Please log in again.':
        #     return {'message' : 'Signature expired. Please log in again.'}, 401

        print('IDENTITY: {}'.format(identity))

        return f(*args, **kwargs)
    return decorated  


# def adminRequired(j):
#     @wraps(j)
#     def decorated(*args, **kwargs):

#         token = None
#         identity = None

#         if 'Authorization' in request.headers:
#             token = request.headers['Authorization']
#             identity = User.decode_auth_token(token)

#         if not token:
#             return {'message' : 'Token is missing.'}, 401

#         # if identity['message'] == 'Invalid token. Please log in again.':
#         #     return {'message' : 'Invalid token. Please log in again.'}, 401

#         # if identity['message'] == 'Signature expired. Please log in again.':
#         #     return {'message' : 'Signature expired. Please log in again.'}, 401

#         print('TOKEN: {}'.format(token))

#         return j(*args, **kwargs)
#     return decorated  
