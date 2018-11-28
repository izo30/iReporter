from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Api, Namespace, fields
from app.api.v1.models.red_flags_model import RedFlags

api = Namespace('Red_Flags_endpoints', description='A collection of endpoints for the red flags model; includes get and post endpoints', path='api/v1/redflags')

parser = reqparse.RequestParser()
parser.add_argument('created_on', help = 'This field cannot be blank', required = True)
parser.add_argument('created_by', help = 'This field cannot be blank', required = True)
parser.add_argument('latitude', help = 'This field cannot be blank', required = True)
parser.add_argument('longitude', help = 'This field cannot be blank', required = True)
parser.add_argument('status', help = 'This field cannot be blank', required = True)
parser.add_argument('images', help = 'This field cannot be blank', required = True)
parser.add_argument('videos', help = 'This field cannot be blank', required = True)
parser.add_argument('description', help = 'This field cannot be blank', required = True)

@api.route('')
class RedFlagsEndpoint(Resource):

    red_flags_fields = api.model('RedFlag', {
        'created_on' : fields.DateTime(),
        'created_by': fields.Integer,
        'latitude': fields.Float,
        'longitude': fields.Float,
        'status' : fields.String,
        'images': fields.List(fields.String),
        'videos': fields.List(fields.String),
        'description': fields.String
    })

    @api.expect(red_flags_fields)
    def post(self):
        """Add new red flag"""
        args = parser.parse_args()
        created_on = args['created_on']
        created_by = args['created_by']
        latitude = args['latitude']
        longitude = args['longitude']
        status = args['status']
        images = args['images']
        videos = args['videos']
        description = args['description']

        new_red_flag = RedFlags(created_on, created_by, latitude, longitude, status, images, videos, description)
        created_red_flag = new_red_flag.create_red_flag()
        return make_response(jsonify({
            'status': 'ok',
            'message': 'Red Flag created successfully',
            'red flags': created_red_flag
        }), 201)

    def get(self):
        """Get all red flags"""
        red_flags = RedFlags.get_all_red_flags(self)

        return make_response(jsonify({
            'message':  'success',
            'status': 'ok',
            'red flags': red_flags
        }), 200)
