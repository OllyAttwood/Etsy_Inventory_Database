# ---   THIS SCRIPT HAS NOT BEEN KEPT UP TO DATE SO PROBABLY DOESN'T WORK WITH UPDATED CODE   ---

#script to create a dummy version of the database for development
from database_manager import DatabaseManager

#inserts fake data into the tables for use during development and testing features
def insert_dummy_data(db):
    #designs
    design_rows = [["Web", "halloween"],
                   ["Heart", None],
                   ["Planet", "space"],
                   ["Chunky chain", None]]

    for design_row in design_rows:
        db.insert_data("Design", design_row)

    #producttypes
    type_rows = [["Regular earrings", "earring", None],
                 ["Metal chain necklace", "necklace", "metal chain"],
                 ["Fully plastic necklace", "necklace", "fully plastic"],
                 ["Bauble", "bauble", None]]

    for type_row in type_rows:
        db.insert_data("ProductType", type_row)

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
                 ["Chunky chain necklace - blue", "blue", 1, 1, 4, 3]]

    for prod_row in prod_rows:
        db.insert_data("Product", prod_row)

    #components
    comp_rows = [["Jump ring - small", 146, 50],
                 ["Jump ring - large", 12, 15],
                 ["Earring back", 123, 50],
                 ["Earring hook - stainless steel", 46, 50],
                 ["Necklace chain - stainless steel", 8, 5],
                 ["Bauble ribbon", 23, 10]]

    for comp_row in comp_rows:
        db.insert_data("Component", comp_row)

    #MadeUsing
    made_using_rows = [[1, 5, 1], [1, 1, 2], [2, 5, 1], [2, 1, 2], [3, 5, 1],
                       [3, 1, 2], [4, 1, 4], [4, 3, 2], [4, 4, 2], [5, 1, 4],
                       [5, 3, 2], [5, 4, 2], [6, 1, 4], [6, 3, 2], [6, 4, 2],
                       [7, 1, 4], [7, 3, 2], [7, 4, 2], [8, 1, 4], [8, 3, 2],
                       [8, 4, 2], [9, 1, 4], [9, 3, 2], [9, 4, 2], [10, 1, 2],
                       [10, 5, 1], [11, 1, 2], [11, 5, 1], [12, 6, 1], [13, 6, 1]]

    for made_using_row in made_using_rows:
        db.insert_data("MadeUsing", made_using_row)

db = DatabaseManager()

#insert_dummy_data(db)
#db.view_filtered_products(name_search="Web necklace - black", design="Web", design_theme="halloween", type="necklace", subtype="metal chain", colour="black", stock_level=1)
#db.view_filtered_products(name_search="Web necklace", design="Web", design_theme="halloween", type="necklace", subtype="metal chain", stock_level=1)
#db.view_filtered_components(name_search="Jump ring")
#db.update_component_stock_level(2, 7) #Jump ring - large
db.update_product_stock_level(14, 0) #chunky yellow chain necklace
print(db.view_low_stock_items())

db.close_connection()
