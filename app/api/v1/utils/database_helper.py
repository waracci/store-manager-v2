import os
import psycopg2

from instance.config import app_configuration


def initialize_database():
    """Creates an active connection to the database"""
    app_environment = os.environ['APP_SETTINGS']
    DATABASE_URI = app_configuration[app_environment].DATABASE_CONNECTION_URL

    database_connection = psycopg2.connect(DATABASE_URI)
    return database_connection

