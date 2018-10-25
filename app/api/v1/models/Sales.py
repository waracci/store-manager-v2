"""Sales Model and data storage functions"""
from datetime import datetime
from ..utils.database_helper import initialize_database

class Sales:
    """This class defines the Sales model and
        the various methods of manipulating the Sales data"""

    def __init__(self):
        """Initialise the Sales model with constructor"""
        self.connection = initialize_database()
        self.cursor = self.connection.cursor()

    def save_sales(self, made_by, cart, cart_price):
        """Sales method to create a sale Record"""

        self.cart = cart
        self.cart_price = cart_price
        self.made_by = made_by

        self.date_created = datetime.now()
        self.date_modified = datetime.now()

        sales_item = dict(
            cart = self.cart,
            cart_price = self.cart_price,
            made_by = self.made_by
        )

        save_sales_sql = """INSERT INTO sales INTO 
                            (cart, cart_price, made_by)
                            VALUES(%(cart)s, %(cart_price)s, %(made_by)s);"""

        self.cursor.execute(save_sales_sql, sales_item)
        self.connection.commit()
        # Confirm Sales record saved successful
        self.connection.close()
        return sales_item

    def fetch_all_sales(self):
        """Sales Class method to fetch all sales"""
        
        self.cursor.execute("SELECT * FROM sales;")
        sales = self.cursor.fetchall()
        self.connection.close()
        if not sales:
            return dict(error=401)
        return sales

    def fetch_attendant_sales_record(self, attendantId):
        """Sales class method to fetch all sales record for single attendant"""

        self.cursor.execute("SELECT * FROM sales WHERE made_by = (%s);", (attendantId,))
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
        return existing_sales
