from flask_restplus import Namespace, Resource
from flask import make_response, jsonify, request
from flask_jwt_extended import jwt_required

from ..models.Sales import Sales
from ..models.User import User
from ..utils.Validator import SalesDataTransferObject
# from ..utils.jwt_decorator import jwt_required
api = SalesDataTransferObject.sales_namespace
sales_validator = SalesDataTransferObject.sales_model


@api.route('')
class SalesEndpoint(Resource):
    """Sales Endpoints, fetch all sales and Fetch all sales"""
    doctsr = "Sales Endpoints, Fetch and retrieve sales records"

    @api.doc(doctsr, security="Authentication_token")
    @api.expect(sales_validator)
    @jwt_required
    def post(self):
        pass

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
        return dict(sale=existing_sale, status="ok"), 200
    
    @jwt_required
    def delete(self, saleId):
        """Delete a single sales record"""
        del_sale = Sales().delete_sale(saleId)
        return dict(message=del_sale, status="ok"), 200
