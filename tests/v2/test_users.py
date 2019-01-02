import json
from tests.v2.base_test import BaseTest
from tests.v2.test_data import signup_url, login_url, user1, admin_login,\
 not_exist_login, wrong_password_login, user2

class TestUser(BaseTest):

    def test_create_user(self):
        response = self.client().post(
            signup_url, 
            data = json.dumps(user1),
            content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual('Success', result['status'])
        self.assertEqual(response.status_code, 201)

    def test_create_user_already_exist(self):
        self.client().post(
            signup_url, 
            data = json.dumps(user2), 
            content_type = 'application/json')
        response = self.client().post(
            signup_url, 
            data = json.dumps(user2), 
            content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual('Fail', result['status'])
        self.assertEqual('User already exists, signup with another email', result['error'])
        self.assertEqual(response.status_code, 403)

    def test_user_login(self):
        response = self.client().post(
            login_url, 
            data = json.dumps(admin_login),
            content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual('Success', result['status'])
        self.assertEqual('Logged in successfully', result['message'])
        self.assertEqual(response.status_code, 200)

    def test_login_user_not_exist(self):
        response = self.client().post(
            login_url, 
            data = json.dumps(not_exist_login),
            content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual('Fail', result['status'])
        self.assertEqual('User does not exist, sign up!', result['message'])
        self.assertEqual(response.status_code, 403)

    def test_login_wrong_password(self):
        response = self.client().post(
            login_url, 
            data = json.dumps(wrong_password_login),
            content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual('Fail', result['status'])
        self.assertEqual('Wrong password', result['error'])
        self.assertEqual(response.status_code, 400)
