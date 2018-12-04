
from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.incident_model import Incident
from app.api.v1.utils.auth import admin_required, token_required
import json

api = Namespace('Incident Endpoints', description='A collection of endpoints for the incident model; includes get, post, put and delete endpoints', path='api/v1/incidents')

parser = reqparse.RequestParser()
parser.add_argument('created_by', help = 'This field cannot be blank', required = True)
parser.add_argument('type', help = 'This field cannot be blank', required = True)
parser.add_argument('latitude', help = 'This field cannot be blank', required = True)
parser.add_argument('longitude', help = 'This field cannot be blank', required = True)
parser.add_argument('status', help = 'This field cannot be blank', required = True)
parser.add_argument('images', help = 'This field cannot be blank', required = True)
parser.add_argument('videos', help = 'This field cannot be blank', required = True)
parser.add_argument('comments', help = 'This field cannot be blank', required = True)

incident_fields = api.model('Incident', {
    'created_by': fields.String,
    'type': fields.String,
    'latitude': fields.String,
    'longitude': fields.String,
    'status': fields.String,
    'images': fields.List(fields.String),
    'videos': fields.List(fields.String),
    'comments': fields.String
})

@api.route('')
class IncidentEndpoint(Resource):
    @api.expect(incident_fields)
    @api.doc(security='apikey')
    @token_required
    def post(self):
        """Create a new incident """
        args = parser.parse_args()
        created_by = args['created_by']
        _type = args['type']
        latitude = args['latitude']
        longitude = args['longitude']
        status = args['status']
        images = args['images']
        videos = args['videos']
        comments = args['comments']

        new_incident = Incident(created_by, _type, latitude, longitude, status, images, videos, comments)
        created_incident = new_incident.create_incident()
        return make_response(jsonify({
            'status': 'ok',
            'message': 'Success',
            'data': created_incident
        }), 201)

    @api.doc(security='apikey')
    @token_required
    def get(self):
        """Get all incidents"""
        incidents = Incident.get_all_incidents(self)
        if len(incidents) == 0:
            return make_response(jsonify({
                'message':  'success',
                'status': 'ok',
                'incidents': incidents
            }), 200)
        return make_response(jsonify({
            'message':  'success',
            'status': 'ok',
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
                'message':  'success',
                'status': 'ok',
                'incidents': incidents
            }), 200)
        return make_response(jsonify({
            'message':  'success',
            'status': 'ok',
            'data': incidents
        }), 200)

@api.route('/<int:incident_id>')
class SingleIncident(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, incident_id):
        """Get a specific incident when provided with an id"""
        single_incident = Incident.get_incident(self, incident_id) 
        return make_response(jsonify({
                'status': 'ok',
                'message': 'success',
                'data': single_incident
            }), 200)

    @api.expect(incident_fields)
    @api.doc(security='apikey')
    @token_required
    def put(self, incident_id):
        """Edit incident"""
        args = parser.parse_args()
        created_by = args['created_by']
        _type = args['type']
        latitude = args['latitude']
        longitude = args['longitude']
        status = args['status']
        images = args['images']
        videos = args['videos']
        comments = args['comments']

        update_incident = Incident(created_by, _type, latitude, longitude, status, images, videos, comments)
        updated_incident = update_incident.edit_incident(incident_id)
        return make_response(jsonify({
            'status': 'ok',
            'message': 'Successful',
            'data': updated_incident
        }), 201)

    @api.doc(security='apikey')
    @token_required
    def delete(self, incident_id):
        """Delete a specific incident when provided with an id"""
        delete_incident = Incident.delete_incident(self, incident_id) 
        return make_response(jsonify({
            'status': 'ok',
            'message': 'success',
            'data': delete_incident
        }), 200)

@api.route('/admin/<int:incident_id>')
class AdminSingleIncident(Resource):
    @api.expect(incident_fields)
    @api.doc(security='apikey')
    @admin_required
    def put(self, incident_id):
        """Edit incident status"""
        args = parser.parse_args()
        created_by = args['created_by']
        _type = args['type']
        latitude = args['latitude']
        longitude = args['longitude']
        status = args['status']
        images = args['images']
        videos = args['videos']
        comments = args['comments']

        update_incident = Incident(created_by, _type, latitude, longitude, status, images, videos, comments)
        updated_incident = update_incident.edit_incident(incident_id)
        return make_response(jsonify({
            'status': 'ok',
            'message': 'Successful',
            'data': updated_incident
        }), 201)