create_customer_table_query = """
CREATE TABLE IF NOT EXISTS customer (
	email TEXT PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	address TEXT NOT NULL,
	phone TEXT NOT NULL,
	password TEXT NOT NULL
);
"""