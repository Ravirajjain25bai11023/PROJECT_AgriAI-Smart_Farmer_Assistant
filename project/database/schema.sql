-- Database Schema
CREATE DATABASE smart_farmer_db;

USE smart_farmer_db;

CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100)        NOT NULL,
    email       VARCHAR(150) UNIQUE NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    image_path  VARCHAR(300)        NOT NULL,         
    disease     VARCHAR(150)        NOT NULL,         
    confidence  FLOAT               NOT NULL,         
    solution    TEXT                NOT NULL,         
    language    VARCHAR(10) DEFAULT 'en',             
    user_id     INT DEFAULT NULL,                    
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_predictions_created_at ON predictions (created_at DESC);

INSERT INTO users (name, email) VALUES
    ('Test Farmer', 'farmer@example.com');
