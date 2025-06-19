from database_manager import DatabaseManager

class Presenter:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def get_filtered_products(self):
        """Get the products according to the provided filters, and tidy up the column names"""
        filtered_products = self.db_manager.view_filtered_products()
        filtered_products["column_names"] = self.process_column_names(filtered_products["column_names"])

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
