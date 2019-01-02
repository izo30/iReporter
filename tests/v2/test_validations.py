import json
from tests.v2.base_test import BaseTest
from tests.v2.test_data import signup_url, login_url, incident_url, user5_login,\
 invalid_user, invalid_email_login, empty_values_user, empty_values_login,\
 incident1

class TestValidations(BaseTest):

    def generate_auth_token(self):
        resp = self.client().post(login_url, data =user5_login)
        auth_token = json.loads(resp.data.decode('UTF-8'))['auth_token']
        return auth_token

    def test_user_signup_validation(self):
        response = self.client().post(
            signup_url, 
            data = json.dumps(invalid_user), 
            content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Fail', result['status'])

    def test_user_login_validation(self):
        response = self.client().post(
            login_url, 
            data = json.dumps(invalid_email_login), 
            content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Fail', result['status'])
        self.assertEqual('Invalid email', result['error'])

    def test_empty_values_signup_validation(self):
        response = self.client().post(
            signup_url, 
            data = json.dumps(empty_values_user), 
            content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Fail', result['status'])

    def test_empty_values_login_validation(self):
        response = self.client().post(
            login_url, 
            data = json.dumps(empty_values_login), 
            content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Fail', result['status'])

    def test_empty_fields_signup_validation(self):
        response = self.client().post(
            signup_url, 
            data = json.dumps(""),
            content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Input payload validation failed', result['message'])

    def test_empty_fields_login_validation(self):
        response = self.client().post(
            login_url, 
            data = json.dumps(""),
            content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Input payload validation failed', result['message'])

    def test_empty_fields_create_incident_validation(self):
        user_auth_token = self.generate_auth_token()
        create_incident = self.client().post(
            incident_url, 
            headers = dict(Authorization="{}".format(user_auth_token)),
            data = "")
        """Asserts test return true status_code and message"""
        result = json.loads(create_incident.data)
        self.assertEqual(create_incident.status_code, 400)
        self.assertEqual('Input payload validation failed', result['message'])