"""App module: sets the configuration for the flask application"""

import os
from datetime import timedelta
# Third party imports
from flask import Flask, jsonify, Blueprint
from flask_restplus import Api
from flask_jwt_extended import JWTManager
from instance.config import app_configuration
from app.Database_setup import Database_Setup_Config
from app.utils.database_helper import initialize_database

from app.views.product import api as product_namespace
from app.views.sales import api as sales_namespace
from app.views.auth import api as auth_endpoint
jwt = JWTManager()
from app.models.User import blacklist
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(app_configuration[config_name])
    app.config.from_pyfile('config.py')
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    jwt.init_app(app)
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist

    version2 = Blueprint('api version 2', __name__, url_prefix='/api/v2')
    authorizations = {'Authentication_token': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Authorization'
    }}

    api = Api(version2,
            title='Store manager API',
            version='2.0',
            description='An application that helps store owners manage sales \
                and product inventory records',
            authorizations=authorizations)
    app.register_blueprint(version2)            
    api.add_namespace(auth_endpoint, path='/auth/')
    api.add_namespace(product_namespace, path='/products')
    api.add_namespace(sales_namespace, path='/sales')

    jwt._set_error_handler_callbacks(api)
    

    return app
