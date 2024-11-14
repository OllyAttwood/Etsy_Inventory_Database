import sqlite3

class DatabaseManager:

    #connect to database
    def __init__(self):
        self.database_file_name = "inventory.db"
        self.connection = sqlite3.connect(self.database_file_name)
        self.cursor = self.connection.cursor()

        #create tables if they don't exist
        self.create_tables()

    def close_connection(self):
        self.connection.close()

    def create_tables(self):
        self.cursor.execute("PRAGMA foreign_keys = ON") #enforces foreign key constraints

        #we use INTEGER rather than INT for primary key declaration as this makes it
        #an alias for ROWID which in sqlite3 allows us to auto-increment by providing
        #NULL as the primary key value
        design_str = """CREATE TABLE IF NOT EXISTS Design (
                            design_id INTEGER PRIMARY KEY,
                            name VARCHAR(50) NOT NULL,
                            theme VARCHAR(50)
                        );"""
        self.cursor.execute(design_str)

        type_str = """CREATE TABLE IF NOT EXISTS ProductType (
                          product_type_id INTEGER PRIMARY KEY,
                          name VARCHAR(50) NOT NULL,
                          type VARCHAR(50) NOT NULL,
                          sub_type VARCHAR(50)
                      );"""
        self.cursor.execute(type_str)

        prod_str = """CREATE TABLE IF NOT EXISTS Product (
                          product_id INTEGER PRIMARY KEY,
                          name VARCHAR(50) NOT NULL,
                          colour VARCHAR(30) NOT NULL,
                          stock INT NOT NULL,
                          low_stock_warning INT NOT NULL,
                          design_id INT NOT NULL,
                          product_type_id INT NOT NULL,
                          FOREIGN KEY(design_id) REFERENCES Design(design_id),
                          FOREIGN KEY(product_type_id) REFERENCES ProductType(product_type_id)
                      );"""
        self.cursor.execute(prod_str)

        component_str = """CREATE TABLE IF NOT EXISTS Component (
                               component_id INTEGER PRIMARY KEY,
                               name VARCHAR(50) NOT NULL,
                               stock INT NOT NULL,
                               low_stock_warning INT NOT NULL
                           );"""
        self.cursor.execute(component_str)

        made_using_str = """CREATE TABLE IF NOT EXISTS MadeUsing (
                                product_id INTEGER,
                                component_id INT,
                                num_components_used INT NOT NULL,
                                PRIMARY KEY(product_id, component_id),
                                FOREIGN KEY(product_id) REFERENCES Product(product_id),
                                FOREIGN KEY(component_id) REFERENCES Component(component_id)
                            );"""
        self.cursor.execute(made_using_str)

        self.connection.commit()

    #insert a single row of data to a table
    #user must not be able to type in table_name directly as SQL injection placeholder
    #doesn't work with table names - table_name must be picked from drop-down list
    def insert_data(self, table_name, data_row):
        #as data_row has variable number of elements depending on which table is
        #being inserted into, the number of question marks in the insertion
        #string must also vary
        question_mark_str = "?"
        for _ in range(len(data_row) - 1):
            question_mark_str += ", ?"

        #we use NULL as the first value so that the primary key is auto incremented
        #apart from the MadeUsing table which has a composite key so can't be
        #auto incremented
        if table_name != "MadeUsing":
            question_mark_str = "NULL, " + question_mark_str

        insert_str = f"INSERT INTO {table_name} VALUES ({question_mark_str})"
        self.cursor.execute(insert_str, data_row)

        self.connection.commit()

    #creates each step of the WHERE clause
    def build_where_clause(self, db_col_name, query_vals, query_value):
        clause = f"{db_col_name}= ? AND "
        query_vals.append(query_value)
        return clause

    #queries the database for products
    def view_filtered_products(self, name_search=None, design=None, design_theme=None,
                               type=None, subtype=None, colour=None, stock_level=None):
        params = (name_search, design, design_theme, type, subtype, colour,
                  stock_level)
        product_query = """SELECT *
                           FROM Product
                           JOIN Design
                           ON Product.design_id=Design.design_id
                           JOIN ProductType
                           ON Product.product_type_id=ProductType.product_type_id"""
        query_vals = []

        #if at least one filter should be applied, add the WHERE clause
        if not all([param is None for param in params]):
            product_query += " WHERE "

            if name_search:
                product_query += self.build_where_clause("Product.name", query_vals, name_search)
            if design:
                product_query += self.build_where_clause("Design.name", query_vals, design)
            if design_theme:
                product_query += self.build_where_clause("Design.theme", query_vals, design_theme)
            if type:
                product_query += self.build_where_clause("ProductType.type", query_vals, type)
            if subtype:
                product_query += self.build_where_clause("ProductType.sub_type", query_vals, subtype)
            if colour:
                product_query += self.build_where_clause("Product.colour", query_vals, colour)
            if stock_level:
                product_query += self.build_where_clause("Product.stock", query_vals, stock_level)

            product_query = product_query[:-4] #remove final " AND"


        res = self.cursor.execute(product_query, query_vals)
        for row in res.fetchall():
            print(row)
