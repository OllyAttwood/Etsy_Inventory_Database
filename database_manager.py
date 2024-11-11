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

    #inserts fake data into the tables for use during development and testing features
    def insert_dummy_data(self):
        #designs
        design_rows = [["Web", "halloween"],
                       ["Heart", None],
                       ["Planet", "space"],
                       ["Chunky chain", None]]

        for design_row in design_rows:
            self.insert_data("Design", design_row)

        res = self.cursor.execute("SELECT * FROM Design;")
        print(res.fetchall())

        #producttypes
        type_rows = [["Regular earrings", "earring", None],
                     ["Metal chain necklace", "necklace", "metal chain"],
                     ["Fully plastic necklace", "necklace", "fully plastic"],
                     ["Bauble", "bauble", None]]

        for type_row in type_rows:
            self.insert_data("ProductType", type_row)

        res = self.cursor.execute("SELECT * FROM ProductType;")
        print(res.fetchall())

        #products
        prod_rows = [["Web necklace - black", "black", 1, 1, 1, 2],
                     ["Web necklace - glow", "glow", 1, 1, 1, 2],
                     ["Web necklace - white", "white", 1, 1, 1, 2],
                     ["Web earrings - black", "black", 2, 1, 1, 1],
                     ["Web earrings - glow", "glow", 1, 1, 1, 1],
                     ["Web earrings - white", "white", 1, 1, 1, 1],
                     ["Heart earrings - blue", "blue", 3, 1, 2, 1],
                     ["Heart earrings - pink", "pink", 2, 1, 2, 1],
                     ["Heart earrings - black", "black", 1, 1, 2, 1],
                     ["Heart necklace - black", "black", 1, 1, 2, 2],
                     ["Heart necklace - pink", "pink", 1, 1, 2, 2],
                     ["Planet bauble - yellow", "yellow", 1, 1, 3, 4],
                     ["Planet bauble - blue", "blue", 1, 1, 3, 4],
                     ["Chunky chain necklace - yellow", "yellow", 1, 1, 4, 3],
                     ["Chunky chain necklace - pink", "pink", 1, 1, 4, 3],
                     ["Chunky chain necklace - pink", "pink", 1, 1, 4, 3]]

        for prod_row in prod_rows:
            self.insert_data("Product", prod_row)

        res = self.cursor.execute("SELECT * FROM Product;")
        print(res.fetchall())

        #components
        comp_rows = [["Jump ring - small", 146, 50],
                     ["Jump ring - large", 52, 15],
                     ["Earring back", 123, 50],
                     ["Earring hook - stainless steel", 77, 50],
                     ["Necklace chain - stainless steel", 8, 5],
                     ["Bauble ribbon", 23, 10]]

        for comp_row in comp_rows:
            self.insert_data("Component", comp_row)

        res = self.cursor.execute("SELECT * FROM Component;")
        print(res.fetchall())

        #MadeUsing
        made_using_rows = [[1, 5, 1], [1, 1, 2], [2, 5, 1], [2, 1, 2], [3, 5, 1],
                           [3, 1, 2], [4, 1, 4], [4, 3, 2], [4, 4, 2], [5, 1, 4],
                           [5, 3, 2], [5, 4, 2], [6, 1, 4], [6, 3, 2], [6, 4, 2],
                           [7, 1, 4], [7, 3, 2], [7, 4, 2], [8, 1, 4], [8, 3, 2],
                           [8, 4, 2], [9, 1, 4], [9, 3, 2], [9, 4, 2], [10, 1, 2],
                           [10, 5, 1], [11, 1, 2], [11, 5, 1], [12, 6, 1], [13, 6, 1]]

        for made_using_row in made_using_rows:
            self.insert_data("MadeUsing", made_using_row)

        res = self.cursor.execute("SELECT * FROM MadeUsing;")
        print(res.fetchall())
