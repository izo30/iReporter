from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.user_auth_models import User

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
    parser.add_argument('first_name', help = 'This field cannot be blank', required = True)
    parser.add_argument('last_name', help = 'This field cannot be blank', required = True)
    parser.add_argument('email', help = 'This field cannot be blank', required = True)
    parser.add_argument('phone', help = 'This field cannot be blank', required = True)
    parser.add_argument('username', help = 'This field cannot be blank', required = True)
    parser.add_argument('password', help = 'This field cannot be blank', required = True)
    parser.add_argument('role', help = 'This field cannot be blank', required = True)

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
        
        new_user = User()
        created_user = new_user.create_user(first_name, last_name, email, phone, username, password, role)

        if created_user == "Field should not be empty":
            return make_response(jsonify({
                'status': 'Fail',
                'message': created_user
            }), 400)

        try:
            if created_user['error']:
                return make_response(jsonify({
                    'status': 'Fail',
                    'error': created_user['error']
                }), 400)
        except Exception:
            pass

        print("ID : {}" .format(created_user['id']))
        token = User.encode_auth_token(created_user['id'], email, role)   
        return make_response(jsonify({
            'status' : 'Success',
            'message' : 'Signed up successfully',
            'auth_token': token.decode('UTF-8')
        }), 201)

login_fields = api.model('Login', {
    'email': fields.String,
    'password': fields.String
})
"""user login"""
@api.route('/login')
class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', help = 'This field cannot be blank', required = True)
    parser.add_argument('password', help = 'This field cannot be blank', required = True)

    @api.expect(login_fields)
    def post(self):
        args = Login.parser.parse_args()
        email = args['email']
        password = args['password']

        if email is None or email == "":
            return make_response(jsonify({
                'status': 'Fail',
                'message': 'Email should be provided'
            }), 400)

        if password is None or password == "":
            return make_response(jsonify({
                'status': 'Fail',
                'message': 'Password should be provided'
            }), 400)

        if not User.validate_email(email):
            return make_response(jsonify({
                'status': 'Fail',
                'message': 'Invalid email'
            }), 400)
                
        try:
            user = User()
            current_user = user.get_single_user(email)
            if current_user == 'User not found':
                return make_response(jsonify({
                    'status': 'Fail',
                    'message': 'User does not exist, sign up!'
                }), 400)
            if current_user and User.verify_hash(password, current_user['password']):
                role = current_user['role']
                id = current_user['id']
                token = User.encode_auth_token(id, email, role)   
                return make_response(jsonify({
                    'status' : 'Success',
                    'message' : 'Logged in successfully',
                    'auth_token': token.decode('UTF-8')
                }), 200) 
            else:
                return make_response(jsonify({
                    'status' : 'Fail',
                    'message' : 'Incorrect email or password'
                }), 400)

        except Exception as e:
            return make_response(jsonify({
                'status' : 'Fail',
                'message' : str(e)
            }), 500)