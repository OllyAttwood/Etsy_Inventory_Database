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
