from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify, request

from ..models.Product import Product
from ..models.Sales import Sales
from ..models.User import User
from ..utils.Validator import ProductDataTransferObject
from ..utils.jwt_decorator import jwt_required
from ..utils.decode_token import jwt_decode
api = ProductDataTransferObject.product_namespace


product_validator_model = ProductDataTransferObject.product_model
product_sale_model = ProductDataTransferObject.product_sale_model
product_validator_response = ProductDataTransferObject.product_response

parser = reqparse.RequestParser()
parser.add_argument('product_name', required=True)
parser.add_argument('product_description', required=True)
parser.add_argument('product_quantity', required=True)
parser.add_argument('product_category', required=True)
parser.add_argument('product_moq', required=True)
parser.add_argument('product_price', required=True)


@api.route('')
class ProductEndpoint(Resource):

    """Contains all the endpoints for Product Model"""

    docStr = "Endpoint to post a Product"

    @api.expect(product_validator_model, validate=True)
    @api.doc(docStr, security='Authentication_token')
    @jwt_required
    def post(self):
        """Add a product to inventory"""
        args = parser.parse_args()
        name = args['product_name']
        description = args['product_description']
        price = args['product_price']
        quantity = args['product_quantity']
        category = args['product_category']
        moq = args['product_moq']

        # if name.strip() == "":
        #     return dict()
        # also check if negative
        
        # Make a validator method that takes in *args 

        if 'error' in jwt_decode():
            return dict(message="invalid token", status="failed"), 401
        if 'invalid' in jwt_decode():
            return dict(message="invalid token", status="failed"), 401
        if 'expired' in jwt_decode():
            return dict(message="expired token", status="failed"), 401
        added_by = jwt_decode()

        new_product = Product()
        response = new_product.save_product(name, description, price, quantity, category, moq, added_by)
        if 'exists' in response:
            return dict(message="product {} exists".format(name), status="failed"), 400
        return dict(message="Product {} added to inventory".format(name), status="ok"), 201

    @api.doc(security='Authentication_token')
    @jwt_required
    def get(self):
        """Retrieve all products in inventory"""
        # print(user_identity)
        product = Product()
        all_products = product.fetch_all_products()
        if 'empty' in all_products:
            return dict(message="No products in inventory", status="ok"), 404
        return dict(products=all_products, status="ok"), 200

@api.route('/<int:productId>')
@api.doc(security='Authentication_token')
class GetSingleProduct(Resource):
    """Get a single Product record"""
    
    @jwt_required
    def get(self, productId):
        """Retrieve a single product"""
        product = Product()
        existing_product = product.fetch_single_product(productId)
        if 'error' in existing_product:
            return dict(message="product not found", status="failed"), 404
        return dict(product=existing_product, status="ok"), 200
    
    @jwt_required
    def delete(self, productId):
        """Delete a single product"""
        product = Product()
        del_product = product.delete_product(productId)
        return dict(message=del_product, status="ok"), 200

    @jwt_required
    @api.expect(product_sale_model, validate=True)
    def post(self, productId):
        """Sell a single product"""
        if 'error' in jwt_decode():
            return dict(message="invalid token", status="failed"), 401
        if 'invalid' in jwt_decode():
            return dict(message="invalid token", status="failed"), 401
        if 'expired' in jwt_decode():
            return dict(message="expired token", status="failed"), 401
        args = parser.parse_args()
        quantity = args['product_quantity']
        if not quantity:
            return dict(message="product_quantity not provided", status="failed"), 400
        if int(quantity) <= 0:
            return dict(message="product quantity cannot be zero or less", status="failed"), 400
        new_sale = Sales()
        existing_product = new_sale.sell_single_product(productId, quantity, jwt_decode())
        # import pdb; pdb.set_trace()
        if 'unavailable' in existing_product:
            return dict(message="Product not found for sale", status="failed"), 404
            
        if 'insufficient' in existing_product:
            return dict(message="{} products remaining only".format(existing_product['quantity']), status="failed"), 404
        
        if 'remaining' in existing_product:
            return dict(message="Low stock levels, sale cannot be completed", status="failed"), 400

        return existing_product, 200

    @jwt_required
    def put(self, productId):
        return "edit {}".format(productId)
