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
    #like should only be True if we are using LIKE in the WHERE clause rather
    #than an equality check
    def build_where_clause(self, db_col_name, query_vals, query_value, like=False):
        clause = db_col_name

        #if we should us LIKE or = in the query
        if like:
            clause += " LIKE ?"
             #we can't put % signs directly around ? as it doesn't work
             # see https://stackoverflow.com/a/3105370
            query_value = f"%{query_value}%"
        else:
            clause += " = ?"

        clause += " AND "

        query_vals.append(query_value)
        return clause

    #queries the database for products/components
    #this method shouldn't be called directly - use view_filtered_products() or
    #view_filtered_components() instead
    def view_filtered_items(self, params_with_db_cols, query_without_where_clause, name_search=None,
                            design=None, design_theme=None, type=None, subtype=None, colour=None,
                            stock_level=None):
        product_query = query_without_where_clause
        where_clauses = []
        query_vals = []

        #loop through params and add to where clause where there is a value to filter
        for param, db_column in params_with_db_cols:
            if param:
                if param is name_search:
                    where_clauses.append(self.build_where_clause(db_column, query_vals, param, like=True))
                else:
                    where_clauses.append(self.build_where_clause(db_column, query_vals, param))

        if where_clauses:
            product_query += " WHERE " + "".join(where_clauses)
            product_query = product_query[:-4] #remove final " AND"

        res = self.cursor.execute(product_query, query_vals)
        return_list = []
        for row in res.fetchall():
            return_list.append(row)

        column_names = self.get_column_names_most_recent_query()

        return {
            "column_names": column_names,
            "data": return_list
        }

    def view_filtered_products(self, name_search=None, design=None, design_theme=None,
                               type=None, subtype=None, colour=None, stock_level=None):
        product_query = """SELECT Product.product_id, Product.name AS 'Product Name', Product.colour,
                                  Product.stock, Product.low_stock_warning, Design.name AS 'Design Name',
                                  Design.theme, ProductType.type, ProductType.sub_type
                           FROM Product
                           JOIN Design
                           ON Product.design_id=Design.design_id
                           JOIN ProductType
                           ON Product.product_type_id=ProductType.product_type_id"""

        params_with_db_cols = ((name_search, "Product.name"), (design, "Design.name"),
                               (design_theme, "Design.theme"), (type, "ProductType.type"),
                               (subtype, "ProductType.sub_type"), (colour, "Product.colour"),
                               (stock_level, "Product.stock"))

        return self.view_filtered_items(params_with_db_cols, product_query, name_search, design,
                                 design_theme, type, subtype, stock_level)

    def view_filtered_components(self, name_search=None, stock_level=None):
        product_query = """SELECT *
                           FROM Component"""
        params_with_db_cols = ((name_search, "Component.name"), (stock_level, "Component.stock"))

        return self.view_filtered_items(params_with_db_cols, product_query, name_search, stock_level)

    def view_low_stock_items(self, products=True, components=True):
        def create_query(table_name):
            return f"""SELECT name, stock, low_stock_warning
                       FROM {table_name}
                       WHERE stock <= low_stock_warning"""

        product_query = create_query("Product")
        component_query = create_query("Component")
        full_query = ""

        items_and_queries = [(products, product_query), (components, component_query)]

        for item, query in items_and_queries:
            if item:
                if len(full_query) > 0:
                    full_query += " UNION "

                full_query += query

        res = self.cursor.execute(full_query)
        return_list = []
        for row in res.fetchall():
            return_list.append(row)

        column_names = self.get_column_names_most_recent_query()

        return {
            "column_names": column_names,
            "data": return_list
        }

    #alters stock level for products/components
    #this method shouldn't be called directly - use update_product_stock_level() or
    #update_component_stock_level() instead
    def update_item_stock_level(self, item_type, id, new_stock_level):
        #names of the id fields for each table
        id_field_dict = {
            "Product": "product_id",
            "Component": "component_id"
        }

        update_sql = f"""UPDATE {item_type}
                         SET stock = ?
                         WHERE {id_field_dict[item_type]} = ?"""

        self.cursor.execute(update_sql, (new_stock_level, id))
        self.connection.commit()

    def update_product_stock_level(self, id, new_stock_level):
        self.update_item_stock_level("Product", id, new_stock_level)

    def update_component_stock_level(self, id, new_stock_level):
        self.update_item_stock_level("Component", id, new_stock_level)

    def get_column_names_most_recent_query(self):
        return [col[0] for col in self.cursor.description]

    def view_single_column_from_single_table(self, column_name, table_name, no_duplicates=True):
        """Performs a simple SELECT call with given column and table.
        *** WARNING *** - placeholders (i.e. '?') cannot be used for column or table names, therefore this function is VULNERABLE to SQL injection if exposed to the user
        """
        distinct = "DISTINCT " if no_duplicates else ""
        query = f"SELECT {distinct}{column_name} FROM {table_name} WHERE {column_name} IS NOT NULL" #exclude None values
        res = self.cursor.execute(query)
        return_list = []
        for row in res.fetchall():
            return_list.append(row[0]) #[0] needed otherwise each row is a tuple rather than just the value e.g. ('Heart',)

        return return_list

    def view_design_names(self):
        return self.view_single_column_from_single_table("name", "Design")

    def view_theme_names(self):
        return self.view_single_column_from_single_table("theme", "Design")

    def view_type_names(self):
        return self.view_single_column_from_single_table("type", "ProductType")

    def view_sub_type_names(self):
        return self.view_single_column_from_single_table("sub_type", "ProductType")

    def view_colour_names(self):
        return self.view_single_column_from_single_table("colour", "Product")

    def view_component_names(self):
        return self.view_single_column_from_single_table("name", "Component")

    def insert_new_design(self, name, theme):
        self.insert_data("Design", [name, theme])

    def insert_new_product_type(self, name, type, sub_type):
        self.insert_data("ProductType", [name, type, sub_type])
