"""Incident model class"""
class Incident():
    incident_id = 1
    incidents = []
    
    """ Initializing the constructor"""
    def __init__(self, created_on, created_by, type, latitude, longitude, status, images, videos, comments):
        Incident.incident_id = len(Incident.incidents) + 1
        self.created_on = created_on
        self.created_by = created_by
        self.type = type
        self.latitude = latitude
        self.longitude = longitude
        self.status = status
        self.images = images
        self.videos = videos
        self.comments = comments

    def create_incident(self):
        """Method to create a new incident into list"""
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
        self.incidents.append(incident_item)
        return incident_item