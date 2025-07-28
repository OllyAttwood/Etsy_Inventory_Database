"""Tests for the database_manager.py functions.

If the command "pytest" doesn't work (as it didn't for me), use
"python -m pytest" instead.

See https://www.tutorialspoint.com/pytest/index.htm for more help
"""

import pytest
from database_manager import DatabaseManager
import sqlite3

@pytest.fixture
def db():
    """Sets up the database temporarily in memory, for use by the test functions"""
    db = DatabaseManager(save_database_in_memory=True) #setup
    yield db # provides db to the test
    db.close_connection() #teardown

def test_insert_data(db):
    """Tests the insert_data() function"""
    table_name = "Component"
    component_name = "TestComponent"
    stock = 4
    low_stock = 2
    db.insert_data(table_name, [component_name, stock, low_stock])
    db_row = db.view_filtered_components()["data"][0]

    assert "TestComponent" == db_row[1]
    assert stock == db_row[2]
    assert low_stock == db_row[3]

def test_insert_new_design(db):
    """Tests the insert_new_design() function"""
    name = "Name"
    theme = "Theme"
    db.insert_new_design(name, theme)
    retrieved_design_name = db.view_design_names()[0]
    retrieved_theme = db.view_theme_names()[0]

    assert name == retrieved_design_name
    assert theme == retrieved_theme

def test_insert_new_product_type(db):
    """Tests the insert_new_product_type() function"""
    name = "Name"
    type = "Type"
    sub_type = "SubType"
    db.insert_new_product_type(name, type, sub_type)
    retrieved_name = db.view_type_names()[0]
    retrieved_type = db.view_type_types()[0]
    retrieved_subtype = db.view_sub_type_names()[0]

    assert name == retrieved_name
    assert type == retrieved_type
    assert sub_type == retrieved_subtype

def test_insert_new_component(db):
    """Tests the insert_new_component() function"""
    name = "Name"
    stock = 1
    low_stock = 0
    db.insert_new_component(name, stock, low_stock)
    retrieved_name = db.view_component_names()[0]

    assert name == retrieved_name

def test_insert_new_product(db):
    """Tests the insert_new_product() function"""
    product_name = "ProductName"
    product_prequisite_dict = _setup_product_prerequisites(db)
    _insert_new_product(product_name, db, product_prequisite_dict)

    product_row = db.view_filtered_products()["data"][0]
    retrieved_component_ids_and_quantities = db.view_components_of_product(1)
    retrieved_component_quantities = [id_and_quantity[1] for id_and_quantity in retrieved_component_ids_and_quantities]

    assert product_name == product_row[1]
    assert product_prequisite_dict["colour"] == product_row[2]
    assert product_prequisite_dict["stock"] == product_row[3]
    assert product_prequisite_dict["low_stock"] == product_row[4]
    assert product_prequisite_dict["design_name"] == product_row[5]
    assert product_prequisite_dict["design_theme"] == product_row[6]
    assert product_prequisite_dict["type_type"] == product_row[7]
    assert product_prequisite_dict["sub_type"] == product_row[8]
    assert product_prequisite_dict["component1_quantity"] == retrieved_component_quantities[0]
    assert product_prequisite_dict["component2_quantity"] == retrieved_component_quantities[1]

def test_view_filtered_products(db):
    """Tests the view_filtered_products function"""
    product1_name = "Product1Name"
    product2_name = "Product2Name"
    product_prequisite_dict = _setup_product_prerequisites(db)
    _insert_new_product(product1_name, db, product_prequisite_dict)
    _insert_new_product(product2_name, db, product_prequisite_dict)

    filtered_rows = db.view_filtered_products(name_search=product2_name)["data"]

    assert len(filtered_rows) == 1
    assert filtered_rows[0][1] == product2_name

def test_view_filtered_components(db):
    """Tests the view_filtered_components() function"""
    name1 = "Name1"
    stock1 = 1
    low_stock1 = 0
    name2 = "Name2"
    stock2 = 3
    low_stock2 = 2

    db.insert_new_component(name1, stock1, low_stock1)
    db.insert_new_component(name2, stock2, low_stock2)

    filtered_rows = db.view_filtered_components(stock_level=stock2)["data"]

    assert len(filtered_rows) == 1
    assert filtered_rows[0][1] == name2

def test_view_low_stock_items(db):
    """Tests the view_low_stock_items() function"""
    product1_name = "Product1Name"
    product2_name = "Product2Name"
    product1_prequisite_dict = _setup_product_prerequisites(db)
    product2_prequisite_dict = product1_prequisite_dict.copy() # needed so that stock level can be adjusted for only product2
    product2_prequisite_dict["stock"] = 1
    _insert_new_product(product1_name, db, product1_prequisite_dict)
    _insert_new_product(product2_name, db, product2_prequisite_dict)

    low_stock_rows = db.view_low_stock_items()["data"]
    low_stock_item_names = [product2_name, product1_prequisite_dict["component1_name"]]

    assert len(low_stock_rows) == 2
    assert low_stock_rows[0][0] in low_stock_item_names
    assert low_stock_rows[1][0] in low_stock_item_names

def test_update_product_stock_level(db):
    """Tests the update_product_stock_level() function"""
    product1_name = "Product1Name"
    product2_name = "Product2Name"
    product_prequisite_dict = _setup_product_prerequisites(db)
    _insert_new_product(product1_name, db, product_prequisite_dict)
    _insert_new_product(product2_name, db, product_prequisite_dict)

    stock_change_amount = -1
    db.update_product_stock_level(2, stock_change_amount)

    product_rows = db.view_filtered_products()["data"]

    assert product_rows[0][3] == product_prequisite_dict["stock"]
    assert product_rows[1][3] == (product_prequisite_dict["stock"] + stock_change_amount)

