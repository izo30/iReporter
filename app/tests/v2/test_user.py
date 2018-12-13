# Library imports
import json
# Local application imports
from app.tests.v2.base_test import BaseTest
from app.api.v2.models.user_auth_models import User
from app.api.v2.utils.auth import AuthToken
from .test_data import signup_url, login_url, user1, admin_login, encode_token_data, user2, user3, user4

class TestUser(BaseTest):

    def test_create_user(self):
        response = self.client().post(signup_url, data=json.dumps(user1)
        , content_type = 'application/json')

        result = json.loads(response.data)
        self.assertEqual('Success', result['status'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual('Success', result['status'])

    def test_create_user_already_exist(self):
        self.client().post(signup_url, data=json.dumps(user2)
        , content_type = 'application/json')
        response = self.client().post(signup_url, data=json.dumps(user2)
        , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual('Fail', result['status'])
        self.assertEqual('User already exists, signup with another email', result['error'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_user_login(self):
        response = self.client().post(login_url, data=json.dumps(admin_login)
        ,content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual('Success', result['status'])
        self.assertEqual('Logged in successfully', result['message'])
        self.assertEqual(response.status_code, 200)
            
    def test_encode_auth_token(self):
        auth_token = AuthToken().encode_auth_token(encode_token_data['user_id'], encode_token_data['email'], encode_token_data['role'])
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        auth_token = AuthToken().encode_auth_token(encode_token_data['user_id'], encode_token_data['email'], encode_token_data['role'])
        self.assertEqual(AuthToken().decode_auth_token(auth_token)['id'], encode_token_data['user_id'])

    def test_user_validation(self):
        response = self.client().post(signup_url, data=json.dumps(user4)
        , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual('Invalid email', result['error']['email'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Fail', result['status'])
