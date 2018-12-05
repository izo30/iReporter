# Library imports
import json
# Local application imports
from app.tests.v1.base_test import BaseTest
from app.api.v1.models.user_auth_models import User

reg_url = 'api/v1/auth/signup'
login_url = 'api/v1/auth/login'

class TestUser(BaseTest):

    def test_create_user(self):
        response = self.client().post(reg_url, data=json.dumps(dict(
            first_name = 'brian',
            last_name = 'wainaina',
            email = 'brian@gmail.com',
            phone = '0736547657', 
            username = 'brian',
            password = 'F31+25e9',
            role = 'user'
        )), content_type = 'application/json')

        result = json.loads(response.data)
        self.assertEqual('brian@gmail.com', result['data']['email'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual('Success', result['status'])
        self.assertTrue(response.content_type == 'application/json')

    def test_get_single_user(self):
        response = self.client().post(login_url, data=json.dumps(dict(
            email = 'isaac@gmail.com',
            password = 'F31+25e9'
        )), content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual('Logged in successfully', result['message'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Success', result['status'])
        self.assertTrue(response.content_type == 'application/json')

    def test_create_user_already_exist(self):
        response = self.client().post(reg_url, data=json.dumps(dict(
            first_name = 'isaac',
            last_name = 'wangethi',
            email = 'brit@gmail.com',
            phone = '0736547657', 
            username = 'isaac',
            password = 'F31+25e9',
            role = 'user'
        )), content_type = 'application/json')

        response = self.client().post(reg_url, data=json.dumps(dict(
            first_name = 'isaac',
            last_name = 'wangethi',
            email = 'brit@gmail.com',
            phone = '0736547657', 
            username = 'isaac',
            password = 'F31+25e9',
            role = 'user'
        )), content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual('Fail', result['status'])
        self.assertEqual('Email already exists, please log in', result['message'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 303)
    
    def test_user_login(self):
        """test for registered user login"""
        #User registration
        response = self.client().post(reg_url, data=json.dumps(dict(
            first_name = 'isaac',
            last_name = 'wangethi',
            email = 'bri@gmail.com',
            phone = '0736547657', 
            username = 'isaac',
            password = 'F31+25e9',
            role = 'user'
        )), content_type = 'application/json')

        register_result = json.loads(response.data)
        self.assertEqual('Success', register_result['status'])
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.content_type == 'application/json')

        #Registered user login
        response = self.client().post(login_url, data=json.dumps(dict(
            email = 'brian@gmail.com',
            password = 'F31+25e9',
        )),content_type = 'application/json')

        result = json.loads(response.data)
        self.assertEqual('Success', result['status'])
        self.assertTrue('Logged in successfully', result['message'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content_type == 'application/json')
            
    def test_encode_auth_token(self):
        user = User(
            first_name = 'isaac',
            last_name = 'wangethi',
            email = 'isaac@gmail.com',
            phone = '0736547657', 
            username = 'isaac',
            password = 'F31+25e9',
            role = 'user'
        )

        auth_token = user.encode_auth_token(user.email, user.role)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            first_name = 'isaac',
            last_name = 'wangethi',
            email = 'isaac@gmail.com',
            phone = '0736547657', 
            username = 'isaac',
            password = 'F31+25e9',
            role = 'user'
        )

        auth_token = user.encode_auth_token(user.email, user.role)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token)['role'] == 'user')

    def test_user_password_validation(self):
        response = self.client().post(reg_url, data=json.dumps(dict(
            first_name = 'brian',
            last_name = 'wainaina',
            email = 'brian@gmail.com',
            phone = '0736547657', 
            username = 'brian',
            password = '123456',
            role = 'user'
        )), content_type = 'application/json')

        result = json.loads(response.data)
        self.assertEqual('The password should contain a small and a capital letter, a number and a special character', result['message'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Fail', result['status'])
        self.assertTrue(response.content_type == 'application/json')

    def test_user_email_validation(self):
        response = self.client().post(reg_url, data=json.dumps(dict(
            first_name = 'brian',
            last_name = 'wainaina',
            email = 'briangmail.com',
            phone = '0736547657', 
            username = 'brian',
            password = 'F31+25e9',
            role = 'user'
        )), content_type = 'application/json')

        result = json.loads(response.data)
        self.assertEqual('Invalid email', result['message'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Fail', result['status'])
        self.assertTrue(response.content_type == 'application/json')
