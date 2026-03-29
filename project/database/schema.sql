-- ============================================
-- AI Smart Farmer Assistant - Database Schema
-- ============================================

-- Create the database
CREATE DATABASE IF NOT EXISTS smart_farmer_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE smart_farmer_db;

-- -----------------------------------------------
-- Table: users (optional, for future auth)
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100)        NOT NULL,
    email       VARCHAR(150) UNIQUE NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------
-- Table: predictions (core table)
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS predictions (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    image_path  VARCHAR(300)        NOT NULL,         -- path to saved image
    disease     VARCHAR(150)        NOT NULL,         -- detected disease name
    confidence  FLOAT               NOT NULL,         -- confidence 0–100
    solution    TEXT                NOT NULL,         -- recommended treatment
    language    VARCHAR(10) DEFAULT 'en',             -- 'en' or 'hi'
    user_id     INT DEFAULT NULL,                     -- FK to users (optional)
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Index for faster history queries
CREATE INDEX idx_predictions_created_at ON predictions (created_at DESC);

-- -----------------------------------------------
-- Sample data (optional, for testing)
-- -----------------------------------------------
INSERT INTO users (name, email) VALUES
    ('Test Farmer', 'farmer@example.com');
