CREATE TABLE customers (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    email VARCHAR UNIQUE,
    phone VARCHAR,
    join_date TIMESTAMP
);

CREATE TABLE cards (
    id VARCHAR PRIMARY KEY,
    type VARCHAR,
    status VARCHAR,
    balance FLOAT,
    issue_date TIMESTAMP,
    customer_id VARCHAR,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE cases (
    id VARCHAR PRIMARY KEY,
    customer_id VARCHAR,
    type VARCHAR,
    status VARCHAR,
    priority VARCHAR,
    assigned_to VARCHAR,
    created_at TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE trips (
    id VARCHAR PRIMARY KEY,
    card_id VARCHAR,
    station VARCHAR,
    type VARCHAR,
    amount FLOAT,
    status VARCHAR,
    timestamp TIMESTAMP,
    FOREIGN KEY (card_id) REFERENCES cards(id)
); 