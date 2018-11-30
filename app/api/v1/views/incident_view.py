
from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.incident_model import Incident
from ..models.user_auth_models import User
from ..utils.auth import admin_required, token_required

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
@api.route('/create')
class IncidentEndpoint(Resource):
    @api.expect(incident_fields)
    @api.doc(security='apikey')
    @token_required
    def post(self):
        #User authentication
        authentication_header = request.headers.get('Authorization') 
        if authentication_header:
            try:
                auth_token = authentication_header.split(" ")[1]
                identity = User.decode_auth_token(auth_token)
                if identity == 'Invalid token. Please sign in again':
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'Invalid token. Please sign in again'
                    }), 401)

            except Exception:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'You are not authorized'
                }), 401)
            if auth_token:
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

