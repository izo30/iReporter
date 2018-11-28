from flask import Flask
from flask_restplus import Api, Resource

def create_app():
    app = Flask(__name__)

    from .api.v1 import version1 as v1
    app.register_blueprint(v1)

    app.url_map.strict_slashes = False
    
    return app