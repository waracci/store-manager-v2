from flask_restplus import fields, Namespace


class ProductDataTransferObject():
    product_namespace = Namespace('Product endpoints',
                description='Product endpoints to add, edit and delete products')

    product_model = product_namespace.model('product model', {
        'product_name': fields.String(description='product name'),
        'product_description': fields.String(description='product description'),
        'product_price': fields.Integer(description='product price'),
        'product_quantity': fields.Integer(description='product stock quantity'),
        'product_category': fields.String(description='product category'),
        'product_minorder': fields.Integer(description='product minimum order quantity')
    })

    product_edit_model = product_namespace.model('product model', {
        'product_name': fields.String(description='product name'),
        'product_description': fields.String(description='product description'),
        'product_price': fields.Integer(description='product price'),
        'product_quantity': fields.Integer(description='product stock quantity'),
        'product_category': fields.String(description='product category'),
        'product_minorder': fields.Integer(description='product minimum order quantity')
    })

    product_sale_model = product_namespace.model('product model', {
        'product_quantity': fields.Integer(description='product stock quantity'),
        'product_id': fields.Integer(description='product id')
    })

class SalesDataTransferObject():
    sales_namespace = Namespace('Sales endpoints',
                description='Sales endpoints to make a sale and view sales made')

class AuthDataTransferObject():
    authentication_namespace = Namespace('User Authentication',
                description='User authentication to access protected routes')
    authentication_model_register = authentication_namespace.model('authentication register', {
        'email': fields.String(description='User registration email'),
        'password': fields.String(description='User password'),
        'confirm_password': fields.String(description='User password confirmation'),
        'role': fields.String(description='User role')
    })
    authentication_model_login = authentication_namespace.model('authentication login', {
        'email': fields.String(description='User registration email'),
        'password': fields.String(description='User password')
    })
class categoryDataTransferObject():
    category_namespace = Namespace('Product Category',
                description='Product categories')
    category_model = category_namespace.model('category model', {
        'category_name': fields.String(description="Category name"),
        'category_description': fields.String(description="Category description")})
