from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify, request

from ..models.Product import Product
from ..models.User import User
from ..utils.Validator import ProductDataTransferObject

api = ProductDataTransferObject.product_namespace


product_validator_model = ProductDataTransferObject.product_model
product_validator_response = ProductDataTransferObject.product_response

parser = reqparse.RequestParser()
parser.add_argument('product_name')
parser.add_argument('product_description')
parser.add_argument('product_quantity')
parser.add_argument('product_category')
parser.add_argument('product_moq')


@api.route('')
class ProductEndpoint(Resource):

    """Contains all the endpoints for Product Model"""

    docStr = "Endpoint to post a Product"

    @api.expect(product_validator_model, validate=True)
    @api.doc(docStr, security='Authentication_token')
    def post(self):
        """Endpoint for adding a product"""
        args = parser.parse_args()
        name = args['product_name']
        description = args['product_description']
        quantity = args['product_quantity']
        category = args['product_category']
        moq = args['product_moq']
        added_by = 'James'

        new_product = Product()
        response = new_product.save_product(name, description, quantity, category, moq, added_by)
        if 'exists' in response:
            return dict(message="product exists", status="failed"), 400
        return make_response(jsonify({'status': 'ok',
                                      'message': 'success',
                                      'product': 'new_product'}), 201)
    @api.doc(security='Authentication_token')
    def get(self):

        product = Product()
        all_products = product.fetch_all_products()
        return dict(products=all_products, status="ok"), 200

@api.route('/<int:productId>')
@api.doc(security='Authentication_token')
class GetSingleProduct(Resource):
    """Get a single Product record"""
    def get(self, productId):
        """Retrieve a single product"""
        product = Product()
        existing_product = product.fetch_single_product(productId)
        if 'error' in existing_product:
            return dict(message="product not found", status="failed"), 404
        return dict(product=existing_product, status="ok"), 200
            
    def delete(self, productId):
        product = Product()
        del_product = product.delete_product(productId)
        return dict(message=del_product, status="ok"), 200
