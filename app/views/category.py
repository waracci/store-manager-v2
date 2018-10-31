from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
from ..models.Category import Category
from ..models.Sales import Sales
from ..models.User import User
from ..utils.admin_required import admin_required_check
from ..utils.Validator import categoryDataTransferObject
api = categoryDataTransferObject.category_namespace


category_validator_model = categoryDataTransferObject.category_model

parser = reqparse.RequestParser()
parser.add_argument('category_name', required=True)
parser.add_argument('category_description', required=True)


@api.route('')
class categoryEndpoint(Resource):

    """Contains all the endpoints for category Model"""

    docStr = "Endpoint to post a category"

    @api.expect(category_validator_model, validate=True)
    @api.doc(docStr, security='Authentication_token')
    @jwt_required
    @admin_required_check
    def post(self):
        """Add a category to inventory"""
        args = parser.parse_args()
        name = (args['category_name']).strip()
        description = args['category_description']
        new_category = Category()
        response = new_category.save_category(name, description)
        if 'exists' in response:
            return dict(message="category {} exists".format(name), status="failed"), 400
        return dict(message="category {} added to inventory".format(name), status="ok"), 201

    @api.doc(security='Authentication_token')
    @jwt_required
    def get(self):
        """Retrieve all categories"""
        category = Category()
        all_categories = category.fetch_all_categories()
        if 'empty' in all_categories:
            return dict(message="No categories in inventory", status="ok"), 404
        return dict(categories=all_categories, status="ok"), 200

@api.route('/<int:categoryId>')
@api.doc(security='Authentication_token')
class GetSinglecategory(Resource):
    """Get a single category record"""
    
    @jwt_required
    def get(self, categoryId):
        """Retrieve a single category"""
        category = Category()
        existing_category = category.fetch_single_category_by_id(categoryId)
        if 'error' in existing_category:
            return dict(message="category not found", status="failed"), 404
        return dict(category=existing_category, status="ok"), 200
    
    @jwt_required
    @admin_required_check
    def delete(self, categoryId):
        """Delete a single category"""
        category = Category()
        del_category = category.delete_category(categoryId)
        return dict(message=del_category, status="ok"), 200

   
    @jwt_required
    @api.expect(category_validator_model, validate=True)
    def put(self, categoryId):
        existing_category = Category().fetch_single_category_by_id(categoryId)
        if 'error' in existing_category:
            return dict(message="not found", status="failed"), 404
        data = request.get_json(force=True)
        category_name = (existing_category[0]['name']).lower()
        if 'category_name' in data:
            same_name_category = Category().fetch_single_category_by_name((data['category_name']).lower())
            if list(same_name_category)[0] != 'error':
                    return dict(message="category name exists already", status="failed"), 400
            category_name = data['category_name']
        category_description = existing_category[0]['description']
        if 'category_description' in data:
            category_description = data['category_description']
        Category().edit_category(categoryId, category_name, category_description)
        return dict(message="success", status="ok"), 200
