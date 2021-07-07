CREATE TABLE 'users' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    'username' TEXT NOT NULL,
    'hash' TEXT NOT NULL
);

CREATE TABLE expenses (
    'user_id' INTEGER,
    'name' TEXT NOT NULL,
    'amount' REAL NOT NULL,
    'frequency' TEXT NOT NULL,
    FOREIGN KEY ('user_id')
        REFERENCES users ('id')
);

CREATE TABLE income (
    'user_id' INTEGER,
    'name' TEXT NOT NULL,
    'amount' REAL NOT NULL,
    'frequency' TEXT NOT NULL,
    FOREIGN KEY ('user_id')
        REFERENCES users ('id')
);

CREATE TABLE transactions (
    'user_id' INTEGER,
    'name' TEXT NOT NULL,
    'type' TEXT NOT NULL,
    'amount' REAL NOT NULL,
    FOREIGN KEY ('user_id')
        REFERENCES users ('id')
);