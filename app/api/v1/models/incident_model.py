"""Incident model class"""
class Incident():
    incident_id = 1
    incidents = []
    
    """ Initializing the constructor"""
    def __init__(self, created_on, created_by, type, latitude, longitude, status, images, videos, comments):
        self.incident_id = len(Incident.incidents) + 1
        self.created_on = created_on
        self.created_by = created_by
        self.type = type
        self.latitude = latitude
        self.longitude = longitude
        self.status = status
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
        return 'incident not found'

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
        """edit the incident"""
        for number, incident in enumerate(Incident.incidents):
            if incident['incident_id'] == incident_id:
                if incident['status'] == 'draft':
                    Incident.incidents[number] = edited_incident_item
                    return edited_incident_item
                else:
                    return {'message':'incident status has changed'}
        return 'incident not found'

    def delete_incident(self, incident_id):
        """delete the incident"""
        for number, incident in enumerate(Incident.incidents):
            if incident['incident_id'] == incident_id:
                if incident['status'] == 'draft':
                    del Incident.incidents[number]
                    return 'deleted'
                else: 
                    return 'incident status has changed'
        return 'incident not found'