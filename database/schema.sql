-- 1. Create the database (Run in 'postgres' default database)
CREATE DATABASE jr_journal_db;

-- 2. Connect to the new database
\c jr_journal_db

-- 3. Create the table for clinical logs
CREATE TABLE clinical_logs (
    id SERIAL PRIMARY KEY,
    log_date DATE NOT NULL,
    entry_type VARCHAR(255) NOT NULL,
    metric_value INTEGER,
    details TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
