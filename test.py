#script to create a dummy version of the database for development
from database_manager import DatabaseManager

db = DatabaseManager()
db.insert_dummy_data()
