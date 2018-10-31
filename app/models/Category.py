"""category Model and data storage functions"""
from datetime import datetime
import psycopg2.extras as extras 
from flask_jwt_extended import get_jwt_identity

from ..utils.database_helper import initialize_database

class Category():
    """This class defines the category model and
        the various methods of manipulating the category data"""

    def __init__(self):
        """Initialise the category model with constructor"""
        self.connection = initialize_database()
        self.cursor = self.connection.cursor()
        self.custom_cursor = self.connection.cursor(cursor_factory=extras.DictCursor)

    def save_category(self, category_name, category_description):
        """category Class method to add category to list"""
        self.category_name = (category_name).lower()
        self.category_description = category_description
        self.added_by = get_jwt_identity()

        self.date_created = datetime.now()
        self.date_modified = datetime.now()

        category_item = dict(
            category_name=self.category_name,
            category_description=self.category_description,
            added_by=self.added_by,
            date_created=self.date_created,
            date_modified=self.date_modified
        )
        # check if category exists
        self.cursor.execute("SELECT * FROM categories WHERE name = (%s);", (self.category_name,))
        existing_category = self.cursor.fetchone()
        if existing_category:
            self.connection.close()
            return dict(message="category already exists", exists=True)
        save_category_sql = """INSERT INTO categories 
                              (name, description,added_by, date_created, date_modified)
                              VALUES(%(category_name)s, %(category_description)s,
                               %(added_by)s, %(date_created)s, %(date_modified)s);"""
        self.cursor.execute(save_category_sql, category_item)
        self.connection.commit()
        # Confirm category saved successfully
        self.cursor.execute("SELECT * FROM categories WHERE name = (%s);", (self.category_name,))
        new_saved_category = self.cursor.fetchone()
        self.connection.close()
        if not new_saved_category:
            return dict(message="Failed to save category", error=404)
        return new_saved_category

    def fetch_all_categories(self):
        """category Class method to fetch all categories"""
        self.custom_cursor.execute("SELECT * FROM categories;")
        categories = self.custom_cursor.fetchall()
        self.connection.close()
        if not categories:
            return dict(empty=404)
        all_categories = []
        for row in categories:
            all_categories.append(dict(row))
        return all_categories


    def fetch_single_category_by_id(self, categoryId):
        """category Class method to fetch a single category by ID"""

        self.custom_cursor.execute("SELECT * FROM categories WHERE id = (%s);", (categoryId,))
        existing_category = self.custom_cursor.fetchall()
        self.connection.close()
        if not existing_category:
            return dict(error=401)
        category = []
        for row in existing_category:
            category.append(dict(row))
        return category

    def fetch_single_category_by_name(self, categoryName):
        """category Class method to fetch a single category by ID"""

        self.custom_cursor.execute("SELECT * FROM categories WHERE name = (%s);", (categoryName,))
        existing_category = self.custom_cursor.fetchall()
        self.connection.close()
        if not existing_category:
            return dict(error=401)
        category = []
        for row in existing_category:
            category.append(dict(row))
        return category

    def edit_category(self, categoryId, category_name, category_description):
        """Class method to Edit category details"""
        self.cursor.execute("SELECT * FROM categories WHERE id = %s", (categoryId,))
        check_existing_category = self.cursor.fetchone()
        if not check_existing_category:
            return dict(message="category not found", status="failed"), 404
        added_by = get_jwt_identity() 
        date_modified = datetime.now()
        put_sql = """UPDATE categories SET name = %s,
                     description = %s, added_by = %s,
                     date_modified = %s WHERE id = %s"""
        self.cursor.execute(put_sql, (category_name, category_description, added_by, date_modified, categoryId))
        self.connection.commit()
        self.connection.close()
        return 'success'

    def delete_category(self, categoryId):
        """Class method to delete categories"""
        self.cursor.execute("SELECT * FROM categories WHERE id = (%s);", (categoryId,))
        del_category = self.cursor.fetchone()
        if not del_category:
            return 'category id {} not found'.format(categoryId)
        self.cursor.execute("DELETE FROM categories WHERE id = (%s);", (categoryId,))
        self.connection.commit()
        self.connection.close()
        return 'success'
