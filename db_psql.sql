CREATE TABLE products(
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL,
    price integer NOT NULL
);
CREATE TABLE sale_for_me(
    id serial PRIMARY KEY,
    products_id integer,
    quantity integer,
    sale_at timestamptz NOT NULL,
    foreign key(products_id) references products(id)
);

CREATE TABLE debt(
    id serial PRIMARY KEY,
    quantity integer,
    products_id integer,
    foreign key(products_id) references products(id)
);