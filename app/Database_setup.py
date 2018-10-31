"""Class to set up application database"""
import psycopg2
from instance.config import app_configuration

class Database_Setup_Config:
    """Initialize a Database connection"""
    def __init__(self, app_config):
        database_url = app_configuration[app_config].DATABASE_CONNECTION_URL
        self.database_connection = psycopg2.connect(database_url)
        self.cursor = self.database_connection.cursor()

    def initialize_database_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            id          SERIAL PRIMARY KEY,
            email       VARCHAR(50)    UNIQUE NOT NULL,
            password    VARCHAR(100)   NOT NULL,
            role        VARCHAR(10)    NOT NULL,
            created_at  TIMESTAMP
        );''')

        # Initialize Product Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products(
            id             SERIAL PRIMARY KEY,
            name           VARCHAR(50)    UNIQUE NOT NULL,
            description    VARCHAR(100)   NOT NULL,
            price          VARCHAR(50)    NOT NULL,
            quantity       VARCHAR(50)    NOT NULL,
            category       VARCHAR(50) NOT NULL,
            moq            VARCHAR(50) NOT NULL,
            added_by       VARCHAR(50) NOT NULL,
            date_created   VARCHAR(50),
            date_modified  VARCHAR(50)
        );''')

        # Initialize Sales Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales(
            id             SERIAL PRIMARY KEY,
            cart           VARCHAR(100)    NOT NULL,
            cart_price     VARCHAR(100)   NOT NULL,
            made_by        VARCHAR(100)   NOT NULL,
            date_created   VARCHAR(100),
            date_modified  VARCHAR(100)
        );''')

        # Initialize Category Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories(
            id             SERIAL PRIMARY KEY,
            name           VARCHAR(100)    NOT NULL,
            description     VARCHAR(100)   NOT NULL,
            added_by        VARCHAR(100)   NOT NULL,
            date_created   VARCHAR(100),
            date_modified  VARCHAR(100)
        );''')

        self.database_connection.commit()
        self.cursor.close()
        self.database_connection.close()
