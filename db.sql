CREATE TABLE personal_finance_tracker.user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE,
    phone VARCHAR(20),
    currency VARCHAR(10) DEFAULT 'EUR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE personal_finance_tracker.categories (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, name)
);

CREATE TABLE personal_finance_tracker.transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    category_id INTEGER,
    amount DECIMAL(12, 2) NOT NULL,
    type VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    date DATE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES personal_finance_tracker.auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES personal_finance_tracker.categories(id) ON DELETE SET NULL
);