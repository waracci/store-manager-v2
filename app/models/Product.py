"""Product Model and data storage functions"""
from datetime import datetime
import psycopg2.extras as extras 

from ..utils.database_helper import initialize_database

class Product():
    """This class defines the Product model and
        the various methods of manipulating the product data"""

    def __init__(self):
        """Initialise the Product model with constructor"""
        self.connection = initialize_database()
        self.cursor = self.connection.cursor()
        self.custom_cursor = self.connection.cursor(cursor_factory=extras.DictCursor)

    def save_product(self, product_name, product_description, product_price, product_quantity,
       product_category, product_minorder, added_by):
        """Product Class method to add product to list"""
        self.product_name = product_name
        self.product_description = product_description
        self.product_price = product_price
        self.product_quantity = product_quantity
        self.product_category = product_category
        self.product_minorder = product_minorder
        self.added_by = added_by

        self.date_created = datetime.now()
        self.date_modified = datetime.now()

        product_item = dict(
            product_name=self.product_name,
            product_description=self.product_description,
            product_price=self.product_price,
            product_quantity=self.product_quantity,
            product_category=self.product_category,
            product_minorder=self.product_minorder,
            added_by=self.added_by,
            date_created=self.date_created,
            date_modified=self.date_modified
        )
        # check if product exists
        self.cursor.execute("SELECT * FROM products WHERE name = (%s);", (self.product_name,))
        existing_product = self.cursor.fetchone()
        if existing_product:
            self.connection.close()
            return dict(message="Product already exists", exists=True)
        save_product_sql = """INSERT INTO products 
                              (name, description, price, quantity, category, 
                              minorder, added_by, date_created, date_modified)
                              VALUES(%(product_name)s, %(product_description)s, %(product_price)s,
                              %(product_quantity)s, %(product_category)s, %(product_minorder)s,
                               %(added_by)s, %(date_created)s, %(date_modified)s);"""
        self.cursor.execute(save_product_sql, product_item)
        self.connection.commit()
        # Confirm Product saved successfully
        self.cursor.execute("SELECT * FROM products WHERE name = (%s);", (self.product_name,))
        new_saved_product = self.cursor.fetchone()
        self.connection.close()
        if not new_saved_product:
            return dict(message="Failed to save product", error=404)
        return new_saved_product

    def fetch_all_products(self):
        """Product Class method to fetch all products"""
        self.custom_cursor.execute("SELECT * FROM products;")
        products = self.custom_cursor.fetchall()
        self.connection.close()
        if not products:
            return dict(empty=404)
        all_products = []
        for row in products:
            all_products.append(dict(row))
        return all_products

    def fetch_single_product(self, productId):
        """Product Class method to fetch a single product by ID"""

        self.custom_cursor.execute("SELECT * FROM products WHERE id = (%s);", (productId,))
        existing_product = self.custom_cursor.fetchall()
        self.connection.close()
        if not existing_product:
            return dict(error=401)
        product = []
        for row in existing_product:
            product.append(dict(row))
        return product

    def fetch_single_product_by_name(self, productName):
        """Product Class method to fetch a single product by ID"""

        self.custom_cursor.execute("SELECT * FROM products WHERE name = (%s);", (productName,))
        existing_product = self.custom_cursor.fetchall()
        self.connection.close()
        if not existing_product:
            return dict(error=401)
        product = []
        for row in existing_product:
            product.append(dict(row))
        return product

    def edit_product(self, productId, product_name, product_description, product_price, product_quantity,
       product_category, product_minorder, added_by):
        """Class method to Edit Product details"""
        self.cursor.execute("SELECT * FROM products WHERE id = %s", (productId,))
        check_existing_product = self.cursor.fetchone()
        if not check_existing_product:
            return dict(message="product not found", status="failed"), 404
        # product_name = 
        date_modified = datetime.now()
        put_sql = """UPDATE products SET name = %s,
                     description = %s, price=%s, quantity = %s,
                     category = %s, minorder = %s,
                     added_by = %s, date_modified = %s WHERE id = %s"""
        self.cursor.execute(put_sql, (product_name, product_description, product_price, product_quantity, \
        product_category, product_minorder, added_by, date_modified, productId))
        self.connection.commit()
        self.connection.close()
        return 'success'

    def delete_product(self, productId):
        """Class method to delete products from inventory"""
        self.cursor.execute("SELECT * FROM products WHERE id = (%s);", (productId,))
        del_product = self.cursor.fetchone()
        if not del_product:
            return 'product id {} not found'.format(productId)
        self.cursor.execute("DELETE FROM products WHERE id = (%s);", (productId,))
        self.connection.commit()
        self.connection.close()
        return 'success'
