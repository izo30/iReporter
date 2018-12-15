from flask_restplus import reqparse, Api, Namespace, fields
from app.api.v2.utils.validations import Validations

user_api = Namespace('User Endpoints', description='A collection of user endpoints')

class UserFields():
    @staticmethod
    def required_signup_fields():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['first_name','last_name','email','phone','username','password','role'])
        return parser

    @staticmethod
    def required_login_fields():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['email','password'])
        return parser

    signup_fields = user_api.model('Signup', {
        'first_name' : fields.String,
        'last_name' : fields.String,
        'email': fields.String,
        'phone' : fields.String,
        'username' : fields.String,
        'password': fields.String,
        'role': fields.String
    })

    login_fields = user_api.model('Login', {
        'email': fields.String,
        'password': fields.String
    })

incidents_api = Namespace('Incident Endpoints', description='A collection of endpoints for the incident model; includes get, post, put and delete endpoints')

class IncidentFields():
    @staticmethod
    def required_incident_fields():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['type','latitude','longitude','images','videos','comments'])
        return parser

    @staticmethod
    def required_edit_incident_fields():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['latitude','longitude','images','videos','comments'])
        return parser

    @staticmethod
    def admin_status_field():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['status'])
        return parser

    @staticmethod
    def edit_location_fields():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['latitude','longitude'])
        return parser

    @staticmethod
    def edit_comments_fields():
        parser = reqparse.RequestParser()
        Validations().add_arguments(parser, ['comments'])
        return parser

    incident_fields = incidents_api.model('Incident', {
        'type': fields.String,
        'latitude': fields.String,
        'longitude': fields.String,
        'images': fields.List(fields.String),
        'videos': fields.List(fields.String),
        'comments': fields.String
    })

    edit_incident_fields = incidents_api.model('Edit Incident', {
        'latitude': fields.String,
        'longitude': fields.String,
        'images': fields.List(fields.String),
        'videos': fields.List(fields.String),
        'comments': fields.String
    })

    status_field = incidents_api.model('Status', {
        'status': fields.String
    })

    location_fields = incidents_api.model('Location', {
        'latitude': fields.String,
        'longitude': fields.String
    })

    comments_fields = incidents_api.model('Comments', {
        'comments': fields.String
    })