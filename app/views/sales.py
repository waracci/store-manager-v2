from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models.Sales import Sales
from ..models.User import User
from ..utils.admin_required import admin_required_check
from ..utils.Validator import SalesDataTransferObject
# from ..utils.jwt_decorator import jwt_required
api = SalesDataTransferObject.sales_namespace
parser = reqparse.RequestParser()
parser.add_argument('product_quantity')
parser.add_argument('product_id')


@api.route('')
class SalesEndpoint(Resource):
    """Sales Endpoints, fetch all sales and Fetch all sales"""
    doctsr = "Sales Endpoints, Fetch and retrieve sales records"

    @api.doc(security="Authentication_token")
    @jwt_required
    def post(self):
        """Make sales endpoints"""
        args = parser.parse_args()
        quantity = args['product_quantity']
        productId = args['product_id']
        if not quantity:
            return dict(message="product_quantity not provided", status="failed"), 400
        if int(quantity) <= 0:
            return dict(message="product quantity cannot be zero or less", status="failed"), 400
        new_sale = Sales()
        existing_product = new_sale.sell_single_product(productId, quantity, get_jwt_identity())

        if 'unavailable' in existing_product:
            return dict(message="Product not found for sale", status="failed"), 404
            
        if 'insufficient' in existing_product:
            return dict(message="{} products remaining only".format(existing_product['quantity']), status="failed"), 404
        
        if 'remaining' in existing_product:
            return dict(message="Low stock levels, sale cannot be completed", status="failed"), 400

        return existing_product, 201

    @api.doc(security="Authentication_token")
    @jwt_required
    def get(self):
        """Retrieve all sales records"""
        # check for admin
        all_sales = Sales().fetch_all_sales()
        if 'empty' in all_sales:
            return dict(message="No Sales made", status="ok"), 404
        return dict(sales=all_sales, status="ok"), 200
        

@api.route('/<int:saleId>')
@api.doc(security='Authentication_token')
class GetSingleSalesRecord(Resource):
    """Retrieve single Sales Record"""

    @jwt_required
    def get(self, saleId):
        """Retrieve a single sale"""
        sale = Sales()
        existing_sale = sale.fetch_single_sales_record(saleId)
        if 'error' in existing_sale:
            return dict(message="sales record not found", status="failed"), 404
        if 'unauthorized' in existing_sale:
            return dict(message="requires admin", status="failed"), 406
        return dict(sale=existing_sale, status="ok"), 200
    
    @jwt_required
    def delete(self, saleId):
        """Delete a single sales record"""
        del_sale = Sales().delete_sale(saleId)
        return dict(message=del_sale, status="ok"), 200
