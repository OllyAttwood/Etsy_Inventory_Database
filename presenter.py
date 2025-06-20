from database_manager import DatabaseManager

class Presenter:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def get_filtered_products(self):
        """Get the products according to the provided filters, and tidy up the column names"""
        filtered_products = self.db_manager.view_filtered_products()
        filtered_products["column_names"] = self.process_column_names(filtered_products["column_names"])

        #***********************************************************     SORT OUT DISPLAYED COLUMN NAMES (SOME COLUMN NAMES ARE THE SAME ETC) - PERHAPS EITHER PROCESS THEM OR CHANGE NAMES IN DATABASE E.G. FROM (DESIGN.)NAME -> (DESIGN.)DESIGN_NAME

        return filtered_products

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
