import json
from app.tests.v1.base_test import BaseTest

incident_url = "/api/v1/incidents"
signup_url = "/api/v1/auth/signup"
reg_url = 'api/v1/auth/signup'
login_url = 'api/v1/auth/login'

class TestIncidents(BaseTest):
    incidents_data = {
        "created_on": "2018-11-28T08:09:57.562Z",
        "created_by": "454",
        "type":"red flag",
        "latitude": 25.252,
        "longitude": 2.456,
        "status": "draft",
        "images": [
            "image1","image2"
        ],
        "videos": [
            "video1","video2"
        ],
        "comments": "the police asked for a bribe"
    }

    edited_incident = {
        "created_on": "2018-11-28T08:09:57.562Z",
        "created_by": "746",
        "type":"intervention",
        "latitude": 25.252,
        "longitude": 2.456,
        "status": "under investigation",
        "images": [
            "image1","image2"
        ],
        "videos": [
            "video1","video2"
        ],
        "comments": "kahawa west road needs maintenance"
    }

    another_incident = {
        "created_on": "2018-11-28T08:09:57.562Z",
        "created_by": "746",
        "type":"red flag",
        "latitude": 25.252,
        "longitude": 2.456,
        "status": "resolved",
        "images": [
            "image1","image2"
        ],
        "videos": [
            "video1","video2"
        ],
        "comments": "the chief wanted more money"
    }

    def user_auth_signup(self, first_name = "isaac", last_name = "wangethi", email = "isaac@gmail.com", phone = "0748567845", username = "isaac", password = "F31+25e9", role = "admin", registered_on = "2018-11-29T19:20:39.957Z"):
        """authenticate user"""
        signup_data = {
            'first_name':first_name,
            'last_name':last_name,
            'email':email,
            'phone':phone,
            'username':username,
            'password': password,
            'role':role,
            'registered_on': registered_on
        }
        return self.client().post(reg_url, data = signup_data)

    def user_auth_login(self, email="isaac@gmail.com", password="F31+25e9"):
        """authenticate user"""
        login_data = {
            'email': email,
            'password': password
        }
        return self.client().post(login_url, data = login_data)

    def create_incident(self, incidents_data):

        auth_token = self.generate_auth_token()

        create_incident = self.client().post(incident_url, headers=dict(Authorization="Bearer {}".format(auth_token)),
        data = self.incidents_data)
        """Asserts test return true status_code and message"""
        result = json.loads(create_incident.data)
        self.assertEqual('Incident created successfully', result['message'])
        self.assertEqual(create_incident.status_code, 201)
        
        return result

    def generate_auth_token(self):
        self.user_auth_signup()
        resp = self.user_auth_login()

        auth_token = json.loads(resp.data.decode('UTF-8'))['auth_token']

        return auth_token

    def test_create_incident(self):
        """method to test for create incident"""
        with self.client():
            auth_token = self.generate_auth_token()

            create_incident = self.client().post(incident_url, headers=dict(Authorization="Bearer {}".format(auth_token)),
            data = self.incidents_data)
            """Asserts test return true status_code and message"""
            result = json.loads(create_incident.data)
            self.assertEqual('Incident created successfully', result['message'])
            self.assertEqual(create_incident.status_code, 201)

    def test_get_incidents(self):
        auth_token = self.generate_auth_token()
        self.create_incident(TestIncidents.incidents_data)

        """Asserts test return true status_code and message"""
        fetch_incidents = self.client().get(incident_url, headers=dict(Authorization="Bearer {}".format(auth_token)))
        self.assertEqual(fetch_incidents.status_code, 200)

    def test_get_single_incident(self):
        """Asserts test return true status_code and message"""
        auth_token = self.generate_auth_token()
        result = self.create_incident(TestIncidents.incidents_data)

        created_incident = self.client().get('/api/v1/incidents/{}'.format(result['data']['incident_id']), headers=dict(Authorization="Bearer {}".format(auth_token)))
        created_incident_result = json.loads(created_incident.data)
        self.assertEqual(created_incident.status_code, 200)
        self.assertEqual(self.incidents_data["comments"],created_incident_result["data"]['comments'])

    def test_get_incident_not_exist(self):
        """Asserts test return true status_code and message"""
        auth_token = self.generate_auth_token()

        single_incident = self.client().get('/api/v1/incidents/184', headers=dict(Authorization="Bearer {}".format(auth_token)))
        result = json.loads(single_incident.data)
        self.assertEqual(single_incident.status_code, 200)
        self.assertEqual('incident not found', result['data'])

    def test_edit_incident(self):
        """Asserts test return true status_code and message"""
        auth_token = self.generate_auth_token()
        result = self.create_incident(TestIncidents.incidents_data)

        new_incident = self.client().put('/api/v1/incidents/{}'.format(result['data']['incident_id']), headers=dict(Authorization="Bearer {}".format(auth_token)), data = TestIncidents.edited_incident)
        edited_result = json.loads(new_incident.data)
        self.assertEqual(new_incident.status_code, 201)
        self.assertEqual(self.edited_incident['comments'], edited_result['data']['comments'])

    def test_edit_incident_not_exist(self):
        auth_token = self.generate_auth_token()

        new_incident = self.client().put('/api/v1/incidents/123', headers=dict(Authorization="Bearer {}".format(auth_token)), data = TestIncidents.edited_incident)
        edited_result = json.loads(new_incident.data)
        self.assertEqual(new_incident.status_code, 201)
        self.assertEqual('incident not found', edited_result['data'])


    def test_delete_incident(self):
        auth_token = self.generate_auth_token()
        self.create_incident(TestIncidents.incidents_data)
        self.create_incident(TestIncidents.edited_incident)
        self.create_incident(TestIncidents.another_incident)

        delete_incident = self.client().delete('/api/v1/incidents/1', headers=dict(Authorization="Bearer {}".format(auth_token)))
        deleted_result = json.loads(delete_incident.data)
        self.assertEqual(delete_incident.status_code, 200)
        self.assertEqual('deleted', deleted_result['data'])
        
        
    def test_delete_incident_not_exist(self):
        auth_token = self.generate_auth_token()
    
        delete_incident_not_found = self.client().delete('/api/v1/incidents/105', headers=dict(Authorization="Bearer {}".format(auth_token)))
        deleted_not_found_result = json.loads(delete_incident_not_found.data)
        self.assertEqual(delete_incident_not_found.status_code, 200)
        self.assertEqual('incident not found', deleted_not_found_result['data'])
