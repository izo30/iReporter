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
        self.assertEqual('User created successfully', result['message'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual('ok', result['status'])
        self.assertTrue(response.content_type == 'application/json')

    def test_get_single_user(self):
        with self.client():
            response = self.client().post(login_url, data=json.dumps(dict(
                email = 'isaac@gmail.com',
                password = 'F31+25e9'
            )), content_type = 'application/json')
            result = json.loads(response.data)
            self.assertEqual('Logged in successfully', result['message'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual('ok', result['status'])
            self.assertTrue(response.content_type == 'application/json')

    def test_create_user_already_exist(self):
        user = User(
            first_name = 'isaac',
            last_name = 'wangethi',
            email = 'isaac@gmail.com',
            phone = '0736547657', 
            username = 'isaac',
            password = 'F31+25e9',
            role = 'user'
        )
        with self.client():
            response = self.client().post(reg_url, data=json.dumps(dict(
                first_name = 'isaac',
                last_name = 'wangethi',
                email = 'isaac@gmail.com',
                phone = '0736547657', 
                username = 'isaac',
                password = 'F31+25e9',
                role = 'user'
            )), content_type = 'application/json')
            result = json.loads(response.data)
            self.assertEqual('fail', result['status'])
            self.assertEqual('Email already exists, please log in', result['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
    
    def test_user_login(self):
        """test for registered user login"""
        with self.client():
            #User registration
            response = self.client().post(login_url, data=json.dumps(dict(
                first_name = 'isaac',
                last_name = 'wangethi',
                email = 'isaac@gmail.com',
                phone = '0736547657', 
                username = 'isaac',
                password = 'F31+25e9',
                role = 'user'
            )), content_type = 'application/json')

            result = json.loads(response.data)
            self.assertEqual('Logged in successfully', result['message'])
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual('Incorrect email or password', result['message'])
            self.assertTrue(response.content_type == 'application/json')

            #Registered user login
            response2 = self.client().post(login_url, data=json.dumps(dict(
                email = 'isaac@gmail.com',
                password = 'F31+25e9',
            )), 
            content_type = 'application/json'
        )
            result2 = json.loads(response2.data)
            self.assertEqual('ok', result['status'])
            self.assertTrue('logged in Successfully', result2['message'])
            self.assertEqual(response2.status_code, 200)
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
        self.assertEqual('the password should contain a small and a capital letter, a number and a special character', result['message'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual('fail', result['status'])
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
        self.assertEqual('invalid email', result['message'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual('fail', result['status'])
        self.assertTrue(response.content_type == 'application/json')
