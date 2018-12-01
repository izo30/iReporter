import json
from app.tests.v1.base_test import BaseTest

incident_url = "/api/v1/incidents"
signup_url = "/api/v1/auth/signup"

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
            'email':email,
            'password': password
        }
        return self.client().post(login_url, data = login_data)

    def test_create_incident(self):
        """method to test for create incident"""
        with self.client():
            self.user_auth_signup()
            resp = self.user_auth_login()

            auth_token = json.loads(resp.data.decode())['auth_token']

            create_incident = self.client().post(incident_url, headers=dict(Authorization="Bearer {}".format(auth_token)),
            data = self.incidents_data)
            """Asserts test return true status_code and message"""
            result = json.loads(post_sale.data)
            self.assertEqual('Incident created successfully', result['message'])
            self.assertEqual(create_incident.status_code, 201)

    def test_get_incidents(self):
        with self.client():
            resp = self.user_auth_login()

            auth_token = json.loads(resp.data.decode())['auth_token']

            create_incident = self.client().post(incident_url, headers=dict(Authorization="Bearer {}".format(auth_token)),
            data = self.incidents_data)
            """Asserts test return true status_code and message"""
            result = json.loads(post_sale.data)
            self.assertEqual('Incident created successfully', result['message'])
            self.assertEqual(post_sale.status_code, 201)

            """Asserts test return true status_code and message"""
            fetch_incidents = self.client().get(incident_url)
            self.assertEqual(fetch_incidents.status_code, 200)

    def test_get_single_incident(self):
        """Asserts test return true status_code and message"""
        with self.client():
            self.user_auth_signup()
            resp = self.user_auth_login()

            auth_token = json.loads(resp.data.decode())['auth_token']

            create_incident = self.client().post(incident_url, headers=dict(Authorization="Bearer {}".format(auth_token)),
            data = self.sales_data)
            """Asserts test return true status_code and message"""
            result = json.loads(create_incident.data)
            self.assertEqual('Incident created successfully', result['message'])
            self.assertEqual(create_incident.status_code, 201)

            single_incident = self.client().get(
                '/api/v1/incidents/{}'.format(result['incidents']['incident_id']))
            self.assertEqual(single_incident.status_code, 200)