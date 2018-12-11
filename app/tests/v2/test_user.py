# Library imports
import json
# Local application imports
from app.tests.v2.base_test import BaseTest
from app.api.v2.models.user_auth_models import User

signup_url = 'api/v2/auth/signup'
login_url = 'api/v2/auth/login'

class TestUser(BaseTest):

    def test_create_user(self):
        response = self.client().post(signup_url, data=json.dumps(dict(
            first_name = 'brian',
            last_name = 'wainaina',
            email = 'brian@gmail.com',
            phone = '0736547657', 
            username = 'brian',
            password = 'F31+25e9',
            role = 'user'
        )), content_type = 'application/json')

        result = json.loads(response.data)
        self.assertEqual('Success', result['status'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual('Success', result['status'])
        self.assertTrue(response.content_type == 'application/json')

    def test_get_single_user(self):
        response = self.client().post(login_url, data=json.dumps(dict(
            email = 'brian@gmail.com',
            password = 'F31+25e9'
        )), content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual('Logged in successfully', result['message'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Success', result['status'])
        self.assertTrue(response.content_type == 'application/json')

    def test_create_user_already_exist(self):
        response = self.client().post(signup_url, data=json.dumps(dict(
            first_name = 'isaac',
            last_name = 'wangethi',
            email = 'isaacwangethi30@gmail.com',
            phone = '0736547657', 
            username = 'isaac',
            password = 'F31+25e9',
            role = 'user'
        )), content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual('Fail', result['status'])
        self.assertEqual('User already exists, signup with another email', result['error'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_user_login(self):
        #Registered user login
        response = self.client().post(login_url, data=json.dumps(dict(
            email = 'isaacwangethi30@gmail.com',
            password = 'F31+25e9',
        )),content_type = 'application/json')

        result = json.loads(response.data)
        self.assertEqual('Success', result['status'])
        self.assertTrue('Logged in successfully', result['message'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content_type == 'application/json')
            
    def test_encode_auth_token(self):
        user_id = 'aa520a77-a9a2-461c-9efa-169bb698391c'
        email = 'brian@gmail.com'
        role = 'user'
        user = User()
        auth_token = user.encode_auth_token(user_id, email, role)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user_id = 'aa520a77-a9a2-461c-9efa-169bb698391c'
        email = 'brian@gmail.com'
        role = 'user'
        user = User()
        auth_token = user.encode_auth_token(user_id, email, role)
        self.assertTrue(isinstance(auth_token, bytes))
        print ("AUTH TOKEN : {}" .format(auth_token))
        self.assertTrue(user.decode_auth_token(auth_token)['id'] == 'user_id')

    def test_user_password_validation(self):
        response = self.client().post(signup_url, data=json.dumps(dict(
            first_name = 'brian',
            last_name = 'wainaina',
            email = 'brin@gmail.com',
            phone = '0736547657', 
            username = 'brian',
            password = '123456',
            role = 'user'
        )), content_type = 'application/json')

        result = json.loads(response.data)
        self.assertEqual('The password should contain a small and a capital letter, a number and a special character', result['error']['password'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Fail', result['status'])
        self.assertTrue(response.content_type == 'application/json')

    def test_user_email_validation(self):
        response = self.client().post(signup_url, data=json.dumps(dict(
            first_name = 'brian',
            last_name = 'wainaina',
            email = 'briangmail.com',
            phone = '0736547657', 
            username = 'brian',
            password = 'F31+25e9',
            role = 'user'
        )), content_type = 'application/json')

        result = json.loads(response.data)
        self.assertEqual('Invalid email', result['error']['email'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Fail', result['status'])
        self.assertTrue(response.content_type == 'application/json')
