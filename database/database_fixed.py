import mysql.connector
from mysql.connector import Error
import logging

class DatabaseConnection:
    def __init__(self, host='localhost', port=3306, user='root', password='', database='ats_db'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                auth_plugin='mysql_native_password'
            )
            if self.connection.is_connected():
                logging.info("Database connection established successfully")
                return True
        except Error as e:
            logging.error(f"Error connecting to database: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("Database connection closed")

    def execute_query(self, query, params=None):
        """Execute SELECT query and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            logging.error(f"Error executing query: {e}")
            return []

    def execute_insert(self, query, params=None):
        """Execute INSERT query and return last inserted ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except Error as e:
            logging.error(f"Error executing insert: {e}")
            self.connection.rollback()
            return None

    def get_all_cv_data(self):
        """Get all CV data from database"""
        query = """
        SELECT 
            ap.applicant_id,
            ap.first_name,
            ap.last_name,
            ap.phone_number,
            ap.email,
            ap.address,
            ap.date_of_birth,
            ad.application_id,
            ad.application_role,
            ad.cv_path
        FROM ApplicantProfile ap
        JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
        ORDER BY ap.first_name, ap.last_name
        """
        return self.execute_query(query)

    def get_applicant_by_id(self, applicant_id):
        """Get specific applicant data by ID"""
        query = """
        SELECT 
            ap.applicant_id,
            ap.first_name,
            ap.last_name,
            ap.phone_number,
            ap.email,
            ap.address,
            ap.date_of_birth,
            ad.application_id,
            ad.application_role,
            ad.cv_path
        FROM ApplicantProfile ap
        JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
        WHERE ap.applicant_id = %s
        """
        results = self.execute_query(query, (applicant_id,))
        return results[0] if results else None
