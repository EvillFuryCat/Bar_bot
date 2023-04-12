class BotDB:
    get_category = """
        SELECT category.name FROM category;
        """

    get_all_products = """
        SELECT products.name FROM products;
        """

    get_product = """
        SELECT products.name FROM products
        JOIN category ON products.category_id = category.id
        WHERE category.name = %(product_name)s;
        """

    add_quantity_product = """
        UPDATE debt SET quantity = quantity - 1
        WHERE products_id = (
        SELECT id FROM products
        WHERE name = %(product_name)s);
        """

    reduce_quantity_product = """
        UPDATE debt SET quantity = quantity + 1
        WHERE products_id = (
        SELECT id FROM products
        WHERE name = %(product_name)s);
        """

    get_debt = """
        WITH dt AS
        (SELECT products.category_id,
                products.name,
                debt.quantity FROM products
                JOIN debt ON products.id = debt.products_id
                WHERE NOT debt.quantity = 0)
        SELECT category.name, dt.name, dt.quantity FROM category
        JOIN dt ON category.id = dt.category_id
        ORDER BY category.id;
        """
