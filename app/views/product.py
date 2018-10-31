from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.Product import Product
from ..models.Sales import Sales
from ..models.User import User
from ..utils.Validator import ProductDataTransferObject
api = ProductDataTransferObject.product_namespace


product_validator_model = ProductDataTransferObject.product_model
product_sale_model = ProductDataTransferObject.product_sale_model
product_edit_model = ProductDataTransferObject.product_edit_model
product_validator_response = ProductDataTransferObject.product_response

parser = reqparse.RequestParser()
parser.add_argument('product_name')
parser.add_argument('product_description')
parser.add_argument('product_quantity')
parser.add_argument('product_category')
parser.add_argument('product_moq')
parser.add_argument('product_price')


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
        name = (args['product_name']).strip()
        description = args['product_description']
        price = args['product_price']
        quantity = args['product_quantity']
        category = args['product_category']
        moq = args['product_moq']
        if int(price) < 0 or int(quantity) < 0 or int(moq) < 0:
            return dict(message="item quantities cannot be zero", status="failed"), 400
        # if name.strip() == "":
        #     return dict()
        # also check if negative
        
        # Make a validator method that takes in *args 
        added_by = get_jwt_identity()
        new_product = Product()
        response = new_product.save_product(name, description, price, quantity, category, moq, added_by)
        if 'exists' in response:
            return dict(message="product {} exists".format(name), status="failed"), 400
        return dict(message="Product {} added to inventory".format(name), status="ok"), 201

    @api.doc(security='Authentication_token')
    @jwt_required
    def get(self):
        """Retrieve all products in inventory"""
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
        args = parser.parse_args()
        quantity = args['product_quantity']
        if not quantity:
            return dict(message="product_quantity not provided", status="failed"), 400
        if int(quantity) <= 0:
            return dict(message="product quantity cannot be zero or less", status="failed"), 400
        new_sale = Sales()
        existing_product = new_sale.sell_single_product(productId, quantity, get_jwt_identity())
        # import pdb; pdb.set_trace()
        if 'unavailable' in existing_product:
            return dict(message="Product not found for sale", status="failed"), 404
            
        if 'insufficient' in existing_product:
            return dict(message="{} products remaining only".format(existing_product['quantity']), status="failed"), 404
        
        if 'remaining' in existing_product:
            return dict(message="Low stock levels, sale cannot be completed", status="failed"), 400

        return existing_product, 200

    @jwt_required
    @api.expect(product_edit_model, validate=True)
    def put(self, productId):
        existing_product = Product().fetch_single_product(productId)
        data = request.get_json()
        product_name = existing_product['name']
        if 'product_name' in data:
            product_name = data['product_name']
        product_description = existing_product['description']
        if 'product_description' in data:
            product_description = data['product_description']
        product_price = existing_product['price']
        if 'product_price' in data:
            product_price = data['product_price']
        product_quantity = existing_product['quantity']
        if 'product_quantity' in data:
            product_quantity = data['product_quantity']
        product_category = existing_product['category']
        if 'product_catgory' in data:
            product_category = data['product_category']
        product_moq = existing_product['moq']
        if 'product_moq' in data:
            product_moq = data['product_moq']
        Product().edit_product(productId, product_name, product_description, 
                                              product_price, product_quantity,
                                              product_category, product_moq, get_jwt_identity())
        return dict(message="success", status="ok"), 200