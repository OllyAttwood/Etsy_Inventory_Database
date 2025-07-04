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
                            name VARCHAR(50) NOT NULL UNIQUE,
                            theme VARCHAR(50)
                        );"""
        self.cursor.execute(design_str)

        type_str = """CREATE TABLE IF NOT EXISTS ProductType (
                          product_type_id INTEGER PRIMARY KEY,
                          name VARCHAR(50) NOT NULL UNIQUE,
                          type VARCHAR(50) NOT NULL,
                          sub_type VARCHAR(50)
                      );"""
        self.cursor.execute(type_str)

        prod_str = """CREATE TABLE IF NOT EXISTS Product (
                          product_id INTEGER PRIMARY KEY,
                          name VARCHAR(50) NOT NULL UNIQUE,
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
                               name VARCHAR(50) NOT NULL UNIQUE,
                               stock INT NOT NULL,
                               low_stock_warning INT NOT NULL
                           );"""
        self.cursor.execute(component_str)

        made_using_str = """CREATE TABLE IF NOT EXISTS MadeUsing (
                                product_id INTEGER,
                                component_id INT,
                                num_components_used INT NOT NULL,
                                PRIMARY KEY(product_id, component_id),
                                FOREIGN KEY(product_id) REFERENCES Product(product_id) ON DELETE CASCADE,
                                FOREIGN KEY(component_id) REFERENCES Component(component_id) ON DELETE CASCADE
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

    def get_column_names_most_recent_query(self):
        return [col[0] for col in self.cursor.description]

    def view_single_column_from_single_table(self, column_name, table_name, no_duplicates=True):
        """Performs a simple SELECT call with given column and table.
        *** WARNING *** - placeholders (i.e. '?') cannot be used for column or table names, therefore this function is VULNERABLE to SQL injection if exposed to the user
        """
        distinct = "DISTINCT " if no_duplicates else ""
        query = f"SELECT {distinct}{column_name} FROM {table_name} WHERE {column_name} IS NOT NULL AND {column_name} != ''" #exclude None values and empty strings
        res = self.cursor.execute(query)
        return_list = []
        for row in res.fetchall():
            return_list.append(row[0]) #[0] needed otherwise each row is a tuple rather than just the value e.g. ('Heart',)

        return return_list

    def view_design_names(self):
        return self.view_single_column_from_single_table("name", "Design")

    def view_theme_names(self):
        return self.view_single_column_from_single_table("theme", "Design")

    def view_type_types(self):
        return self.view_single_column_from_single_table("type", "ProductType")

    def view_sub_type_names(self):
        return self.view_single_column_from_single_table("sub_type", "ProductType")

    def view_type_names(self):
        return self.view_single_column_from_single_table("name", "ProductType")

    def view_colour_names(self):
        return self.view_single_column_from_single_table("colour", "Product")

    def view_component_names(self):
        return self.view_single_column_from_single_table("name", "Component")

    def view_single_column_from_single_table_with_where_clause(self, column_to_obtain, table_name, column_to_match, value_to_match):
        """Performs a simple SELECT query with a WHERE clause
        WARNING *** - placeholders (i.e. '?') cannot be used for column or table names, therefore this function is VULNERABLE to SQL injection if exposed to the user
        """
        query = f"SELECT {column_to_obtain} FROM {table_name} WHERE {column_to_match}='{value_to_match}'"
        res = self.cursor.execute(query)
        query_list = []
        for row in res.fetchall():
            query_list.append(row[0]) #[0] needed otherwise each row is a tuple rather than just the value e.g. ('Heart',)

        return query_list

    def insert_new_design(self, name, theme):
        self.insert_data("Design", [name, theme])

    def insert_new_product_type(self, name, type, sub_type):
        self.insert_data("ProductType", [name, type, sub_type])

    def insert_new_component(self, name, stock, low_stock_warning):
        self.insert_data("Component", [name, stock, low_stock_warning])

    def insert_new_product(self, name, design, colour, product_type, stock, low_stock_warning, components):
        # obtain design and product type IDs
        design_id = self.view_single_column_from_single_table_with_where_clause("design_id", "Design", "name", design)[0] # [0] because a list is returned by the function
        product_type_id = self.view_single_column_from_single_table_with_where_clause("product_type_id", "ProductType", "name", product_type)[0]

        #add the record to Product
        self.insert_data("Product", [name, colour, stock, low_stock_warning, design_id, product_type_id])

        #add any records to MadeUsing
        for component_name, quantity in components:
            product_id = self.view_single_column_from_single_table_with_where_clause("product_id", "Product", "name", name)[0]
            component_id = self.view_single_column_from_single_table_with_where_clause("component_id", "Component", "name", component_name)[0]
            self.insert_data("MadeUsing", [product_id, component_id, quantity])

    def _update_item_stock_level(self, item_id, table_name, increase_decrease_amount):
        """Increases or decreases the stock level of the given item by the sepcified amount,
        e.g. if the current stock level is 5 and increase_decrease_amount is -1, then the new
        stock level will be 4.
        This method shouldn't be called directly, rather either update_product_stock_level() or
        update_component_stock_level() should be called
        """
        id_column_name = table_name.lower() + "_id" # produces either "product_id" or "component_id"
        update_sql = f"""UPDATE {table_name}
                         SET stock = stock + ?
                         WHERE {id_column_name} = ?"""
        self.cursor.execute(update_sql, (increase_decrease_amount, item_id))
        self.connection.commit()

    def update_product_stock_level(self, product_id, increase_decrease_amount):
        self._update_item_stock_level(product_id, "Product", increase_decrease_amount)

    def update_component_stock_level(self, component_id, increase_decrease_amount):
        self._update_item_stock_level(component_id, "Component", increase_decrease_amount)


    def view_components_of_product(self, product_id):
        """Returns a list of the components that are used to create a product, as well as the quantity of each.
        Each component and quantity is stored as a tuple, e.g. the entire list will look like [(2, 1), (0, 2), (7, 1)]
        The first element of a tuple is the component ID and the second element is the quantity used in the product"""
        query = """SELECT component_id, num_components_used
                   FROM MadeUsing
                   WHERE product_id = ?"""
        res = self.cursor.execute(query, (str(product_id)))
        components_list = []
        for row in res.fetchall():
            components_list.append(row)

        return components_list

    def view_component_name_from_id(self, component_id):
        return self.view_single_column_from_single_table_with_where_clause("name", "Component", "component_id", component_id)

    def delete_product(self, product_id):
        sql = f"""DELETE FROM Product
                  WHERE product_id = ?"""
        self.cursor.execute(sql, (str(product_id)))
        self.connection.commit()

    def delete_component(self, component_id):
        sql = f"""DELETE FROM Component
                  WHERE component_id = ?"""
        self.cursor.execute(sql, (str(component_id)))
        self.connection.commit()
