from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from app.api.v1.models.user_auth_models import User

api = Namespace('User Endpoints', description='A collection of user endpoints')

parser = reqparse.RequestParser()
parser.add_argument('first_name', help = 'This field cannot be blank')
parser.add_argument('last_name', help = 'This field cannot be blank')
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('phone', help = 'This field cannot be blank')
parser.add_argument('username', help = 'This field cannot be blank')
parser.add_argument('password', help = 'This field cannot be blank', required = True)
parser.add_argument('role', help = 'This field cannot be blank')
parser.add_argument('registered_on', help = 'This field cannot be blank')

signup_fields = api.model('Signup', {
    'first_name' : fields.String,
    'last_name' : fields.String,
    'email': fields.String,
    'phone' : fields.String,
    'username' : fields.String,
    'password': fields.String,
    'role': fields.String,
    'registered_on': fields.DateTime
})

"""user regitration"""
@api.route('/signup')
class Signup(Resource):
    @api.expect(signup_fields)
    def post(self):
        args = parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']
        phone = args['phone']
        username = args['username']
        password = args['password']
        role = args['role']
        registered_on = args['registered_on']
        
        found_email = User.get_single_user(self, email)
        if found_email == 'not found':
            try:    
                new_user = User(first_name, last_name, email, phone, username, User.generate_hash(password), role, registered_on)
                created_user = new_user.create_user()
                return make_response(jsonify({
                    'status': 'ok',
                    'message': 'User created successfully',
                    'users': created_user
                }), 201)
            
            except Exception as e:
                return make_response(jsonify({
                'message' : str(e),
                'status' : 'failed'
            }), 500)

        return make_response(jsonify({
            'status': 'fail',
            'message' : 'Email already exists, please log in'
        }))

login_fields = api.model('Login', {
    'email': fields.String,
    'password': fields.String
})
"""user login"""
@api.route('/login')
class Login(Resource):
    @api.expect(login_fields)
    def post(self):
        args = parser.parse_args()
        email = args['email']
        password = args['password']
                
        try:
            current_user = User.get_single_user(self, email)
            if current_user == 'not found':
                return make_response(jsonify({
                    'status': 'success',
                    'message': 'User does not exist, sign up!'
                }), 200)
            if current_user and User.verify_hash(password, current_user['password']):
                role = current_user['role']
                token = User.encode_auth_token(email, role)   
                if True:
                    return make_response(jsonify({
                        'status' : 'ok',
                        'message' : 'Logged in successfully',
                        'auth_token': token.decode('UTF-8')
                    }), 200) 
            else:
                return make_response(jsonify({
                    'message' : 'Incorrect email or password',
                    'status' : 'fail'
                }), 400)

        except Exception as e:
            return make_response(jsonify({
                'message' : str(e),
                'status' : 'failed'
            }), 500)
