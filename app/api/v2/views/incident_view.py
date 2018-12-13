
from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from ..models.incident_model import Incident
from ..utils.auth import admin_required, token_required, AuthToken
from ..utils.validations import Validations
import json

api = Namespace('Incident Endpoints', description='A collection of endpoints for the incident model; includes get, post, put and delete endpoints', path='api/v1/incidents')

def required_incident_fields():
    parser = reqparse.RequestParser()
    Validations().add_arguments(parser, ['type','latitude','longitude','images','videos','comments'])
    return parser

def required_edit_incident_fields():
    parser = reqparse.RequestParser()
    Validations().add_arguments(parser, ['latitude','longitude','images','videos','comments'])
    return parser

def admin_status_field():
    parser = reqparse.RequestParser()
    Validations().add_arguments(parser, ['status'])
    return parser

incident_fields = api.model('Incident', {
    'type': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'images': fields.List(fields.String),
    'videos': fields.List(fields.String),
    'comments': fields.String
})

edit_incident_fields = api.model('Edit Incident', {
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

        validate = Validations().validate_incident_data(latitude, longitude, images, videos, comments, _type)
        if validate:
            return {
                'status': 'Fail',
                'error': validate['error']
            }, 400

        created_incident = Incident().create_incident(_type, latitude, longitude, images, videos, comments)
        return {
            'status': 'Success',
            'data': created_incident
        }, 201

    @api.doc(security='apikey')
    @token_required
    def get(self):
        """Get all incidents"""
        incidents = Incident().get_all_incidents()
        return {
            'status': 'Success',
            'data': incidents
        }, 200

@api.route('/<string:incident_id>')
class SingleIncident(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, incident_id):
        """Get a specific incident when provided with an id"""
        single_incident = Incident().get_single_incident(incident_id) 
        if single_incident:
            return {
                'status': 'Success',
                'data': single_incident
            }, 200
        
        return incident_not_found()

    @api.expect(edit_incident_fields)
    @api.doc(security='apikey')
    @token_required
    def put(self, incident_id):
        """Edit incident"""
        parser = required_edit_incident_fields()
        args = parser.parse_args()
        latitude = args['latitude']
        longitude = args['longitude']
        images = args['images']
        videos = args['videos']
        comments = args['comments']

        validate = Validations().validate_incident_data(latitude, longitude, images, videos, comments)
        if validate:
            return {
                'status': 'Fail',
                'error': validate['error']
            }, 400

        updated_incident = Incident().edit_incident(incident_id, latitude, longitude, images, videos, comments)

        if updated_incident:
            return {
                'status': 'Success',
                'data': updated_incident
            }, 201

        return incident_not_found()

    @api.doc(security='apikey')
    @token_required
    def delete(self, incident_id):
        """Delete a specific incident when provided with an id"""
        created_by = AuthToken().get_user_id()

        if not Incident().check_user_incident_exists(incident_id, created_by):
            return incident_not_found()

        if not Incident().check_can_delete(incident_id, created_by):
            return {
                'status': 'Fail',
                'message': 'Incident status has changed. It cannot be deleted'
            }, 400

        delete_incident = Incident().delete_incident(incident_id) 

        if delete_incident:
            return {
                'status': 'Success',
                'message': delete_incident
            }, 200

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

        if not status.strip():
            return {
                'status': 'Fail',
                'error': 'Status should not be empty'
            }, 400

        if not Validations().check_if_status(status):
            return {
                'status': 'Fail',
                'error': 'Invalid status'
            }, 400

        update_incident = Incident().admin_edit_incident_status(incident_id, status)

        if update_incident:
            return {
                'status': 'Success',
                'data': update_incident
            }, 201

        return incident_not_found()

def incident_not_found():
    return {
        'status': 'Fail',
        'data': 'Incident not found'
    }, 404
        