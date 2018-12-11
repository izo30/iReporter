from flask_restplus import Api
from flask import Blueprint

# Import all endpoints for all models
from .views.user_auth_views import api as user_auth_namespace
from .views.incident_view import api as incident_namespace

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

version1 = Blueprint('api version 1', __name__, url_prefix='/api/v1')
api = Api(version1, title='iReporter API', version='1.0', description='An application\
    that helps users report corruption incidents and ask for government interventions',\
    authorizations=authorizations)

api.add_namespace(user_auth_namespace, path='/auth')
api.add_namespace(incident_namespace, path='/incidents')