from flask import Flask
from .instance.config import app_config

def create_app(config):
    '''configuring the flask app'''
    app = Flask(__name__)

    from .api.v1 import version1 as v1
    app.register_blueprint(v1)
   
    app.config.from_object(app_config[config])
    app.url_map.strict_slashes = False
    app.config['testing'] = True

    return app