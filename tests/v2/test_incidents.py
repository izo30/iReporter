import json
from tests.v2.base_test import BaseTest
from tests.v2.test_data import signup_url, login_url, incident_url, user5,\
 user5_login, admin_login, incident1, incident2,incident4, admin_edited_status,\
 edited_comment, edited_location

class TestIncidents(BaseTest):

    def user_auth_signup(self):
        """authenticate user"""
        return self.client().post(signup_url, data = user5)

    def user_auth_login(self):
        """authenticate user"""
        return self.client().post(login_url, data = user5_login)

    def admin_auth_login(self):
        """authenticate user"""
        return self.client().post(login_url, data = admin_login)

    def generate_auth_token(self):
        self.user_auth_signup()
        resp = self.user_auth_login()
        auth_token = json.loads(resp.data.decode('UTF-8'))['auth_token']
        return auth_token

    def generate_admin_auth_token(self):
        resp = self.admin_auth_login()
        auth_token = json.loads(resp.data.decode('UTF-8'))['auth_token']
        return auth_token

    def create_incident(self):
        auth_token = self.generate_auth_token()
        create_incident = self.client().post(incident_url, headers=dict(Authorization="{}".format(auth_token)),
        data = incident1)
        """Asserts test return true status_code and message"""
        result = json.loads(create_incident.data)
        # self.assertEqual('Success', result['error'])
        self.assertEqual('Success', result['status'])
        self.assertEqual(create_incident.status_code, 201)
        return result

    def test_create_incident(self):
        """method to test for create incident"""
        auth_token = self.generate_auth_token()
        create_incident = self.client().post(incident_url, \
        headers=dict(Authorization="{}".format(auth_token)),
        data = incident2)
        """Asserts test return true status_code and message"""
        result = json.loads(create_incident.data)
        self.assertEqual('Success', result['status'])
        self.assertEqual(create_incident.status_code, 201)

    def test_get_incidents(self):
        auth_token = self.generate_auth_token()
        self.create_incident()
        """Asserts test return true status_code and message"""
        fetch_incidents = self.client().get(incident_url, headers=dict(Authorization="{}".format(auth_token)))
        result = json.loads(fetch_incidents.data)
        self.assertEqual('Success', result['status'])
        self.assertEqual(fetch_incidents.status_code, 200)
        self.assertNotEqual('Fail', result['status'])
        self.assertNotEqual(fetch_incidents.status_code, 400)

    def test_get_single_incident(self):
        """Asserts test return true status_code and message"""
        auth_token = self.generate_auth_token()
        result = self.create_incident()
        created_incident = self.client().get('{}/{}'.format(incident_url,result['data']['id']), headers=dict(Authorization="{}".format(auth_token)))
        created_incident_result = json.loads(created_incident.data)
        self.assertEqual(created_incident.status_code, 200)
        self.assertEqual("Success",created_incident_result["status"])

    def test_get_incident_not_exist(self):
        """Asserts test return true status_code and message"""
        auth_token = self.generate_auth_token()

        single_incident = self.client().get('{}/184'.format(incident_url), headers=dict(Authorization="{}".format(auth_token)))
        result = json.loads(single_incident.data)
        self.assertEqual(single_incident.status_code, 404)
        self.assertEqual('Fail', result['status'])

    # def test_edit_incident(self):
    #     """Asserts test return true status_code and message"""
    #     auth_token = self.generate_auth_token()
    #     result = self.create_incident()
    #     new_incident = self.client().put('{}/{}'.format(incident_url,result['data']['id']), headers=dict(Authorization="{}".format(auth_token)), data = incident4)
    #     edited_result = json.loads(new_incident.data)
    #     self.assertEqual(new_incident.status_code, 201)
    #     self.assertEqual("Success", edited_result['status'])
    def test_edit_comment(self):
        """Asserts test return true status_code and message"""
        auth_token = self.generate_auth_token()
        result = self.create_incident()
        new_incident = self.client().patch('{}/{}/comment'.format(incident_url,result['data']['id']), headers=dict(Authorization="{}".format(auth_token)), data = edited_comment)
        edited_result = json.loads(new_incident.data)
        self.assertEqual(new_incident.status_code, 201)
        self.assertEqual("Success", edited_result['status'])

    def test_edit_comment_not_exists(self):
        """Asserts test return true status_code and message"""
        auth_token = self.generate_auth_token()
        self.create_incident()
        new_incident = self.client().patch('{}/{}/comment'.format(incident_url,"51d5d8ae-cf62-4f24-a2d6-3c61e21b0e2"), headers=dict(Authorization="{}".format(auth_token)), data = edited_comment)
        edited_result = json.loads(new_incident.data)
        self.assertEqual(new_incident.status_code, 404)
        self.assertEqual("Fail", edited_result['status'])

    def test_edit_location(self):
        """Asserts test return true status_code and message"""
        auth_token = self.generate_auth_token()
        result = self.create_incident()
        new_incident = self.client().patch('{}/{}/location'.format(incident_url,result['data']['id']), headers=dict(Authorization="{}".format(auth_token)), data = edited_location)
        edited_result = json.loads(new_incident.data)
        self.assertEqual(new_incident.status_code, 201)
        self.assertEqual("Success", edited_result['status'])

    def test_edit_location_not_exists(self):
        """Asserts test return true status_code and message"""
        auth_token = self.generate_auth_token()
        self.create_incident()
        new_incident = self.client().patch('{}/{}/location'.format(incident_url,"51d5d8ae-cf62-4f24-a2d6-3c61e21b0e2"), headers=dict(Authorization="{}".format(auth_token)), data = edited_location)
        edited_result = json.loads(new_incident.data)
        self.assertEqual(new_incident.status_code, 404)
        self.assertEqual("Fail", edited_result['status'])

    def test_admin_edit_status(self):
        """Asserts test return true status_code and message"""
        auth_token = self.generate_admin_auth_token()
        result = self.create_incident()
        new_incident = self.client().patch('{}/{}/status'.format(incident_url,result['data']['id']), headers=dict(Authorization="{}".format(auth_token)), data = admin_edited_status)
        edited_result = json.loads(new_incident.data)
        self.assertEqual(new_incident.status_code, 201)
        self.assertEqual("Success", edited_result['status'])

    def test_admin_edit_status_not_exists(self):
        """Asserts test return true status_code and message"""
        auth_token = self.generate_admin_auth_token()
        self.create_incident()
        new_incident = self.client().patch('{}/{}/status'.format(incident_url,"51d5d8ae-cf62-4f24-a2d6-3c61e21b0e2"), headers=dict(Authorization="{}".format(auth_token)), data = admin_edited_status)
        edited_result = json.loads(new_incident.data)
        self.assertEqual(new_incident.status_code, 404)
        self.assertEqual("Fail", edited_result['status'])

    def test_delete_incident(self):
        auth_token = self.generate_auth_token()
        result = self.create_incident()
        delete_incident = self.client().delete('{}/{}'.format(incident_url,result['data']['id']), headers=dict(Authorization="{}".format(auth_token)))
        deleted_result = json.loads(delete_incident.data)
        self.assertEqual(delete_incident.status_code, 200)
        self.assertEqual('Success', deleted_result['status'])
        
    def test_delete_incident_not_exist(self):
        auth_token = self.generate_auth_token()
        delete_incident_not_found = self.client().delete('{}/105'.format(incident_url), headers=dict(Authorization="{}".format(auth_token)))
        deleted_not_found_result = json.loads(delete_incident_not_found.data)
        self.assertEqual(delete_incident_not_found.status_code, 404)
        self.assertEqual('Fail', deleted_not_found_result['status'])

    def test_expired_auth_token(self):
        """method to test for expired auth token"""
        auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEzNmJmZTAyLWMxYTYtNDEzMC1iZjAwLWM3YTcyMDQ3ZGRlZiIsInVzZXIiOiJicmlhbkBnbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImV4cCI6MTU0NDQ0MDk2NX0.nyDLC6IP7GC8zryGCmoogVIrAXBnazvUmcR40mC-wMk"
        create_incident = self.client().post(incident_url, headers=dict(Authorization="{}".format(auth_token)),
        data = incident1)
        """Asserts test return signature expired message"""
        result = json.loads(create_incident.data)
        self.assertEqual('Signature expired. Please log in again.', result['message'])

    def test_invalid_auth_token(self):
        """method to test for expired auth token"""
        auth_token = "eyJ0eXAiOiJKv2QiLCJhbGciOiJIUzI1NiJ9eyJ1c2VyIjoiaXNhYWNAZ21haWwuY29tIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNTQzODYwNzA3fQe9dW-skrMDCCGizrgPOSOjm1i4IjZ781wgIYDvB3KMA"
        create_incident = self.client().post(incident_url, headers=dict(Authorization="{}".format(auth_token)),
        data = incident1)
        """Asserts test return signature expired message"""
        result = json.loads(create_incident.data)
        self.assertEqual('Invalid token. Please log in again.', result['message'])
