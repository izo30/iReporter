from flask_restplus import Api
from flask import Blueprint

# Import all endpoints for all models
from .views.red_flags_view import api as red_flags_namespace

version1 = Blueprint('api version 1', __name__, url_prefix='/api/v1')
api = Api(version1, title='iReporter API', version='1.0', description='An application that helps users report corruption incidents and ask for intervention')

api.add_namespace(red_flags_namespace, path='/redflag')