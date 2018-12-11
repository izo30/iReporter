"""
This will contain the configuration to be reused in all tests.
"""
# Library imports 
from unittest import TestCase
from app import create_app
import os
from app.instance.db_config import DbSetup
import uuid
from passlib.hash import pbkdf2_sha256 as sha256

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
        DbSetup().drop_tables()

    user1 = dict(
        first_name = 'triza',
        last_name = 'wambui',
        email = 'triza@gmail.com',
        phone = '0736547657', 
        username = 'triza',
        password = 'F31+25e9',
        role = 'user'
    )

    user2 = dict(
        first_name = 'mercy',
        last_name = 'wanjiru',
        email = 'mercy@gmail.com',
        phone = '0736547657', 
        username = 'mercy',
        password = 'F31+25e9',
        role = 'user'
    )

    incident1 = dict(
        type = 'intervention',
        latitude = '4.58',
        longitude = '9.45',
        images = 'image.jpg',
        videos = 'video.jpg',
        comments = 'government offices around kahawa area need renovation'
    ) 

    incident2 = dict(
        type = 'red flag',
        latitude = '8.58',
        longitude = '12.45',
        images = 'image.jpg',
        videos = 'video.jpg',
        comments = 'huduma center officer demanded for an extra fee to provide services'
    )

    incident3 = dict(
        type = 'red flag',
        latitude = '6.58',
        longitude = '9.45',
        images = 'image.jpg',
        videos = 'video.jpg',
        comments = 'the police was given a bribe by the matatu conductor'
    )

    incident4 = dict(
        type = 'intervention',
        latitude = '6.58',
        longitude = '9.45',
        images = 'image.jpg',
        videos = 'video.jpg',
        comments = 'kahawa west road needs maintenance'
    ) 

    test_users = [user1, user2]
    test_incidents = [incident1, incident2, incident3, incident4]

    @staticmethod
    def create_test_users(test_users):
        for user in test_users:
            try:
                connection = psycopg2.connect(
                    "dbname='{}' user='postgres' host='localhost' password='F31+35e9' port='5432'".format(os.environ['DB']))
                connection.autocommit = True
                cursor = connection.cursor()

                _id = uuid.uuid4()
                _id = str(_id)
                hashed_password = BaseTest.generate_hash(user['password'])
                create_user_query = "INSERT INTO users(id, first_name, last_name, email, phone, username, password, role,\
                    registered_on)\
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(create_user_query, (_id, user['first_name'], user['last_name'], user['email'], user['phone'],\
                user['username'], hashed_password, user['role'], datetime.now()))

            except:
                print("Cannot connect to database")

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
