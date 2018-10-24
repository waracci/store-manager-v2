from flask_restplus import Api
from flask import Blueprint

# Import all endpoints for all models
# from .views.product import api as product_namespace
# from .views.sales import api as sales_namespace
# from .views.auth import api as auth_endpoint

# version1 = Blueprint('api version 1', __name__, url_prefix='/api/v1')

# authorizations = {'Authentication_token': {
#   'type': 'apiKey',
#   'in': 'header',
#   'name': 'Authorization'
# }}

# api = Api(version1,
#           title='Store manager API',
#           version='1.0',
#           description='An application that helps store owners manage sales \
#             and product inventory records',
#           authorizations=authorizations)
          
# api.add_namespace(auth_endpoint, path='/')
# api.add_namespace(product_namespace, path='/products')
# api.add_namespace(sales_namespace, path='/sales')
