"""
This will contain the configuration to be reused in all tests.
"""
# Library imports 
from unittest import TestCase
from app import create_app

class BaseTest(TestCase):
    """
    Class to hold all similar test config
    """
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()