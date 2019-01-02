from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from app.api.v2.utils.views_fields import incidents_api as api, IncidentFields
from app.api.v2.models.incident_model import Incident
from app.api.v2.utils.auth import admin_required, user_required, AuthToken
from app.api.v2.utils.validations import Validations
import json

@api.route('')
class IncidentEndpoint(Resource):
    @api.expect(IncidentFields.incident_fields)
    @api.doc(security='apikey')
    @user_required
    def post(self):
        """Create a new incident """
        parser = IncidentFields.required_incident_fields()
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
    @user_required
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
    @user_required
    def get(self, incident_id):
        """Get a specific incident when provided with an id"""
        single_incident = Incident().get_single_incident(incident_id) 
        if single_incident:
            return {
                'status': 'Success',
                'data': single_incident
            }, 200
        
        return incident_not_found()

    @api.doc(security='apikey')
    @user_required
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

@api.route('/<string:incident_id>/status')
class AdminSingleIncident(Resource):
    @api.expect(IncidentFields.status_field)
    @api.doc(security='apikey')
    @admin_required
    def patch(self, incident_id):
        """Edit incident status"""
        parser = IncidentFields.admin_status_field()
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

@api.route('/<string:incident_id>/location')
class EditIncidentLocation(Resource):
    @api.expect(IncidentFields.location_fields)
    @api.doc(security='apikey')
    @user_required
    def patch(self, incident_id):
        """Edit incident location"""
        parser = IncidentFields.edit_location_fields()
        args = parser.parse_args()
        latitude = args['latitude']
        longitude = args['longitude']

        is_empty = Validations().check_if_empty(dict(latitude = latitude, longitude = longitude))
        if is_empty:
            return {
                'status': 'Fail',
                'error': is_empty
            }, 400

        if not Validations().validate_location([latitude, longitude]):
            return {
                'status': 'Fail',
                'error': 'Latitude and longitude should be a float'
            }, 400

        update_location = Incident().edit_incident_location(incident_id, latitude, longitude)

        if update_location:
            return {
                'status': 'Success',
                'data': update_location
            }, 201

        return incident_not_found()

@api.route('/<string:incident_id>/comment')
class EditIncidentComment(Resource):
    @api.expect(IncidentFields.comments_fields)
    @api.doc(security='apikey')
    @user_required
    def patch(self, incident_id):
        """Edit incident comment"""
        parser = IncidentFields.edit_comments_fields()
        args = parser.parse_args()
        comment = args['comments']

        if not comment.strip():
            return {
                'status': 'Fail',
                'error': "Comment should not be empty"
            }, 400

        if not Validations().validate_comments(comment):
            return {
                'status': 'Fail',
                'error': "Comments should contain alphanumeric plus ,.;:\"' only"
            }, 400

        update_comment = Incident().edit_incident_comment(incident_id, comment)

        if update_comment:
            return {
                'status': 'Success',
                'data': update_comment
            }, 201

        return incident_not_found()

def incident_not_found():
    return {
        'status': 'Fail',
        'data': 'Incident not found'
    }, 404
        