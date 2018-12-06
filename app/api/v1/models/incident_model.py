import datetime 
from flask import request
from app.api.v1.models.user_auth_models import User
import re

"""Incident model class"""
class Incident():
    incident_id = 1
    incidents = []
    
    """ Initializing the constructor"""
    def __init__(self, created_by, type, latitude, longitude, images, videos, comments):
        self.incident_id = len(Incident.incidents) + 1
        self.created_on = datetime.datetime.now()
        self.created_by = created_by
        self.type = type
        self.latitude = latitude
        self.longitude = longitude
        self.status = "draft"
        self.images = images
        self.videos = videos
        self.comments = comments

    """Method to create a new incident into list"""
    def create_incident(self):
        incident_item = dict(
            incident_id = self.incident_id,
            created_on = self.created_on,
            created_by = self.created_by,
            type = self.type,
            latitude = self.latitude,
            longitude = self.longitude,
            status = self.status,
            images = self.images,
            videos = self.videos,
            comments = self.comments
        )  
        is_empty = Incident.check_if_empty(incident_item)  
        if is_empty:
            return is_empty

        is_valid = Incident.validate_data(incident_item)  
        if is_valid:
            return is_valid

        self.incidents.append(incident_item)
        return incident_item

    """method to fetch for all incident records"""
    def get_all_incidents (self):
        return Incident.incidents

    def get_incident(self, incident_id):
        """Method to get a single incident given its id"""
        incident_item = [incident for incident in Incident.incidents if incident['incident_id'] == incident_id]
        if incident_item:
            return incident_item[0]
        return "Incident not found"

    def edit_incident(self, incident_id):
        """Method to edit an existing incident"""
        edited_incident_item = dict(
            incident_id = incident_id,
            created_on = self.created_on,
            created_by = self.created_by,
            type = self.type,
            latitude = self.latitude,
            longitude = self.longitude,
            status = self.status,
            images = self.images,
            videos = self.videos,
            comments = self.comments
        ) 

        is_empty = Incident.check_if_empty(edited_incident_item)  
        if is_empty:
            return is_empty

        is_valid = Incident.validate_data(edited_incident_item)
        if is_valid:
            return is_valid

        """edit the incident"""
        for number, incident in enumerate(Incident.incidents):
            if incident['incident_id'] == incident_id:
                if incident['status'] == 'draft':
                    Incident.incidents[number] = edited_incident_item
                    return edited_incident_item
                else:
                    return {'message':'incident status has changed'}
        return 'Incident not found'

    @staticmethod
    def admin_edit_incident(incident_id, status):
        if status.strip() is None or status.strip() == "":
            return "Field should not be empty"
        if not Incident.check_if_status(status.strip()):
            return dict (error = "Status should be either draft, under investigation, \
            resolved or rejected")
        """edit the incident"""
        for number, incident in enumerate(Incident.incidents):
            if incident['incident_id'] == incident_id:
                incident['status'] = status.strip()
                return 'Incident status edited'
        return 'Incident not found'

    def delete_incident(self, incident_id):
        """delete the incident"""
        for number, incident in enumerate(Incident.incidents):
            if incident['incident_id'] == incident_id:
                if incident['status'] == 'draft':
                    del Incident.incidents[number]
                    return 'Deleted'
                else: 
                    return 'Incident status has changed'
        return 'Incident not found'

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
            if key == 'created_by' and not value.isalnum():
                error = True
                error_response[key] = "Created by should be alphanumeric"
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