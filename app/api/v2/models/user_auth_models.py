from flask import jsonify
from app.api.v2.utils.encryption import Encryption
from app.api.v2.utils.auth import AuthToken
from instance.config import secret_key
from datetime import datetime, timedelta
import jwt
import re
import psycopg2
import uuid
import os

class User():
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname='{}' user='postgres' host='localhost' password='F31+35e9' port='5432'".format(os.environ['DB']))
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

        except:
            print("Cannot connect to database")

    def create_user(self, first_name, last_name, email, phone, username, password, role):
        user = dict(
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone = phone, 
            username = username,
            password = password,
            role = role
        )

        query = "SELECT * FROM users WHERE email='{}'" .format(email)
        self.cursor.execute(query)
        user = self.cursor.fetchone()

        if not user:
            _id = uuid.uuid4()
            _id = str(_id)
            create_user_query = "INSERT INTO users(id, first_name, last_name, email, phone, username, password, role,\
             registered_on)\
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(create_user_query, (_id, first_name, last_name, email, phone, username, password, role, datetime.now()))

            response_user = dict(
                id = _id,
                first_name = first_name,
                last_name = last_name,
                username = username,
                role = role
            )
            return response_user
        else:
            return False

    def get_single_user(self, email, password):
        query = "SELECT * FROM users WHERE email='{}'" .format(email)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        if user:
            return dict(
                hash = user[6],
                id = user[0],
                email = user[3],
                role = user[7]
            )
        else:
            return False

    def get_cursor(self):
        try:
            connection = psycopg2.connect(
                "dbname='ireporter' user='postgres' host='localhost' password='F31+35e9' port='5432'")
            connection.autocommit = True
            cursor = connection.cursor()
            return cursor
        except:
            return "Cannot connect to database"
