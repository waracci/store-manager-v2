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

    def save_product(self, product_name, product_description, product_price, product_quantity,
       product_category, product_moq, added_by):
        """Product Class method to add product to list"""
        self.product_name = product_name
        self.product_description = product_description
        self.product_price = product_price
        self.product_quantity = product_quantity
        self.product_category = product_category
        self.product_moq = product_moq
        self.added_by = added_by

        self.date_created = datetime.now()
        self.date_modified = datetime.now()

        product_item = dict(
            product_name=self.product_name,
            product_description=self.product_description,
            product_price=self.product_price,
            product_quantity=self.product_quantity,
            product_category=self.product_category,
            product_moq=self.product_moq,
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
                              moq, added_by, date_created, date_modified)
                              VALUES(%(product_name)s, %(product_description)s, %(product_price)s,
                              %(product_quantity)s, %(product_category)s, %(product_moq)s,
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
        custom_cursor = self.connection.cursor(cursor_factory=extras.DictCursor)
        custom_cursor.execute("SELECT * FROM products;")
        products = custom_cursor.fetchall()
        self.connection.close()
        if not products:
            return dict(empty=404)
        all_products = []
        for row in products:
            all_products.append(dict(row))
        return all_products

    def fetch_single_product(self, productId):
        """Product Class method to fetch a single product by ID"""

        self.cursor.execute("SELECT * FROM products WHERE id = (%s);", (productId,))
        existing_product = self.cursor.fetchone()
        self.connection.close()
        if not existing_product:
            return dict(error=401)
        return dict(
            id= existing_product[0],
            name= existing_product[1], 
            description= existing_product[2],
            price=existing_product[3],
            quantity= existing_product[4],
            category= existing_product[5],
            moq= existing_product[6],
            added_by= existing_product[7],
            date_created= existing_product[8],
            modified_at= existing_product[9])

    


    def edit_product(self, productId, product_name, product_description, product_quantity,
       product_category, product_moq, added_by):
        """Class method to Edit Product details"""
        product_item_edit = dict(
            product_name=self.product_name,
            product_description=self.product_description,
            product_price=self.product_price,
            product_quantity=self.product_quantity,
            product_category=self.product_category,
            product_moq=self.product_moq,
            added_by=self.added_by,
            date_modified=datetime.now()
        )
        put_sql = """UPDATE products SET name = %(product_name)s,
         description = %(product_description)s, quantity = %(product_quantity)s,
          category = %(product_category)s, moq = %(product_moq)s,
           added_by = %(added_by)s, date_modified = %(date_modified)s WHERE id = ${productId}"""
        self.cursor.execute(put_sql, product_item_edit)
        self.connection.commit()
        self.connection.close()
        return 'success'

    def delete_product(self, productId):
        """Class method to delete products from inventory"""
        self.cursor.execute("SELECT * FROM products WHERE id = (%s);", (productId,))
        del_product = self.cursor.fetchone()
        self.cursor.execute("DELETE FROM products WHERE id = (%s);", (productId,))
        if not del_product:
            return 'product id {} not found'.format(productId)
        self.connection.commit()
        self.connection.close()
        return 'success'
