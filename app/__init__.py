"""App module: sets the configuration for the flask application"""

# Third party imports
from flask import Flask
from instance.config import app_configuration
from app.Database_setup import Database_Setup_Config

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    from .api.v1 import version2 as v2
    app.register_blueprint(v2)

    app.config.from_object(app_configuration[config_name])
    app.config.from_pyfile('config.py')
    application_database_connection = Database_Setup_Config(config_name)
    application_database_connection.initialize_database_tables()

    return app
