import pymysql
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
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            logging.info("Database connection established successfully")
            return True
        except Exception as e:
            logging.error(f"Error connecting to database: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed")

    def is_connected(self):
        """Check if database is connected"""
        return self.connection and self.connection.open

    def execute_query(self, query, params=None):
        """Execute SELECT query and return results"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return None

    def execute_update(self, query, params=None):
        """Execute INSERT, UPDATE, DELETE query"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        except Exception as e:
            logging.error(f"Error executing update: {e}")
            return 0

    def get_applicant_profiles(self):
        """Get all applicant profiles"""
        query = "SELECT * FROM ApplicantProfile ORDER BY created_at DESC"
        return self.execute_query(query)

    def get_application_details(self):
        """Get all application details"""
        query = "SELECT * FROM ApplicationDetail ORDER BY applied_date DESC"
        return self.execute_query(query)

    def search_applicants_by_name(self, name):
        """Search applicants by name"""
        query = """
        SELECT * FROM ApplicantProfile 
        WHERE first_name LIKE %s OR last_name LIKE %s
        ORDER BY first_name, last_name
        """
        search_term = f"%{name}%"
        return self.execute_query(query, (search_term, search_term))

    def search_applicants_by_skill(self, skill):
        """Search applicants by skill"""
        query = """
        SELECT * FROM ApplicantProfile 
        WHERE skills LIKE %s
        ORDER BY first_name, last_name
        """
        search_term = f"%{skill}%"
        return self.execute_query(query, (search_term,))

    def add_applicant(self, first_name, last_name, phone_number, email, address, 
                     date_of_birth, summary, skills, experience, education):
        """Add new applicant"""
        query = """
        INSERT INTO ApplicantProfile 
        (first_name, last_name, phone_number, email, address, date_of_birth, 
         summary, skills, experience, education)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (first_name, last_name, phone_number, email, address, 
                 date_of_birth, summary, skills, experience, education)
        return self.execute_update(query, params)

    def add_application(self, applicant_id, application_role, cv_path, 
                       application_status='pending', notes=None):
        """Add new application"""
        query = """
        INSERT INTO ApplicationDetail 
        (applicant_id, application_role, cv_path, application_status, notes)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (applicant_id, application_role, cv_path, application_status, notes)
        return self.execute_update(query, params)

    def update_application_status(self, application_id, status, notes=None):
        """Update application status"""
        if notes:
            query = """
            UPDATE ApplicationDetail 
            SET application_status = %s, notes = %s 
            WHERE application_id = %s
            """
            params = (status, notes, application_id)
        else:
            query = """
            UPDATE ApplicationDetail 
            SET application_status = %s 
            WHERE application_id = %s
            """
            params = (status, application_id)
        return self.execute_update(query, params)

    def get_applicant_details_view(self):
        """Get data from ApplicantDetails view"""
        query = "SELECT * FROM ApplicantDetails ORDER BY first_name, last_name"
        return self.execute_query(query)

    def search_applications_by_role(self, role):
        """Search applications by role"""
        query = """
        SELECT * FROM ApplicationDetail 
        WHERE application_role LIKE %s
        ORDER BY applied_date DESC
        """
        search_term = f"%{role}%"
        return self.execute_query(query, (search_term,))

    def get_all_applicants(self):
        """Get all applicants with their application details"""
        query = """
        SELECT ap.*, ad.application_role, ad.cv_path, ad.application_status, ad.applied_date
        FROM ApplicantProfile ap
        LEFT JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
        ORDER BY ap.first_name, ap.last_name
        """
        return self.execute_query(query)

    def get_applicants_by_role(self, role):
        """Get applicants by role"""
        query = """
        SELECT ap.*, ad.application_role, ad.cv_path, ad.application_status, ad.applied_date
        FROM ApplicantProfile ap
        INNER JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
        WHERE ad.application_role LIKE %s
        ORDER BY ap.first_name, ap.last_name
        """
        search_term = f"%{role}%"
        return self.execute_query(query, (search_term,))

    def get_all_roles(self):
        """Get all unique roles"""
        query = "SELECT DISTINCT application_role FROM ApplicationDetail ORDER BY application_role"
        return self.execute_query(query)
