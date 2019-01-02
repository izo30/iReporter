from flask import Flask
from instance.config import app_config
from instance.db_config import DbSetup
import os

def create_app(config):
    '''configuring the flask app'''
    app = Flask(__name__)

    from .api.v2 import version2 as v2
    app.register_blueprint(v2)
    app.config.from_object(app_config[config])
    app.url_map.strict_slashes = False

    return app