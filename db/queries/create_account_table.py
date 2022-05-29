create_account_table = """
CREATE TABLE IF NOT EXISTS bank_account (
    email TEXT NOT NULL,
    number TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    name TEXT NOT NULL,
    balance REAL NOT NULL,
    FOREIGN KEY (email) REFERENCES customer(email)
);
"""
