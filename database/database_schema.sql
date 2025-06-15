-- Database schema for ATS (Applicant Tracking System)
-- Updated schema for improved consistency with specification requirements

CREATE DATABASE IF NOT EXISTS ats_db;
USE ats_db;

-- Table for storing applicant profiles (as per specification)
CREATE TABLE IF NOT EXISTS ApplicantProfile (
    applicant_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(150) UNIQUE,
    address TEXT,
    date_of_birth DATE,
    summary TEXT,
    skills TEXT,
    experience TEXT,
    education TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table for storing application details (as per specification)
CREATE TABLE IF NOT EXISTS ApplicationDetail (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    applicant_id INT NOT NULL,
    application_role VARCHAR(100) NOT NULL,
    cv_path VARCHAR(500) NOT NULL,
    application_status ENUM('pending', 'reviewed', 'shortlisted', 'rejected') DEFAULT 'pending',
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id) ON DELETE CASCADE
);

-- Additional table for keyword tracking (for analytics)
CREATE TABLE IF NOT EXISTS SearchKeywords (
    keyword_id INT AUTO_INCREMENT PRIMARY KEY,
    keyword VARCHAR(100) NOT NULL,
    search_count INT DEFAULT 1,
    last_searched TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_keyword (keyword)
);

-- Create indexes for better performance
CREATE INDEX idx_applicant_name ON ApplicantProfile(first_name, last_name);
CREATE INDEX idx_applicant_email ON ApplicantProfile(email);
CREATE INDEX idx_application_role ON ApplicationDetail(application_role);
CREATE INDEX idx_cv_path ON ApplicationDetail(cv_path);
CREATE INDEX idx_application_status ON ApplicationDetail(application_status);
CREATE INDEX idx_applied_date ON ApplicationDetail(applied_date);

-- Create view for easy joins
CREATE VIEW ApplicantDetails AS
SELECT 
    ap.applicant_id,
    ap.first_name,
    ap.last_name,
    ap.phone_number,
    ap.email,
    ap.address,
    ap.summary,
    ap.skills,
    ap.experience,
    ap.education,
    ad.application_id,
    ad.application_role,
    ad.cv_path,
    ad.application_status,
    ad.applied_date
FROM ApplicantProfile ap
LEFT JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id;
