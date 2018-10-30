"""Sales Model and data storage functions"""
from flask import json
from datetime import datetime
import psycopg2.extras as extras
from psycopg2.extras import Json, DictCursor
from ..utils.database_helper import initialize_database

class Sales:
    """This class defines the Sales model and
        the various methods of manipulating the Sales data"""

    def __init__(self):
        """Initialise the Sales model with constructor"""
        self.connection = initialize_database()
        self.cursor = self.connection.cursor()
        
    def sell_single_product(self, productId, product_quantity, made_by):
        """Class method to sell single product """
        self.cursor.execute("SELECT * FROM products WHERE id = (%s);", (productId,))
        sale_item = self.cursor.fetchone()
        if not sale_item:
            return dict(unavailable=404)

        amount_available_inventory = int(sale_item[4])
        print("amount available inventory {}".format(amount_available_inventory))
        product_sale_quantity = int(product_quantity)
        print(product_sale_quantity)

        # Check if item quantity exists
        if product_sale_quantity > amount_available_inventory:
            return dict(insufficient=400, quantity=sale_item[4])

        remaining_quantity = amount_available_inventory - product_sale_quantity 
        print("remaining {}".format(remaining_quantity)) 
       
        if remaining_quantity < 0:
            return dict(remaining=remaining_quantity)

        existing_product_price = int(sale_item[3])
        sale_total = existing_product_price * product_sale_quantity

        self.cursor.execute("UPDATE products SET quantity = (%s) WHERE id = (%s);", (remaining_quantity, productId))

        # Record a sale 
        self.cart = {
           "product_name": sale_item[1],
           "product_id": sale_item[0],
           "product_quantity": product_quantity 
        }
        self.cart_price = sale_total
        self.made_by = made_by

        self.date_created = datetime.now()
        self.date_modified = datetime.now()
        
        save_sales_sql = """INSERT INTO sales 
                            (cart, cart_price, made_by, date_created, date_modified)
                            VALUES(%s, %s, %s, %s, %s);"""

        self.cursor.execute(save_sales_sql, [Json(self.cart), self.cart_price, self.made_by, self.date_created, self.date_modified])

        self.connection.commit()
        self.connection.close()
        return dict(
            sale_total=sale_total,
            product_name=sale_item[1],
            stock_level="{} products remaining in inventory".format(remaining_quantity)
        )

    def fetch_all_sales(self):
        """Sales Class method to fetch all sales"""
        
        custom_cursor = self.connection.cursor(cursor_factory=extras.DictCursor)
        custom_cursor.execute("SELECT * FROM sales;")
        sales = custom_cursor.fetchall()
        self.connection.close()
        if not sales:
            return dict(empty=404)
        all_sales = []
        for row in sales:
            # print(row)
            all_sales.append(dict(row))
        return all_sales

    def fetch_attendant_sales_record(self, attendantEmail):
        """Sales class method to fetch all sales record for single attendant"""

        self.cursor.execute("SELECT * FROM sales WHERE made_by = (%s);", (attendantEmail,))
        attendant_sales = self.cursor.fetchone()
        self.connection.close()
        if not attendant_sales:
            return dict(error=401)
        return attendant_sales

    def fetch_single_sales_record(self, salesId):
        """Sales class method to fetch a single sales record"""

        self.cursor.execute("SELECT * FROM sales WHERE id = (%s);", (salesId,))
        existing_sales = self.cursor.fetchone()
        self.connection.close()
        if not existing_sales:
            return dict(error=401)
        return dict(
            id=existing_sales[0],
            cart = json.loads(existing_sales[1]),
            cart_price = existing_sales[2],
            made_by = existing_sales[3],  
            date_created=existing_sales[4],
            date_modified=existing_sales[5])

    def delete_sale(self, saleId):
        """Class method to delete sales records"""
        self.cursor.execute("SELECT * FROM sales WHERE id = (%s);", (saleId,))
        del_sale = self.cursor.fetchone()
        self.cursor.execute("DELETE FROM sales WHERE id = (%s);", (saleId,))
        if not del_sale:
            return 'sale id {} not found'.format(saleId)
        self.connection.commit()
        self.connection.close()
        return 'success'
