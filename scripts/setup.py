"""
Setup script for ATS application
Installs dependencies, creates database, and sets up initial data
"""

import subprocess
import sys
import os
import mysql.connector
from mysql.connector import Error
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def install_dependencies():
    """Install required Python packages"""
    logger.info("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False

def create_database():
    """Create the ATS database and tables"""
    logger.info("Setting up database...")
    
    # Database configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Change if you have a password
        'port': 3306
    }
    
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Read and execute SQL schema
        with open('database_schema.sql', 'r') as file:
            sql_commands = file.read()
        
        # Split commands by semicolon and execute each
        commands = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]
        
        for command in commands:
            if command:
                cursor.execute(command)
        
        connection.commit()
        logger.info("Database created successfully!")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        logger.error(f"Database setup failed: {e}")
        return False

def generate_sample_data():
    """Generate sample CV data"""
    logger.info("Generating sample CV data...")
    
    try:
        # First install reportlab if not available
        try:
            import reportlab
        except ImportError:
            logger.info("Installing reportlab for PDF generation...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
        
        # Run the sample CV generator
        from generate_sample_cvs import generate_sample_cvs
        generate_sample_cvs(5)  # Generate 5 CVs per role
        logger.info("Sample CV data generated successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to generate sample data: {e}")
        return False

def seed_database():
    """Seed the database with sample applicant data"""
    logger.info("Seeding database with sample data...")
    
    try:
        from seeding_db import main as seed_main
        seed_main()
        logger.info("Database seeded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to seed database: {e}")
        return False

def main():
    """Main setup function"""
    logger.info("Starting ATS application setup...")
    
    steps = [
        ("Installing dependencies", install_dependencies),
        ("Creating database", create_database),
        ("Generating sample CVs", generate_sample_data),
        ("Seeding database", seed_database)
    ]
    
    for step_name, step_func in steps:
        logger.info(f"Step: {step_name}")
        if not step_func():
            logger.error(f"Setup failed at step: {step_name}")
            return False
        logger.info(f" {step_name} completed")
    
    logger.info("ATS application setup completed successfully!")
    logger.info("You can now run the application with: python main_gui.py")
    return True

if __name__ == "__main__":
    main()
