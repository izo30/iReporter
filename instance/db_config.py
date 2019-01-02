import psycopg2
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import datetime
import uuid
import os
from flask import current_app

class DbSetup():

    def __init__(self, app=None):
        self.app = app
        current_context = self.context_switcher()
        self.db_name = current_context.config['DB_NAME']
        self.db_user = current_context.config['DB_USERNAME']
        self.db_password = current_context.config['DB_PASSWORD']
        self.db_host = current_context.config['DB_HOST']
        self.connection = psycopg2.connect(
            database=self.db_name, 
            user=self.db_user,
            password=self.db_password,
            host=self.db_host
        )
        self.connection.autocommit = True
        print("DB URL : {}{}{}{}" .format(self.db_name, self.db_user, self.db_password, self.db_host))
        try:
            self.cursor = self.connection.cursor()
            print("CONNECTION_SUCCESS!!")
        except:
            print("CONNECTION_ERROR!!")

    def context_switcher(self):
        """get current passed context to the dbModel"""
        if current_app:
            return current_app
        else:
            return self.app

    def create_users_table(self):
        create_table_command = """CREATE TABLE IF NOT EXISTS users(
            id VARCHAR(50) PRIMARY KEY,
            first_name VARCHAR(25) NOT NULL,
            last_name VARCHAR(25) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone INTEGER,
            username VARCHAR(25) NOT NULL,
            password VARCHAR(256) NOT NULL,
            role VARCHAR(5) NOT NULL,
            registered_on VARCHAR(50));"""
        self.cursor.execute(create_table_command)

    def create_incidents_table(self):
        create_table_command = """CREATE TABLE IF NOT EXISTS incidents (
            id VARCHAR(50) PRIMARY KEY,
            created_on VARCHAR(50),
            created_by VARCHAR(50) REFERENCES users(id),
            type VARCHAR NOT NULL,
            latitude VARCHAR,
            longitude VARCHAR,
            status VARCHAR DEFAULT 'draft',
            images VARCHAR,
            videos VARCHAR,
            comment VARCHAR(500) NOT NULL);"""
        self.cursor.execute(create_table_command)

    def create_default_admin(self):
        hashed_password = DbSetup.generate_hash('F31+25e9')

        query = "SELECT * FROM users WHERE email=%s"
        self.cursor.execute(query, ('isaacwangethi30@gmail.com',))
        admin = self.cursor.fetchone()

        if not admin:
            _id = uuid.uuid4()
            _id = str(_id)
            create_admin_query = "INSERT INTO users(id, first_name, last_name, email, phone, username, password, role,\
             registered_on)\
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(create_admin_query, (_id, 'Isaac', 'Wangethi', 'isaacwangethi30@gmail.com', '0785768576',\
            'isaacwangethi30', hashed_password, 'admin', datetime.now()))

    def create_default_test_user(self):
        hashed_password = DbSetup.generate_hash('F31+25e9')

        query = "SELECT * FROM users WHERE email=%s"
        self.cursor.execute(query, ('hamani@gmail.com',))
        user = self.cursor.fetchone()

        if not user:
            _id = uuid.uuid4()
            _id = str(_id)
            create_user_query = "INSERT INTO users(id, first_name, last_name, email, phone, username, password, role,\
             registered_on)\
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(create_user_query, (_id, 'hamani', 'grain', 'hamani@gmail.com', '0736547657',\
            'hamani', hashed_password, 'user', datetime.now()))

    def drop_tables(self):
        drop_users_command = "DROP TABLE IF EXISTS users CASCADE;"
        self.cursor.execute(drop_users_command)

        drop_incidents_command = "DROP TABLE IF EXISTS incidents CASCADE;"
        self.cursor.execute(drop_incidents_command)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)