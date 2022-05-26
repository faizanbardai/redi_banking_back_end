create_customer_table_query = """
CREATE TABLE IF NOT EXISTS customer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  address TEXT NOT NULL,
  phone TEXT NOT NULL,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  initial_balance REAL NOT NULL
);
"""