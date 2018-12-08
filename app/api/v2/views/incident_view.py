
from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.incident_model import Incident
from app.api.v1.utils.auth import admin_required, token_required
import json

api = Namespace('Incident Endpoints', description='A collection of endpoints for the incident model; includes get, post, put and delete endpoints', path='api/v1/incidents')

def required_incident_fields():
    parser = reqparse.RequestParser()
    parser.add_argument('created_by', help = 'This field cannot be blank', required = True)
    parser.add_argument('type', help = 'This field cannot be blank', required = True)
    parser.add_argument('latitude', help = 'This field cannot be blank', required = True)
    parser.add_argument('longitude', help = 'This field cannot be blank', required = True)
    parser.add_argument('images', help = 'This field cannot be blank', required = True)
    parser.add_argument('videos', help = 'This field cannot be blank', required = True)
    parser.add_argument('comments', help = 'This field cannot be blank', required = True)
    return parser

def admin_status_field():
    parser = reqparse.RequestParser()
    parser.add_argument('status', help = 'This field cannot be blank', required = True)
    return parser

incident_fields = api.model('Incident', {
    'type': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'images': fields.List(fields.String),
    'videos': fields.List(fields.String),
    'comments': fields.String
})

status_field = api.model('Status', {
    'status': fields.String
})

@api.route('')
class IncidentEndpoint(Resource):
    @api.expect(incident_fields)
    @api.doc(security='apikey')
    @token_required
    def post(self):
        """Create a new incident """
        parser = required_incident_fields()
        args = parser.parse_args()
        _type = args['type']
        latitude = args['latitude']
        longitude = args['longitude']
        images = args['images']
        videos = args['videos']
        comments = args['comments']

        new_incident = Incident()
        created_incident = new_incident.create_incident(_type, latitude, longitude, images, videos, comments)

        if created_incident == "Field should not be empty":
            return make_response(jsonify({
                'status': 'Fail',
                'data': created_incident
            }), 400)

        try:
            if created_incident['error']:
                return make_response(jsonify({
                    'status': 'Fail',
                    'error': created_incident['error']
                }), 400)
        except Exception:
            pass

        return make_response(jsonify({
            'status': 'Success',
            'data': created_incident
        }), 201)

