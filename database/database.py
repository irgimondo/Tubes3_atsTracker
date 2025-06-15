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

    def is_connected(self):
        """Check if database is connected"""
        return self.connection and self.connection.is_connected()

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
        # If database connection is available, use real data
        if self.connection and self.connection.is_connected():
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
        else:
            # Return same mock data as get_all_applicants when database not available
            return self.get_all_applicants()

    def get_applicant_by_id(self, applicant_id):
        """Get specific applicant data by ID"""
        # If database connection is available, use real data
        if self.connection and self.connection.is_connected():
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
        else:
            # Search in mock data
            mock_data = self.get_all_applicants()
            for applicant in mock_data:
                if applicant['applicant_id'] == applicant_id:
                    return applicant
            return None

    def get_all_applicants(self):
        """Get all applicants with their CV data - uses mock data when database is not available"""
        # If database connection is available, use real data
        if self.connection and self.connection.is_connected():
            return self.get_all_cv_data()
        
        # Mock data for testing when database is not available
        mock_data = [
            {
                'applicant_id': 1,
                'first_name': 'John',
                'last_name': 'Doe',
                'phone_number': '+6281234567890',
                'email': 'john.doe@email.com',
                'address': 'Jakarta, Indonesia',
                'date_of_birth': '1995-01-15',
                'application_id': 1,
                'application_role': 'Designer',
                'cv_path': 'data/Designer/designer_01.pdf'
            },
            {
                'applicant_id': 2,
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone_number': '+6281234567891',
                'email': 'jane.smith@email.com',
                'address': 'Bandung, Indonesia',
                'date_of_birth': '1993-03-22',
                'application_id': 2,
                'application_role': 'Engineer',
                'cv_path': 'data/Engineer/engineer_01.pdf'
            },
            {
                'applicant_id': 3,
                'first_name': 'Bob',
                'last_name': 'Johnson',
                'phone_number': '+6281234567892',
                'email': 'bob.johnson@email.com',
                'address': 'Surabaya, Indonesia',
                'date_of_birth': '1990-07-10',
                'application_id': 3,
                'application_role': 'Marketing',
                'cv_path': 'data/Marketing/marketing_01.pdf'
            },
            {
                'applicant_id': 4,
                'first_name': 'Alice',
                'last_name': 'Brown',
                'phone_number': '+6281234567893',
                'email': 'alice.brown@email.com',
                'address': 'Medan, Indonesia',
                'date_of_birth': '1992-12-05',
                'application_id': 4,
                'application_role': 'HR',
                'cv_path': 'data/HR/hr_01.pdf'
            },
            {
                'applicant_id': 5,
                'first_name': 'Charlie',
                'last_name': 'Wilson',
                'phone_number': '+6281234567894',
                'email': 'charlie.wilson@email.com',
                'address': 'Yogyakarta, Indonesia',
                'date_of_birth': '1994-09-18',
                'application_id': 5,
                'application_role': 'Sales',
                'cv_path': 'data/Sales/sales_01.pdf'
            }
        ]
        
        return mock_data
