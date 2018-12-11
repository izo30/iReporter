from flask import Flask
from .instance.config import app_config
from .instance.db_config import DbSetup

def create_app(config):
    '''configuring the flask app'''
    app = Flask(__name__)

    from .api.v1 import version1 as v1
    app.register_blueprint(v1)

    from .api.v2 import version2 as v2
    app.register_blueprint(v2)
   
    app.config.from_object(app_config[config])
    app.url_map.strict_slashes = False
    app.config['testing'] = True

    #  setup database
    DbSetup().create_users_table()
    DbSetup().create_incidents_table()
    DbSetup().create_default_admin()

    # DbSetup().drop_tables()

    return app