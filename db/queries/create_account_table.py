create_account_table = """
CREATE TABLE IF NOT EXISTS account (
    id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    account_number TEXT NOT NULL,
    account_type TEXT NOT NULL,
    balance REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(id)
);
"""