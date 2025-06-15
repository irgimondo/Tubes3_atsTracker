-- Database schema for ATS (Applicant Tracking System)
-- Schema compatible with tubes3_seeding.sql

SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';

CREATE DATABASE IF NOT EXISTS ats_db;
USE ats_db;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS ApplicationDetail;
DROP TABLE IF EXISTS ApplicantProfile;

SET FOREIGN_KEY_CHECKS = 1;

-- Table for storing applicant profiles (exactly matching tubes3_seeding.sql)
CREATE TABLE ApplicantProfile (
    applicant_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    address VARCHAR(255),
    phone_number VARCHAR(20)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table for storing application details (exactly matching tubes3_seeding.sql)
CREATE TABLE ApplicationDetail (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    applicant_id INT NOT NULL,
    application_role VARCHAR(100),
    cv_path TEXT,
    FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create indexes for better performance
CREATE INDEX idx_applicant_name ON ApplicantProfile(first_name, last_name);
CREATE INDEX idx_applicant_phone ON ApplicantProfile(phone_number);
CREATE INDEX idx_application_role ON ApplicationDetail(application_role);
CREATE INDEX idx_cv_path ON ApplicationDetail(cv_path(255));
CREATE INDEX idx_applicant_detail ON ApplicationDetail(applicant_id);

-- Additional useful views
CREATE VIEW ApplicantSummary AS
SELECT 
    ap.applicant_id,
    CONCAT(COALESCE(ap.first_name, ''), ' ', COALESCE(ap.last_name, '')) as full_name,
    ap.phone_number,
    ap.address,
    ap.date_of_birth,
    COUNT(ad.detail_id) as total_applications
FROM ApplicantProfile ap
LEFT JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
GROUP BY ap.applicant_id;

-- View for complete applicant data with CV paths
CREATE VIEW CompleteApplicantData AS
SELECT 
    ap.applicant_id,
    ap.first_name,
    ap.last_name,
    CONCAT(COALESCE(ap.first_name, ''), ' ', COALESCE(ap.last_name, '')) as name,
    ap.phone_number,
    ap.address,
    ap.date_of_birth,
    ad.detail_id,
    ad.application_role as position,
    ad.cv_path
FROM ApplicantProfile ap
LEFT JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
WHERE ad.cv_path IS NOT NULL;
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
