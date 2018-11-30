
from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.incident_model import Incident
from ..models.user_auth_models import User

api = Namespace('Incident Endpoints', description='A collection of endpoints for the incident model; includes get, post, put and delete endpoints')

parser = reqparse.RequestParser()
parser.add_argument('created_on', help = 'This field cannot be blank', required = True)
parser.add_argument('created_by', help = 'This field cannot be blank', required = True)
parser.add_argument('type', help = 'This field cannot be blank', required = True)
parser.add_argument('latitude', help = 'This field cannot be blank', required = True)
parser.add_argument('longitude', help = 'This field cannot be blank', required = True)
parser.add_argument('status', help = 'This field cannot be blank', required = True)
parser.add_argument('images', help = 'This field cannot be blank', required = True)
parser.add_argument('videos', help = 'This field cannot be blank', required = True)
parser.add_argument('comments', help = 'This field cannot be blank', required = True)

incident_fields = api.model('Incident', {
    'created_on' : fields.DateTime,
    'created_by': fields.String,
    'type': fields.String,
    'latitude': fields.String,
    'longitude': fields.String,
    'status': fields.String,
    'images': fields.List,
    'videos': fields.List,
    'comments': fields.String
})
@api.route('')
class IncidentEndpoint(Resource):
    @api.expect(incident_fields)
    def post(self):
        """ Create a new incident """
        args = parser.parse_args()
        created_on = args['created_on']
        created_by = args['created_by']
        _type = args['type']
        latitude = args['latitude']
        longitude = args['longitude']
        status = args['status']
        images = args['images']
        videos = args['videos']
        comments = args['comments']

        new_incident = Incident(created_on, created_by, _type, latitude, longitude, status, images, videos, comments)
        created_incident = new_incident.create_incident()
        return make_response(jsonify({
            'status': 'ok',
            'message': 'incident created successfully',
            'data': created_incident
        }), 201)

    def get(self):
        """Get all incidents"""
        incidents = Incident.get_all_incidents(self)
        if len(incidents) == 0:
            return make_response(jsonify({
                'message':  'success',
                'status': 'ok',
                'incidents': 'Incidents are empty. Add an incident'
            }), 200)
        return make_response(jsonify({
            'message':  'success',
            'status': 'ok',
            'data': incidents
        }), 200)

@api.route('/admin')
class AdminIncidentEndpoint(Resource):
    def get(self):
        """User authentication"""
        incidents = Incident.get_all_incidents(self)
        if len(incidents) == 0:
            return make_response(jsonify({
                'message':  'success',
                'status': 'ok',
                'incidents': 'Incidents are empty. Add an incident'
            }), 200)
        return make_response(jsonify({
            'message':  'success',
            'status': 'ok',
            'data': incidents
        }), 200)

@api.route('/<int:incident_id>')
class SingleIncident(Resource):
    def get(self, incident_id):
        """Get a specific incident when provided with an id"""
        single_incident = Incident.get_incident(self, incident_id) 
        if single_incident:
            return make_response(jsonify({
                'status': 'ok',
                'message': 'success',
                'data': single_incident
            }), 200)
        return make_response(jsonify({
            'status': 'failed',
            'message': 'not found'
        }), 404)

    @api.expect(incident_fields)
    def put(self, incident_id):
        """Edit incident"""
        args = parser.parse_args()
        created_on = args['created_on']
        created_by = args['created_by']
        _type = args['type']
        latitude = args['latitude']
        longitude = args['longitude']
        status = args['status']
        images = args['images']
        videos = args['videos']
        comments = args['comments']

        update_incident = Incident(created_on, created_by, _type, latitude, longitude, status, images, videos, comments)
        updated_incident = update_incident.edit_incident(incident_id)
        return make_response(jsonify({
            'status': 'ok',
            'message': 'Incident edited successfully',
            'data': updated_incident
        }), 201)

@api.route('/admin/<int:incident_id>')
class AdminSingleIncident(Resource):
    def put(self):
        """Edit incident"""
        args = parser.parse_args()
        created_on = args['created_on']
        created_by = args['created_by']
        _type = args['type']
        latitude = args['latitude']
        longitude = args['longitude']
        status = args['status']
        images = args['images']
        videos = args['videos']
        comments = args['comments']

        update_incident = Incident(created_on, created_by, _type, latitude, longitude, status, images, videos, comments)
        updated_incident = update_incident.edit_incident(incident_id)
        return make_response(jsonify({
            'status': 'ok',
            'message': 'Incident edited successfully',
            'data': updated_incident
        }), 201)