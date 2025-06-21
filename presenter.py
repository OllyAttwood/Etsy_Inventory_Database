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

        #***********************************************************     SORT OUT DISPLAYED COLUMN NAMES (SOME COLUMN NAMES ARE THE SAME ETC) - PERHAPS EITHER PROCESS THEM OR CHANGE NAMES IN DATABASE E.G. FROM (DESIGN.)NAME -> (DESIGN.)DESIGN_NAME
        #***********************************************************     MAYBE SPECIFY WHICH ACTUAL COLUMNS ARE WANTED IN THE SELECT STATEMENTcd

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
        return self.db_manager.view_type_names()

    def get_product_sub_types(self):
        return self.db_manager.view_sub_type_names()

    def get_product_colours(self):
        return self.db_manager.view_colour_names()
