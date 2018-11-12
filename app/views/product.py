from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
from ..models.Product import Product
from ..models.Sales import Sales
from ..models.User import User
from ..utils.admin_required import admin_required_check
from ..utils.Validator import ProductDataTransferObject
api = ProductDataTransferObject.product_namespace


product_validator_model = ProductDataTransferObject.product_model
product_sale_model = ProductDataTransferObject.product_sale_model
product_edit_model = ProductDataTransferObject.product_edit_model

parser = reqparse.RequestParser()
parser.add_argument('product_name')
parser.add_argument('product_description')
parser.add_argument('product_quantity')
parser.add_argument('product_category')
parser.add_argument('product_minorder')
parser.add_argument('product_price')


@api.route('')
class ProductEndpoint(Resource):

    """Contains all the endpoints for Product Model"""

    docStr = "Endpoint to post a Product"

    @api.expect(product_validator_model, validate=True)
    @api.doc(docStr, security='Authentication_token')
    @jwt_required
    @admin_required_check
    def post(self):
        """Add a product to inventory"""
        args = parser.parse_args()
        name = (args['product_name']).strip()
        if name == "":
            return dict(message="product name cant be null"), 400
        if not name:
            return dict(message="product name missing"), 400
        description = args['product_description']
        if not description:
            return dict(message="product description missing"), 400
        price = args['product_price']
        if not price:
            return dict(message="product price missing"), 400
        quantity = args['product_quantity']
        if not quantity:
            return dict(message="product quantity missing"), 400
        category = args['product_category']
        minorder = args['product_minorder']
        if not minorder:
            return dict(message="product minimum order quantity missing"), 400
        if int(price) < 0 or int(quantity) < 0 or int(minorder) < 0:
            return dict(message="item quantities cannot be zero", status="failed"), 400

        added_by = get_jwt_identity()
        new_product = Product()
        response = new_product.save_product(name, description, price, quantity, category, minorder, added_by)
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
    @admin_required_check
    def delete(self, productId):
        """Delete a single product"""
        product = Product()
        del_product = product.delete_product(productId)
        return dict(message=del_product, status="ok"), 200


    @jwt_required
    @api.expect(product_edit_model, validate=True)
    def put(self, productId):
        existing_product = Product().fetch_single_product(productId)
        if 'error' in existing_product:
            return dict(message="product not found", status="failed"), 404
        data = request.get_json(force=True)
        product_name = (existing_product[0]['name']).lower()
        if 'product_name' in data:
            product_name = data['product_name']
        product_description = existing_product[0]['description']
        if 'product_description' in data:
            product_description = data['product_description']
        product_price = existing_product[0]['price']
        if 'product_price' in data:
            product_price = data['product_price']
        product_quantity = existing_product[0]['quantity']
        if 'product_quantity' in data:
            product_quantity = (data['product_quantity'])
        product_category = existing_product[0]['category']
        if 'product_catgory' in data:
            product_category = data['product_category']
        product_minorder = existing_product[0]['minorder']
        if 'product_minorder' in data:
            product_minorder = data['product_minorder']
        edited_product = Product().edit_product(productId, product_name, product_description, 
                                              product_price, product_quantity,
                                              product_category, product_minorder, get_jwt_identity())
        if 'exists' in edited_product:
            return dict(message="Product already exists", status="failed"), 409
        return dict(message="success", status="ok"), 200
