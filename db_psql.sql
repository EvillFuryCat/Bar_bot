
CREATE TABLE category(
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL UNIQUE,
);

CREATE TABLE products(
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL UNIQUE,
    price integer NOT NULL,
    category_id integer NOT NULL,
    FOREIGN KEY(category_id) REFERENCES category(id)
);

CREATE TABLE debt(
    id serial PRIMARY KEY,
    quantity integer,
    products_id integer,
    sale_at timestamptz NOT NULL,
    FOREIGN KEY(products_id) REFERENCES products(id)
);