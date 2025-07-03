from database_manager import DatabaseManager

class Presenter:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def get_filtered_items(self, filters_dict=None):
        """Get the products according to the provided filters, and tidy up the column names"""
        if filters_dict is None: #no filters applied initially
            filtered_items = self.db_manager.view_filtered_products()
        elif filters_dict["Item Type"] == "Product":
            filtered_items = self.db_manager.view_filtered_products(filters_dict["Name"], filters_dict["Design"],
                                                                    filters_dict["Theme"], filters_dict["Type"],
                                                                    filters_dict["Sub-type"], filters_dict["Colour"])
        elif filters_dict["Item Type"] == "Component":
            filtered_items = self.db_manager.view_filtered_components(filters_dict["Name"])

        filtered_items["column_names"] = self.process_column_names(filtered_items["column_names"])

        return filtered_items

    def process_column_names(self, column_names):
        """Converts the raw database column names into more human-friendly ones e.g. 'product_id' -> 'Product ID' """
        processed_column_names = []

        for column_name in column_names:
            processed_column_name = column_name.replace("_", " ")
            processed_column_name = processed_column_name.title() #capitalise
            processed_column_name = processed_column_name.replace("Id", "ID")
            processed_column_names.append(processed_column_name)

        return processed_column_names

    def get_product_designs(self):
        return self.db_manager.view_design_names()

    def get_product_themes(self):
        return self.db_manager.view_theme_names()

    def get_product_types(self):
        return self.db_manager.view_type_types()

    def get_product_sub_types(self):
        return self.db_manager.view_sub_type_names()

    def get_product_type_names(self):
        return self.db_manager.view_type_names()

    def get_product_colours(self):
        return self.db_manager.view_colour_names()

    def get_component_names(self):
        return self.db_manager.view_component_names()

    def get_low_stock_items(self, products=True, components=True):
        low_stock_items = self.db_manager.view_low_stock_items(products, components)
        low_stock_items["column_names"] = self.process_column_names(low_stock_items["column_names"])

        return low_stock_items

    def save_new_design(self, name, theme):
        """Saves a new design into the database"""
        self.db_manager.insert_new_design(name, theme)

    def save_new_product_type(self, name, type, sub_type):
        """Saves a new product type into the database"""
        self.db_manager.insert_new_product_type(name, type, sub_type)

    def save_new_component(self, name, stock, low_stock_warning):
        """Saves a new component into the database"""
        self.db_manager.insert_new_component(name, stock, low_stock_warning)

    def save_new_product(self, name, design, colour, product_type, stock, low_stock_warning, components):
        """Saves a new product into the database"""
        self.db_manager.insert_new_product(name, design, colour, product_type, stock, low_stock_warning, components)

    def update_stock_level(self, item_id, product_or_component, increase_decrease_amount):
        """Increases or decreases the stock level of the given item by the sepcified amount,
        e.g. if the current stock level is 5 and increase_decrease_amount is -1, then the new
        stock level will be 4.
        product_or_component should be either 'Product' or 'Component'.
        """
        self.db_manager.update_stock_level(item_id, product_or_component, increase_decrease_amount)

    def update_product_stock_level_and_its_components_stock_levels(self, product_id, product_stock_level_change):
        """Does the same thing as update_stock_level() but also updates the stock levels of the components used to make the product"""
        components_and_quantities = self.get_components_of_product(product_id)
        # reduce the stock level of each component that is used to make the product
        for component_id, component_quantity in components_and_quantities:
            component_update_amount = product_stock_level_change * component_quantity
            self.update_stock_level(component_id, "Component", component_update_amount)

        self.update_stock_level(product_id, "Product", product_stock_level_change) # update product stock

    def get_components_of_product(self, product_id):
        """Returns a list of the components that are used to create a product, as well as the quantity of each.
        Each component and quantity is stored as a tuple, e.g. the entire list will look like [(2, 1), (0, 2), (7, 1)]
        The first element of a tuple is the component ID and the second element is the quantity used in the product"""
        return self.db_manager.view_components_of_product(product_id)
