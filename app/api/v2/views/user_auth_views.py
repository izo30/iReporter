from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.user_auth_models import User
from ..utils.validations import Validations
from ..utils.auth import AuthToken
from ..utils.encryption import Encryption

api = Namespace('User Endpoints', description='A collection of user endpoints')

signup_fields = api.model('Signup', {
    'first_name' : fields.String,
    'last_name' : fields.String,
    'email': fields.String,
    'phone' : fields.String,
    'username' : fields.String,
    'password': fields.String,
    'role': fields.String
})

"""user regitration"""
@api.route('/signup')
class Signup(Resource):

    parser = reqparse.RequestParser()
    Validations().add_arguments(parser, ['first_name','last_name','email','phone','username','password','role'])

    @api.expect(signup_fields)
    def post(self):
        args = Signup.parser.parse_args()
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

login_fields = api.model('Login', {
    'email': fields.String,
    'password': fields.String
})
"""user login"""
@api.route('/login')
class Login(Resource):

    parser = reqparse.RequestParser()
    Validations().add_arguments(parser, ['email','password'])

    @api.expect(login_fields)
    def post(self):
        args = Login.parser.parse_args()
        email = args['email']
        password = args['password']

        if Validations().check_if_empty([email, password]):
            return {
                'status': 'Fail',
                'message': 'All fields should be filled'
            }, 400

        if not Validations().validate_email(email):
            return {
                'status': 'Fail',
                'message': 'Invalid email'
            }, 400

        user_result = User().get_single_user(email, password)
        if user_result:
            return {
                'status' : 'Success',
                'message' : 'Logged in successfully',
                'auth_token': user_result.decode('UTF-8')
            }, 200
        else:
            return {
                'status': 'Fail',
                'message': 'User does not exist, sign up!'
            }, 400
                