import os
"""
class for app configurations
"""
class Config():
    """Base Config"""
    DEBUG = False
    SECRET_KEY = 'h7dr4jd48jj84uf84kdnmks8do4fkkt85g98nd3'

class Development(Config):
    '''Configurations for development'''
    Debug = True
    os.environ['DB'] = 'ireporter'

class Testing(Config):
    '''Congigurations for testing'''
    TESTING = True
    Debug = True
    os.environ['DB'] = 'ireportertest'

app_config = {
    'development' : Development(),
    'testing' : Testing()
}

secret_key = Config.SECRET_KEY