def test_update_component_stock_level(db):
    """Tests the update_component_stock_level() function"""
    product_name = "ProductName"
    product_prequisite_dict = _setup_product_prerequisites(db)
    _insert_new_product(product_name, db, product_prequisite_dict)

    stock_change_amount = -1
    db.update_component_stock_level(2, stock_change_amount)

    component_rows = db.view_filtered_components()["data"]

    assert component_rows[0][2] == product_prequisite_dict["component1_stock"]
    assert component_rows[1][2] == (product_prequisite_dict["component2_stock"] + stock_change_amount)

def test_delete_product(db):
    """Tests the delete_product() function"""
    product1_name = "Product1Name"
    product2_name = "Product2Name"
    product_prequisite_dict = _setup_product_prerequisites(db)
    _insert_new_product(product1_name, db, product_prequisite_dict)
    _insert_new_product(product2_name, db, product_prequisite_dict)

    db.delete_product(1)

    product_rows = db.view_filtered_products()["data"]

    assert len(product_rows) == 1
    assert product_rows[0][1] == product2_name

def test_delete_component(db):
    """Tests the delete_component() function"""
    product_prequisite_dict = _setup_product_prerequisites(db)

    db.delete_component(2)

    component_rows = db.view_filtered_components()["data"]

    assert len(component_rows) == 1
    assert component_rows[0][1] == product_prequisite_dict["component1_name"]

@pytest.mark.parametrize("valid_table_name", ["Design", "ProductType", "Product", "Component", "MadeUsing"])
def test_validate_table_name_with_valid_name(db, valid_table_name):
    """Tests the validate_table_name() function by testing it with valid table names"""
    db.validate_table_name(valid_table_name)

@pytest.mark.parametrize("invalid_table_name", ["123", "£$%", "1; DROP TABLE Product"])
def test_validate_table_name_with_invalid_name(db, invalid_table_name):
    """Tests the validate_table_name() function by testing it with invalid table names"""
    with pytest.raises(sqlite3.DataError): # this makes the test fail if an error is not raised
        db.validate_table_name(invalid_table_name)

@pytest.mark.parametrize("valid_column_name", ["product_id", "name", "sub_type", "stock"])
def test_validate_column_name_with_valid_name(db, valid_column_name):
    """Tests the validate_column_names() function by testing it with valid column names"""
    db.validate_column_names([valid_column_name])

@pytest.mark.parametrize("invalid_column_name", ["123", "£$%", "1; DROP TABLE Product"])
def test_validate_column_name_with_invalid_name(db, invalid_column_name):
    """Tests the validate_column_names() function by testing it with invalid column names"""
    with pytest.raises(sqlite3.DataError): # this makes the test fail if an error is not raised
        db.validate_column_names([invalid_column_name])

def test_get_all_table_names(db):
    """Test the _get_all_table_names() function"""
    table_names = ["Design", "ProductType", "Product", "Component", "MadeUsing"]
    retrieved_table_names = db._get_all_table_names()

    assert len(table_names) == len(retrieved_table_names)
    assert set(table_names) == set(retrieved_table_names)

# ------------------------------------------     HELPER FUNCTIONS     ------------------------------------------

def _setup_product_prerequisites(database):
    """Helper function to prepare the database for inserting products by inserting the prerequisite entries in the other tables.
    Returns a dictionary with the inserted values so that the test functions can check for correct database functionality.
    """
    design_name = "DesignName"
    design_theme = "DesignTheme"
    colour = "Colour"
    type_name = "TypeName"
    type_type = "Type"
    sub_type = "SubType"
    stock = 3
    low_stock = 2
    component1_name = "Component1Name"
    component1_stock = 2
    component1_low_stock = 3
    component1_quantity = 1
    component2_name = "Component2Name"
    component2_stock = 10
    component2_low_stock = 4
    component2_quantity = 2

    database.insert_new_design(design_name, design_theme)
    database.insert_new_product_type(type_name, type_type, sub_type)
    database.insert_new_component(component1_name, component1_stock, component1_low_stock)
    database.insert_new_component(component2_name, component2_stock, component2_low_stock)

    return {
        "design_name": design_name,
        "design_theme": design_theme,
        "colour": colour,
        "type_name": type_name,
        "type_type": type_type,
        "sub_type": sub_type,
        "stock": stock,
        "low_stock": low_stock,
        "component1_name": component1_name,
        "component1_stock": component1_stock,
        "component1_low_stock": component1_low_stock,
        "component1_quantity": component1_quantity,
        "component2_name": component2_name,
        "component2_stock": component2_stock,
        "component2_low_stock": component2_low_stock,
        "component2_quantity": component2_quantity
    }

def _insert_new_product(product_name, database, product_prequisite_dict):
    """Inserts a new product row into the database with the given name and other fields obtained
    from product_prequisite_dict - therefore all products inserted using this funtion are identical
    other than their names and IDs.
    """
    database.insert_new_product(
        product_name,
        product_prequisite_dict["design_name"],
        product_prequisite_dict["colour"],
        product_prequisite_dict["type_name"],
        product_prequisite_dict["stock"],
        product_prequisite_dict["low_stock"],
        [
            (product_prequisite_dict["component1_name"], product_prequisite_dict["component1_quantity"]),
            (product_prequisite_dict["component2_name"], product_prequisite_dict["component2_quantity"])
        ]
    )
