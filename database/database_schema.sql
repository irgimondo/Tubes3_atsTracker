-- Database schema for ATS (Applicant Tracking System)
CREATE DATABASE IF NOT EXISTS ats_db;
USE ats_db;

-- Table for storing applicant profiles
CREATE TABLE IF NOT EXISTS ApplicantProfile (
    applicant_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(150),
    address TEXT,
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing application details
CREATE TABLE IF NOT EXISTS ApplicationDetail (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    applicant_id INT NOT NULL,
    application_role VARCHAR(100),
    cv_path VARCHAR(500) NOT NULL,
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_applicant_name ON ApplicantProfile(first_name, last_name);
CREATE INDEX idx_application_role ON ApplicationDetail(application_role);
CREATE INDEX idx_cv_path ON ApplicationDetail(cv_path);
