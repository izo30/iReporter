
from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.incident_model import Incident
from ..utils.auth import admin_required, token_required
import json

api = Namespace('Incident Endpoints', description='A collection of endpoints for the incident model; includes get, post, put and delete endpoints', path='api/v1/incidents')

def required_incident_fields():
    parser = reqparse.RequestParser()
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

edit_incident_fields = api.model('Incident', {
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

    @api.doc(security='apikey')
    @token_required
    def get(self):
        """Get all incidents"""
        incident = Incident()
        incidents = incident.get_all_incidents()
        if len(incidents) == 0:
            return make_response(jsonify({
                'status': 'Fail',
                'data': incidents
            }), 404)
        return make_response(jsonify({
            'status': 'Success',
            'data': incidents
        }), 200)

@api.route('/<string:incident_id>')
class SingleIncident(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, incident_id):
        """Get a specific incident when provided with an id"""
        incident = Incident()
        single_incident = incident.get_single_incident(incident_id) 
        if single_incident == "Incident not found":
            return make_response(jsonify({
                'status': 'Fail',
                'data': single_incident
            }), 404)
        return make_response(jsonify({
            'status': 'Success',
            'data': single_incident
        }), 200)

    @api.expect(edit_incident_fields)
    @api.doc(security='apikey')
    @token_required
    def put(self, incident_id):
        """Edit incident"""
        parser = required_incident_fields()
        args = parser.parse_args()
        latitude = args['latitude']
        longitude = args['longitude']
        images = args['images']
        videos = args['videos']
        comments = args['comments']

        incident = Incident()
        updated_incident = incident.edit_incident(incident_id, latitude, longitude, images, videos, comments)

        if updated_incident == "Field should not be empty":
            return make_response(jsonify({
                'status': 'Fail',
                'data': updated_incident
            }), 400)

        if updated_incident == "Incident not found":
            return make_response(jsonify({
                'status': 'Fail',
                'data': updated_incident
            }), 404)

        return make_response(jsonify({
            'status': 'Success',
            'data': updated_incident
        }), 201)

    @api.doc(security='apikey')
    @token_required
    def delete(self, incident_id):
        """Delete a specific incident when provided with an id"""
        incident = Incident()
        delete_incident = incident.delete_incident(incident_id) 

        if delete_incident == "Incident not found":
            return make_response(jsonify({
                'status': 'Fail',
                'message': delete_incident
            }), 404)

        return make_response(jsonify({
            'status': 'Success',
            'message': delete_incident
        }), 200)

@api.route('/admin/<string:incident_id>')
class AdminSingleIncident(Resource):
    @api.expect(status_field)
    @api.doc(security='apikey')
    @admin_required
    def put(self, incident_id):
        """Edit incident status"""
        parser = admin_status_field()
        args = parser.parse_args()
        status = args['status']

        incident = Incident()
        update_incident = incident.admin_edit_incident_status(incident_id, status)
        
        if update_incident == "Status should not be empty":
            return make_response(jsonify({
                'status': 'Fail',
                'data': update_incident
            }), 400)
        
        if update_incident == "Invalid status":
            return make_response(jsonify({
                'status': 'Fail',
                'data': update_incident
            }), 400)

        if update_incident == "Incident not found":
            return make_response(jsonify({
                'status': 'Fail',
                'data': update_incident
            }), 404)

        return make_response(jsonify({
            'status': 'Success',
            'data': update_incident
        }), 201)