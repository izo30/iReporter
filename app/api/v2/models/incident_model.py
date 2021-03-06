import datetime 
from flask import request
from app.api.v2.models.user_auth_models import User
from app.api.v2.utils.auth import AuthToken
import re
import psycopg2
import uuid
import os
from instance.db_config import DbSetup

"""Incident model class"""
class Incident(DbSetup):
    """ Initializing the constructor"""
    def __init__(self):
        super().__init__()

    """Method to create a new incident into list"""
    def create_incident(self, type, latitude, longitude, images, videos, comments):
        _id = self.generate_unique_id()
        created_by = AuthToken().get_user_id()
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
        created_by = AuthToken().get_user_id()
        retrieve_all_incidents_query = "SELECT * FROM incidents WHERE created_by='{}'".format(created_by)
        self.cursor.execute(retrieve_all_incidents_query)
        rows = self.cursor.fetchall()
        if rows:
            incidents = []
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
        _id = AuthToken().get_user_id()
        retrieve_single_incident_query = "SELECT * FROM incidents WHERE created_by='{}' AND id='{}'".format(_id, incident_id)
        self.cursor.execute(retrieve_single_incident_query)
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

    def edit_incident_location(self, incident_id, latitude, longitude):
        """Method to edit an existing incident"""
        created_by = AuthToken().get_user_id()
        if self.check_user_incident_exists(incident_id, created_by):
            edit_incident_query = "UPDATE incidents SET latitude='{}', longitude='{}' WHERE created_by='{}' AND id='{}'".format(latitude, longitude, created_by, incident_id)
            self.cursor.execute(edit_incident_query)
            response = dict(
                edited_incident = self.get_single_incident(incident_id),
                message = "Incident location updated successfully"
            )
            return response

    def edit_incident_comment(self, incident_id, comment):
        """Method to edit an existing incident"""
        created_by = AuthToken().get_user_id()
        if self.check_user_incident_exists(incident_id, created_by):
            edit_incident_query = "UPDATE incidents SET comment='{}' WHERE created_by='{}' AND id='{}'".format(comment, created_by, incident_id)
            self.cursor.execute(edit_incident_query)
            response = dict(
                edited_incident = self.get_single_incident(incident_id),
                message = "Incident comment updated successfully"
            )
            return response

    def delete_incident(self, incident_id):
        """delete the incident"""
        created_by = AuthToken().get_user_id()
        if self.check_user_incident_exists(incident_id, created_by):
            delete_incident_query = "DELETE FROM incidents WHERE id='{}'".format(incident_id)
            self.cursor.execute(delete_incident_query)
            return "Incident deleted"

    def admin_edit_incident_status(self, incident_id, status):
        """delete the incident"""    
        if self.check_incident_exists(incident_id):
            edit_incident_status_query = "UPDATE incidents SET status='{}' WHERE id='{}'".format(status, incident_id)
            self.cursor.execute(edit_incident_status_query)
            return "Status edited successfully"

    def check_incident_exists(self, incident_id):
        check_incident_exists_query = "SELECT * FROM incidents WHERE id='{}'".format(incident_id)
        self.cursor.execute(check_incident_exists_query)
        row = self.cursor.fetchone()
        if row:
            return True

    def check_user_incident_exists(self, incident_id, created_by):
        check_incident_exists_query = "SELECT * FROM incidents WHERE id='{}' AND created_by='{}'".format(incident_id, created_by)
        self.cursor.execute(check_incident_exists_query)
        row = self.cursor.fetchone()
        if row:
            return True

    def check_can_delete(self, incident_id, created_by):
        check_incident_exists_query = "SELECT * FROM incidents WHERE id='{}' AND created_by='{}' AND status='draft'".format(incident_id, created_by)
        self.cursor.execute(check_incident_exists_query)
        row = self.cursor.fetchone()
        if row:
            return True

    def generate_unique_id(self):
        _id = uuid.uuid4()
        return str(_id)
