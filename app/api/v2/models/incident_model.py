import datetime 
from flask import request
from ..models.user_auth_models import User
import re
import psycopg2
import uuid

"""Incident model class"""
class Incident():
    incident_id = 1
    incidents = []
    
    """ Initializing the constructor"""
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname='ireporter' user='postgres' host='localhost' password='F31+35e9' port='5432'")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

        except:
            print("Cannot connect to database")

    """Method to create a new incident into list"""
    def create_incident(self, type, latitude, longitude, images, videos, comments):
        incident_item = dict(
            type = type,
            latitude = latitude,
            longitude = longitude,
            images = images,
            videos = videos,
            comments = comments
        )  
        is_empty = Incident.check_if_empty(incident_item)  
        if is_empty:
            return is_empty

        is_valid = Incident.validate_data(incident_item)  
        if is_valid:
            return is_valid

        created_by = Incident.get_user_id()

        if created_by == "Authentication required":
            return dict(error = "Authentication required")

        _id = uuid.uuid4()
        _id = str(_id)
        create_incident_query = "INSERT INTO incidents(id, created_on, created_by, type, latitude, longitude, status, images, videos, comment)\
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(create_incident_query, (_id, datetime.datetime.now(), created_by, type, latitude, longitude, "draft", images, videos, comments))

        response_user = dict(
            id = _id,
            message = "Incident created successfully"
        )
        return response_user

    """method to fetch for all incident records"""
    def get_all_incidents (self):
        _id = Incident.get_user_id()
        retrieve_all_incidents_query = "SELECT * FROM incidents WHERE created_by='{}'".format(_id)
        self.cursor.execute(retrieve_all_incidents_query)
        incidents = []
        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                incident = dict(
                    id = row[0],
                    created_on = row[1],
                    created_by = row[2],
                    type = row[3],
                    latitude = row[4],
                    longitude = row[5],
                    status = row[6],
                    images = row[7],
                    videos = row[8],
                    comment = row[9]
                )
                incidents.append(incident)
            return incidents
        else:
            return []

    def get_single_incident(self, incident_id):
        """Method to get a single incident given its id"""
        _id = Incident.get_user_id()
        retrieve_single_incident_id = "SELECT * FROM incidents WHERE created_by='{}' AND id='{}'".format(_id, incident_id)
        self.cursor.execute(retrieve_single_incident_id)
        row = self.cursor.fetchone()
        if row:
            return dict(
                id = row[0],
                created_on = row[1],
                created_by = row[2],
                type = row[3],
                latitude = row[4],
                longitude = row[5],
                status = row[6],
                images = row[7],
                videos = row[8],
                comment = row[9]
            )
        return "Incident not found"

    @staticmethod
    def check_if_empty(incident):
        for key, value in incident.items():
            if value is None or value == "":
                return "Field should not be empty"

    @staticmethod
    def check_if_type(incident_type):
        if incident_type == "intervention":
            return True
        elif incident_type == "red flag":
            return True
        else:
            return False

    @staticmethod
    def check_if_status(status):
        if status == "draft":
            return True
        elif status == "under investigation":
            return True
        elif status == "resolved":
            return True
        elif status == "rejected":
            return True
        else:
            return False

    @staticmethod
    def validate_data(incident):

        error_response = {}
        error = False

        for key, value in incident.items():
            if key == 'type' and not Incident.check_if_type(value):
                error = True
                error_response[key] = "Type should be intervention or red flag"
            if (key == 'latitude' or key == 'longitude') and not re.match(r"^\d+?\.\d+?$", value):
                error = True
                error_response[key] = "Latitude and longitude should be a float number"
            if key == 'images'and not re.match(r"([a-zA-Z0-9\s_\\.\-\(\):])+(.jpg|.png|.jpeg|.gif)$", value):
                error = True
                error_response[key] = "Invalid image format"
            if key == 'videos'and not re.match(r"([a-zA-Z0-9\s_\\.\-\(\):])+(.mp4|.mov|.mkv)$", value):
                error = True
                error_response[key] = "Invalid video format"
            if key == 'comments' and not re.match(r"^[a-z\d\-_\s,.;:\"']+$", value):
                error = True
                error_response[key] = "Comments should be alphanumeric"

        if error:
            print ("ERROR : {}" .format(error_response))
            error_message = dict( error = error_response )
            return error_message

    @staticmethod
    def get_user_id():
        token = None
        content = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            content = User.decode_auth_token(token)

        _id = content['id']

        if _id:
            return _id

        else:
            return "Authentication required"