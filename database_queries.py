class BotDB:

    def get_category():
        req = """SELECT name FROM category;"""
        return req

    def get_product(product_name) -> str:
        req = f'''SELECT products.name FROM products
        JOIN category ON products.category_id = category.id
        WHERE category.name = '{product_name}';'''
        return req

