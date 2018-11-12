"""Sales Model and data storage functions"""
from flask import json
from datetime import datetime
import psycopg2.extras as extras
from psycopg2.extras import Json, DictCursor
from flask_jwt_extended import get_jwt_identity
from ..models.User import User
from ..utils.database_helper import initialize_database

class Sales:
    """This class defines the Sales model and
        the various methods of manipulating the Sales data"""

    def __init__(self):
        """Initialise the Sales model with constructor"""
        self.connection = initialize_database()
        self.cursor = self.connection.cursor()
        self.custom_cursor = self.connection.cursor(cursor_factory=extras.DictCursor)
        
    def sell_single_product(self, productId, product_quantity, made_by):
        """Class method to sell single product """
        self.cursor.execute("SELECT * FROM products WHERE id = (%s);", (productId,))
        sale_item = self.cursor.fetchone()
        if not sale_item:
            return dict(unavailable=404)
        amount_available_inventory = int(sale_item[4])
        product_sale_quantity = int(product_quantity)
        if product_sale_quantity > amount_available_inventory:
            return dict(insufficient=400, quantity=sale_item[4])
        remaining_quantity = amount_available_inventory - product_sale_quantity        
        if remaining_quantity < 0:
            return dict(remaining=remaining_quantity)
        existing_product_price = int(sale_item[3])
        sale_total = existing_product_price * product_sale_quantity
        update_sql = "UPDATE products SET quantity = (%s) WHERE id = (%s);"
        self.cursor.execute(update_sql, (remaining_quantity, productId))

        self.product_name = sale_item[1]
        self.product_id = sale_item[0]
        self.product_quantity = product_quantity
        self.sales_total = sale_total
        self.made_by = made_by

        self.date_created = datetime.now()
        self.date_modified = datetime.now()
        
        save_sales_sql = """INSERT INTO sales 
                            (product_name, product_id, product_quantity, sales_total, made_by, 
                            date_created, date_modified) VALUES(%s, %s, %s, %s, %s, %s, %s);"""

        self.cursor.execute(save_sales_sql, (self.product_name, self.product_id, self.product_quantity, self.sales_total, 
                                            self.made_by, self.date_created, self.date_modified))

        self.connection.commit()
        self.connection.close()
        return dict(
            sale_total=sale_total,
            product_name=sale_item[1],
            stock_level="{} products remaining in inventory".format(remaining_quantity),
            status="ok"
        )

    def fetch_all_sales(self):
        """Sales Class method to fetch all sales"""
        all_sales = []        
        
        check_user_role = User().get_single_user(get_jwt_identity())
        if not check_user_role:
            return dict(message="user not found", status="failed"), 404
        if check_user_role[3] == 'attendant':
            get_attendant_sales_sql = "SELECT * FROM sales WHERE made_by = (%s);"
            self.custom_cursor.execute(get_attendant_sales_sql, (get_jwt_identity(),))
            attendant_sales = self.custom_cursor.fetchall()
            self.connection.close()
            if not attendant_sales:
                return dict(empty=401)
            for row in attendant_sales:
                all_sales.append(dict(row))
            return all_sales
        self.custom_cursor.execute("SELECT * FROM sales;")
        sales = self.custom_cursor.fetchall()
        self.connection.close()
        if not sales:
            return dict(empty=404)
        for row in sales:
            all_sales.append(dict(row))
        return all_sales

    def fetch_single_sales_record(self, salesId):
        """Sales class method to fetch a single sales record"""
        check_user_attendant = User().get_single_user(get_jwt_identity())
        if not check_user_attendant:
            return dict(message="user not found", status="failed"), 404
        if check_user_attendant[3] == 'attendant':
            self.custom_cursor.execute("SELECT * FROM sales WHERE id = (%s);", (salesId,))
            existing_sales = self.custom_cursor.fetchall()
            self.connection.close()
            if existing_sales[0][5] == get_jwt_identity():
                sale_record = []
                for row in existing_sales:
                    sale_record.append(dict(row))
                return sale_record
            return dict(unauthorized=True)
        self.custom_cursor.execute("SELECT * FROM sales WHERE id = (%s);", (salesId,))
        existing_sales = self.custom_cursor.fetchall()
        self.connection.close()
        if not existing_sales:
            return dict(error=401)
        sale_record = []
        for row in existing_sales:
            sale_record.append(dict(row))
        return sale_record

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
