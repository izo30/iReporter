from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.user_auth_models import User

api = Namespace('User Endpoints', description='A collection of user endpoints')

parser = reqparse.RequestParser()
parser.add_argument('first_name', help = 'This field cannot be blank')
parser.add_argument('last_name', help = 'This field cannot be blank')
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('phone', help = 'This field cannot be blank')
parser.add_argument('username', help = 'This field cannot be blank')
parser.add_argument('password', help = 'This field cannot be blank', required = True)
parser.add_argument('is_admin', help = 'This field cannot be blank')
parser.add_argument('registered_on', help = 'This field cannot be blank', required = True)


signup_fields = api.model('Signup', {
    'first_name' : fields.String,
    'last_name' : fields.String,
    'email': fields.String,
    'phone' : fields.String,
    'username' : fields.String,
    'password': fields.String,
    'is_admin': fields.Boolean,
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
        is_admin = args['is_admin']
        registered_on = args['registered_on']
        
        found_email = User.get_single_user(self, email)
        if found_email == 'not found':
            try:    
                new_user = User(first_name, last_name, email, phone, username, password, is_admin, registered_on)
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
