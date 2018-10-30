"""App module: sets the configuration for the flask application"""

import os
from datetime import timedelta
# Third party imports
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from instance.config import app_configuration
from app.Database_setup import Database_Setup_Config
from app.api.v1.utils.database_helper import initialize_database
connection = initialize_database()
jwt = JWTManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    from .api.v1 import version2 as v2
    app.register_blueprint(v2)

    app.config.from_object(app_configuration[config_name])
    app.config.from_pyfile('config.py')
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    jwt.init_app(app)
    cursor = connection.cursor()
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        cursor.execute("SELECT * FROM tokens WHERE token = %s;", (jti,))
        black_token = cursor.fetchone()
        return black_token

    application_database_connection = Database_Setup_Config(config_name)
    application_database_connection.initialize_database_tables()

    return app
