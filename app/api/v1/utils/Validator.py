from flask_restplus import fields, Namespace


class ProductDataTransferObject():
    product_namespace = Namespace('Product endpoints',
                description='Product endpoints to add, edit and delete products')

    product_model = product_namespace.model('product model', {
        'product_name': fields.String(description='product name'),
        'product_description': fields.String(description='product description'),
        'product_quantity': fields.Integer(description='product stock quantity'),
        'product_category': fields.String(description='product category'),
        'product_moq': fields.Integer(description='product minimum order quantity')
    })

    product_response = product_namespace.model('Product response for any get method', {
        'product_id': fields.Integer(description='Unique Id for every product'),
        'product_name': fields.String(description='product name'),
        'product_description': fields.String(description='product description'),
        'product_quantity': fields.Integer(description='product quantity'),
        'product_category': fields.String(description='product category'),
        'product_moq': fields.Integer(description='Minimum order quantity'),
        'product_quantity_store': fields.Integer(description='stock level'),
        'date_created': fields.DateTime(dt_format='rfc822', description='date product was added to inventory'),
        'date_modified': fields.DateTime(dt_format='rfc822', description='date product details were modified'),
        'added_by': fields.String(description='Identity of admin that added the product')
    })

class SalesDataTransferObject():
    sales_namespace = Namespace('Sales endpoints',
                description='Sales endpoints to make a sale and view sales made')
    sales_model = sales_namespace.model('sales response', {
        'cart': fields.String(description='Sales cart, contains a list of products being sold'),
        'cart_price': fields.Integer(description='Total sales price')
    })

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
