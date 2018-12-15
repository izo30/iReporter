from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from app.api.v2.models.user_auth_models import User
from app.api.v2.utils.validations import Validations
from app.api.v2.utils.auth import AuthToken
from app.api.v2.utils.encryption import Encryption
from app.api.v2.utils.views_fields import user_api as api, UserFields

"""user regitration"""
@api.route('/signup')
class Signup(Resource):
    @api.expect(UserFields.signup_fields)
    def post(self):
        parser = UserFields.required_signup_fields()
        args = parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']
        phone = args['phone']
        username = args['username']
        password = args['password']
        role = args['role']

        validate = Validations().validate_user_data(first_name, last_name, email, phone, username, password, role)
        if validate:
            return {
                'status': 'Fail',
                'error': validate['error']
            }, 400
        
        created_user = User().create_user(first_name, last_name, email, phone, username, Encryption().generate_hash(password), role)
        if created_user:
            token = AuthToken().encode_auth_token(created_user['id'], email, role)   
            return {
                'status' : 'Success',
                'message' : 'Signed up successfully',
                'auth_token': token.decode('UTF-8')
            }, 201
        else:
            return {
                'status' : 'Fail',
                'error' : 'User already exists, signup with another email'
            }, 400

"""user login"""
@api.route('/login')
class Login(Resource):
    @api.expect(UserFields.login_fields)
    def post(self):
        parser = UserFields.required_login_fields()
        args = parser.parse_args()
        email = args['email']
        password = args['password']

        is_empty = Validations().check_if_empty(dict(email = email, password = password))
        if is_empty:
            return {
                'status': 'Fail',
                'error': is_empty
            }, 400

        if not Validations().validate_email(email):
            return {
                'status': 'Fail',
                'error': 'Invalid email'
            }, 400

        user = User().get_single_user(email, password)
        if user:
            if Encryption().verify_hash(password, user['hash']):
                token = AuthToken().encode_auth_token(user['id'], user['email'], user['role'])
                return {
                    'status' : 'Success',
                    'message' : 'Logged in successfully',
                    'auth_token': token.decode('UTF-8')
                }, 200
            else:
                return {
                    'status' : 'Fail',
                    'error': "Wrong password"
                }, 400
        else:
            return {
                'status': 'Fail',
                'message': 'User does not exist, sign up!'
            }, 400
                