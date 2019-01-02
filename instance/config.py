import os
"""
class for app configurations
"""
class Config():
    """Base Config"""
    DEBUG = False
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY")

class Development(Config):
    '''Configurations for development'''
    DEBUG = True

class Testing(Config):
    '''Congigurations for testing'''
    TESTING = True
    DEBUG = True
    DB_NAME = os.getenv("TEST_DB_NAME")

class Production(Config):
    DEBUG = False
    DB_PASSWORD = os.getenv("PROD_DB_PASSWORD")
    DB_USERNAME = os.getenv("PROD_DB_USERNAME")
    DB_HOST = os.getenv("PROD_DB_HOST")
    DB_NAME = os.getenv("PROD_DB_NAME")

app_config = {
    'development' : Development(),
    'testing' : Testing(),
    'production' : Production()
}

secret_key = Config.SECRET_KEY