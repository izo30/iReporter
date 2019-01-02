import json
from tests.v2.base_test import BaseTest
from tests.v2.test_data import signup_url, login_url, incident_url, user5,\
 user5_login, admin_login, incident1, incident2, incident3, incident4, incident5,\
 admin_edited_status, edited_comment, edited_location

class TestIncidents(BaseTest):

    def generate_auth_token(self):
        resp = self.client().post(login_url, data =user5_login)
        auth_token = json.loads(resp.data.decode('UTF-8'))['auth_token']
        return auth_token

    def generate_admin_auth_token(self):
        resp = self.client().post(login_url, data = admin_login)
        auth_token = json.loads(resp.data.decode('UTF-8'))['auth_token']
        return auth_token

    def create_incident(self, incident):
        user_auth_token = self.generate_auth_token()
        create_incident = self.client().post(
            incident_url, 
            headers=dict(Authorization="{}".format(user_auth_token)),
            data = incident)
        """Asserts test return true status_code and message"""
        result = json.loads(create_incident.data)
        return result

    def test_create_incident(self):
        user_auth_token = self.generate_auth_token()
        create_incident = self.client().post(
            incident_url, 
            headers=dict(Authorization="{}".format(user_auth_token)),
            data = incident1)
        """Asserts test return true status_code and message"""
        result = json.loads(create_incident.data)
        self.assertEqual('Success', result['status'])
        self.assertEqual(create_incident.status_code, 201)

    def test_get_incidents(self):
        user_auth_token = self.generate_auth_token()
        """Asserts test return true status_code and message"""
        fetch_incidents = self.client().get(
            incident_url, 
            headers = dict(Authorization = "{}".format(user_auth_token)))
        result = json.loads(fetch_incidents.data)
        self.assertEqual('Success', result['status'])
        self.assertEqual(fetch_incidents.status_code, 200)

    def test_get_single_incident(self):
        """Asserts test return true status_code and message"""
        user_auth_token = self.generate_auth_token()
        result = self.create_incident(incident1)
        created_incident = self.client().get(
            '{}/{}'.format(incident_url,
            result['data']['id']), 
            headers=dict(Authorization = "{}".format(user_auth_token)))
        created_incident_result = json.loads(created_incident.data)
        self.assertEqual(created_incident.status_code, 200)
        self.assertEqual("Success",created_incident_result["status"])

    def test_get_incident_not_exist(self):
        """Asserts test return true status_code and message"""
        user_auth_token = self.generate_auth_token()
        single_incident = self.client().get(
            '{}/184'.format(incident_url), 
            headers=dict(Authorization = "{}".format(user_auth_token)))
        result = json.loads(single_incident.data)
        self.assertEqual(single_incident.status_code, 404)
        self.assertEqual('Fail', result['status'])

    def test_edit_comment(self):
        """Asserts test return true status_code and message"""
        user_auth_token = self.generate_auth_token()
        result = self.create_incident(incident2)
        new_incident = self.client().patch(
            '{}/{}/comment'.format(incident_url,result['data']['id']), 
            headers = dict(Authorization = "{}".format(user_auth_token)), 
            data = edited_comment)
        edited_result = json.loads(new_incident.data)
        self.assertEqual(new_incident.status_code, 201)
        self.assertEqual("Success", edited_result['status'])

    def test_edit_comment_not_exists(self):
        """Asserts test return true status_code and message"""
        user_auth_token = self.generate_auth_token()
        incident = self.client().patch(
            '{}/{}/comment'.format(incident_url,"51d5d8ae-cf62-4f24-a2d6-3c61e21b0e2"), 
            headers=dict(Authorization = "{}".format(user_auth_token)), 
            data = edited_comment)
        edited_result = json.loads(incident.data)
        self.assertEqual(incident.status_code, 404)
        self.assertEqual("Fail", edited_result['status'])

    def test_edit_location(self):
        """Asserts test return true status_code and message"""
        user_auth_token = self.generate_auth_token()
        result = self.create_incident(incident3)
        new_incident = self.client().patch(
            '{}/{}/location'.format(incident_url,result['data']['id']), 
            headers = dict(Authorization = "{}".format(user_auth_token)), 
            data = edited_location)
        edited_result = json.loads(new_incident.data)
        self.assertEqual(new_incident.status_code, 201)
        self.assertEqual("Success", edited_result['status'])

    def test_edit_location_not_exists(self):
        """Asserts test return true status_code and message"""
        user_auth_token = self.generate_auth_token()
        incident = self.client().patch(
            '{}/{}/location'.format(incident_url, "51d5d8ae-cf62-4f24-a2d6-3c61e21b0e2"), 
            headers = dict(Authorization = "{}".format(user_auth_token)), 
            data = edited_location)
        edited_result = json.loads(incident.data)
        self.assertEqual(incident.status_code, 404)
        self.assertEqual("Fail", edited_result['status'])

    def test_admin_edit_status(self):
        """Asserts test return true status_code and message"""
        admin_auth_token = self.generate_admin_auth_token()
        result = self.create_incident(incident4)
        new_incident = self.client().patch(
            '{}/{}/status'.format(incident_url, result['data']['id']), 
            headers = dict(Authorization = "{}".format(admin_auth_token)), 
            data = admin_edited_status)
        edited_result = json.loads(new_incident.data)
        self.assertEqual(new_incident.status_code, 201)
        self.assertEqual("Success", edited_result['status'])

    def test_admin_edit_status_not_exists(self):
        """Asserts test return true status_code and message"""
        admin_auth_token = self.generate_admin_auth_token()
        incident = self.client().patch(
            '{}/{}/status'.format(incident_url, "51d5d8ae-cf62-4f24-a2d6-3c61e21b0e2"), 
            headers=dict(Authorization="{}".format(admin_auth_token)), 
            data = admin_edited_status)
        edited_result = json.loads(incident.data)
        self.assertEqual(incident.status_code, 404)
        self.assertEqual("Fail", edited_result['status'])

    def test_delete_incident(self):
        user_auth_token = self.generate_auth_token()
        result = self.create_incident(incident5)
        delete_incident = self.client().delete(
            '{}/{}'.format(incident_url, result['data']['id']), 
            headers = dict(Authorization = "{}".format(user_auth_token)))
        deleted_result = json.loads(delete_incident.data)
        self.assertEqual(delete_incident.status_code, 200)
        self.assertEqual('Success', deleted_result['status'])

    def test_delete_incident_not_exist(self):
        user_auth_token = self.generate_auth_token()
        delete_incident_not_found = self.client().delete(
            '{}/51d5d8ae-cf62-4f24-a2d6-3c61e21b0e2'.format(incident_url), 
            headers = dict(Authorization = "{}".format(user_auth_token)))
        deleted_not_found_result = json.loads(delete_incident_not_found.data)
        self.assertEqual(delete_incident_not_found.status_code, 404)
        self.assertEqual('Fail', deleted_not_found_result['status'])

