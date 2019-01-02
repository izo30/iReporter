import json
from tests.v2.test_data import incident_url, incident1, encode_token_data
from tests.v2.base_test import BaseTest
from app.api.v2.utils.auth import AuthToken

class TestAuth(BaseTest):

    def test_missing_token(self):
        """method to test for expired auth token"""
        create_incident = self.client().post(
            incident_url, 
            data = incident1)
        """Asserts test return signature expired message"""
        result = json.loads(create_incident.data)
        self.assertEqual('Token is missing.', result['message'])

    def test_expired_auth_token(self):
        """method to test for expired auth token"""
        auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEzNmJmZTAyLWMxYTYtNDEzMC1iZjAwLWM3YTcyMDQ3ZGRlZiIsInVzZXIiOiJicmlhbkBnbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImV4cCI6MTU0NDQ0MDk2NX0.nyDLC6IP7GC8zryGCmoogVIrAXBnazvUmcR40mC-wMk"
        create_incident = self.client().post(
            incident_url, 
            headers = dict(Authorization = "{}".format(auth_token)),
            data = incident1)
        """Asserts test return signature expired message"""
        result = json.loads(create_incident.data)
        self.assertEqual('Signature expired. Please log in again.', result['message'])

    def test_invalid_auth_token(self):
        """method to test for expired auth token"""
        auth_token = "eyJ0eXAiOiJKv2QiLCJhbGciOi9eyJm1i4IjZ781wgIYDvB3KMA"
        create_incident = self.client().post(
            incident_url, 
            headers = dict(Authorization = "{}".format(auth_token)),
            data = incident1)
        """Asserts test return signature expired message"""
        result = json.loads(create_incident.data)
        self.assertEqual('Invalid token. Please log in again.', result['message'])

    def test_encode_auth_token(self):
        auth_token = AuthToken().encode_auth_token(
            encode_token_data['user_id'], 
            encode_token_data['email'], 
            encode_token_data['role'])
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        auth_token = AuthToken().encode_auth_token(
            encode_token_data['user_id'], 
            encode_token_data['email'], 
            encode_token_data['role'])
        self.assertEqual(
            AuthToken().decode_auth_token(auth_token)['id'], 
            encode_token_data['user_id'])