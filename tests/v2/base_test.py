"""
This will contain the configuration to be reused in all tests.
"""
# Library imports 
from unittest import TestCase
from app import create_app
import os
from instance.db_config import DbSetup
from tests.v2.test_data import login_url, user5_login, admin_login
import json
from app.api.v2.utils.auth import AuthToken
import json

class BaseTest(TestCase):
    """
    Class to hold all similar test config
    """
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

        DbSetup().create_users_table()
        DbSetup().create_incidents_table()
        DbSetup().create_default_admin()
        DbSetup().create_default_test_user()

    def tearDown(self):
        DbSetup().drop_tables()
        self.app_context.pop()
