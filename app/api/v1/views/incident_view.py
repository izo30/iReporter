
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
    'created_by': fields.String,
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
        created_by = args['created_by']
        _type = args['type']
        latitude = args['latitude']
        longitude = args['longitude']
        images = args['images']
        videos = args['videos']
        comments = args['comments']

        new_incident = Incident(created_by, _type, latitude, longitude, images, videos, comments)
        created_incident = new_incident.create_incident()

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
        incidents = Incident.get_all_incidents(self)
        if len(incidents) == 0:
            return make_response(jsonify({
                'status': 'Fail',
                'data': incidents
            }), 404)
        return make_response(jsonify({
            'status': 'Success',
            'data': incidents
        }), 200)

@api.route('/admin')
class AdminIncidentEndpoint(Resource):
    @api.doc(security='apikey')
    @admin_required
    def get(self):
        """Admin get all incidents"""
        incidents = Incident.get_all_incidents(self)
        if len(incidents) == 0:
            return make_response(jsonify({
                'status': 'Fail',
                'data': incidents
            }), 404)
        return make_response(jsonify({
            'status': 'Success',
            'data': incidents
        }), 200)

@api.route('/<int:incident_id>')
class SingleIncident(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, incident_id):
        """Get a specific incident when provided with an id"""
        single_incident = Incident.get_incident(self, incident_id) 
        if single_incident == "Incident not found":
            return make_response(jsonify({
                'status': 'Fail',
                'data': single_incident
            }), 404)
        return make_response(jsonify({
            'status': 'Success',
            'data': single_incident
        }), 200)

    @api.expect(incident_fields)
    @api.doc(security='apikey')
    @token_required
    def put(self, incident_id):
        """Edit incident"""
        parser = required_incident_fields()
        args = parser.parse_args()
        created_by = args['created_by']
        _type = args['type']
        latitude = args['latitude']
        longitude = args['longitude']
        images = args['images']
        videos = args['videos']
        comments = args['comments']

        update_incident = Incident(created_by, _type, latitude, longitude, images, videos, comments)
        updated_incident = update_incident.edit_incident(incident_id)

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
        delete_incident = Incident.delete_incident(self, incident_id) 

        if delete_incident == "Incident not found":
            return make_response(jsonify({
                'status': 'Fail',
                'message': delete_incident
            }), 404)

        return make_response(jsonify({
            'status': 'Success',
            'message': delete_incident
        }), 200)

@api.route('/admin/<int:incident_id>')
class AdminSingleIncident(Resource):
    @api.expect(status_field)
    @api.doc(security='apikey')
    @admin_required
    def put(self, incident_id):
        """Edit incident status"""
        parser = admin_status_field()
        args = parser.parse_args()
        status = args['status']

        update_incident = Incident.admin_edit_incident(incident_id, status)
        
        if update_incident == "Field should not be empty":
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