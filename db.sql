CREATE TABLE finance.user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE,
    phone VARCHAR(20),
    currency VARCHAR(10) DEFAULT 'EUR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);