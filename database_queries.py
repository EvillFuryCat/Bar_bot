class BotDB:

    def get_category():
        req = """SELECT name FROM category;"""
        return req
    
    def get_all_products():
        req = """SELECT products.name FROM products;"""
        return req

    def get_product(product_name) -> str:
        req = f'''SELECT products.name FROM products
        JOIN category ON products.category_id = category.id
        WHERE category.name = '{product_name}';'''
        return req

    def update_quantity_product(product_name):
        req = f'''UPDATE debt SET quantity = quantity - 1
        WHERE products_id = (
        SELECT id FROM products
        WHERE name = '{product_name}'
        );'''
        return req
