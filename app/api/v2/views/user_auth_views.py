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
        
        new_user = User(first_name, last_name, email, phone, username, password, role)
        created_user = new_user.create_user()

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

        token = User.encode_auth_token(email, role)   
        return make_response(jsonify({
            'status' : 'Success',
            'message' : 'Signed up successfully',
            'auth_token': token.decode('UTF-8')
        }), 201)

