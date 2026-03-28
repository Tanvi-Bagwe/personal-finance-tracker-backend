DROP SCHEMA IF EXISTS personal_finance_tracker;

CREATE SCHEMA IF NOT EXISTS personal_finance_tracker
    AUTHORIZATION postgres;

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


CREATE TABLE personal_finance_tracker.reminders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    amount DECIMAL(12, 2),
    due_date DATE NOT NULL,
    reminder_days_before INT DEFAULT 1,
    is_read BOOLEAN DEFAULT FALSE,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reminder_user FOREIGN KEY(user_id) REFERENCES personal_finance_tracker.auth_user(id) ON DELETE CASCADE
);

ALTER TABLE personal_finance_tracker.reminders
ADD COLUMN last_notified_at DATE;

CREATE TABLE personal_finance_tracker.password_reset_otp (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    otp VARCHAR(6) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES personal_finance_tracker.auth_user(id) ON DELETE CASCADE
);

CREATE INDEX idx_otp_user_id ON personal_finance_tracker.password_reset_otp(user_id);
