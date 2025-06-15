
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional, Tuple
import json
import os
from datetime import datetime
from config import DB_CONFIG as DATABASE_CONFIG

class DatabaseConnection:
    """Database connection and operations for ATS system"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connected = False
        self.mock_mode = False
        self._initialize_connection()
        
    def _initialize_connection(self):
        """Initialize database connection with fallback to mock mode"""
        try:
            self.connection = mysql.connector.connect(**DATABASE_CONFIG)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                self.connected = True
                print("✅ Database connected successfully")
                self._create_tables_if_not_exist()
        except Error as e:
            print(f"⚠️  Database connection failed: {e}")
            print("🔄 Switching to mock mode for demonstration")
            self.mock_mode = True
            self._initialize_mock_data()
    
    def _create_tables_if_not_exist(self):
        """Create tables if they don't exist"""
        try:
            # Read and execute schema
            schema_file = "database_schema.sql"
            if os.path.exists(schema_file):
                with open(schema_file, 'r') as file:
                    schema = file.read()
                    # Execute each statement separately
                    for statement in schema.split(';'):
                        if statement.strip():
                            self.cursor.execute(statement)
                    self.connection.commit()
                    print("✅ Database tables created/verified")
        except Error as e:
            print(f"❌ Error creating tables: {e}")
    
    def _initialize_mock_data(self):
        """Initialize mock data for demonstration"""
        self.mock_applicants = [
            {
                'id': 1,
                'name': 'John Smith',
                'email': 'john.smith@email.com',
                'phone': '+1-555-0123',
                'position': 'Software Engineer',
                'summary': 'Experienced software engineer with 5+ years in full-stack development. Proficient in Python, JavaScript, React, and SQL.',
                'skills': 'Python, JavaScript, React, Node.js, SQL, Git, Docker',
                'experience': '5 years at TechCorp as Senior Developer, 2 years at StartupXYZ as Full Stack Engineer',
                'education': 'Bachelor of Computer Science - MIT (2015)',
                'cv_path': 'data/engineer/cv_001.pdf',
                'created_at': '2024-01-15 10:30:00'
            },
            {
                'id': 2,
                'name': 'Sarah Johnson',
                'email': 'sarah.johnson@email.com',
                'phone': '+1-555-0456',
                'position': 'UI/UX Designer',
                'summary': 'Creative UI/UX designer with strong background in user-centered design and prototyping.',
                'skills': 'Figma, Adobe XD, Sketch, Photoshop, Illustrator, Prototyping, User Research',
                'experience': '3 years at DesignStudio as UI Designer, 2 years at Creative Agency as Junior Designer',
                'education': 'Bachelor of Fine Arts - Design Institute (2018)',
                'cv_path': 'data/designer/cv_001.pdf',
                'created_at': '2024-01-14 14:20:00'
            },
            {
                'id': 3,
                'name': 'Michael Brown',
                'email': 'michael.brown@email.com',
                'phone': '+1-555-0789',
                'position': 'HR Manager',
                'summary': 'Experienced HR professional with expertise in talent acquisition and employee relations.',
                'skills': 'Recruitment, Talent Acquisition, Employee Relations, Performance Management, HRIS',
                'experience': '4 years at CorporateHR as HR Specialist, 3 years at BusinessCorp as Recruiter',
                'education': 'Master of Human Resources - Business University (2016)',
                'cv_path': 'data/hr/cv_001.pdf',
                'created_at': '2024-01-13 09:15:00'
            },
            {
                'id': 4,
                'name': 'Emily Davis',
                'email': 'emily.davis@email.com',
                'phone': '+1-555-0321',
                'position': 'Marketing Specialist',
                'summary': 'Digital marketing expert with focus on SEO, content marketing, and social media strategies.',
                'skills': 'Digital Marketing, SEO, Content Marketing, Social Media, Google Analytics, PPC',
                'experience': '3 years at MarketingPro as Digital Marketer, 2 years at AdAgency as Marketing Assistant',
                'education': 'Bachelor of Marketing - Commerce College (2019)',
                'cv_path': 'data/marketing/cv_001.pdf',
                'created_at': '2024-01-12 16:45:00'
            },
            {
                'id': 5,
                'name': 'David Wilson',
                'email': 'david.wilson@email.com',
                'phone': '+1-555-0654',
                'position': 'Sales Manager',
                'summary': 'Results-driven sales professional with proven track record in B2B sales and client relationship management.',
                'skills': 'B2B Sales, CRM, Lead Generation, Negotiation, Account Management, Salesforce',
                'experience': '5 years at SalesCorp as Senior Sales Rep, 3 years at BusinessSolutions as Sales Associate',
                'education': 'Bachelor of Business Administration - Sales University (2014)',
                'cv_path': 'data/sales/cv_001.pdf',
                'created_at': '2024-01-11 11:30:00'
            }
        ]
    
    def search_applicants(self, query: str, algorithm: str = 'kmp') -> List[Dict]:
        """Search applicants based on keywords"""
        if self.mock_mode:
            return self._mock_search(query)
        
        try:
            sql = """
            SELECT * FROM applicants 
            WHERE name LIKE %s OR email LIKE %s OR position LIKE %s 
            OR skills LIKE %s OR summary LIKE %s OR experience LIKE %s
            ORDER BY created_at DESC
            """
            search_term = f"%{query}%"
            params = (search_term, search_term, search_term, search_term, search_term, search_term)
            
            self.cursor.execute(sql, params)
            results = self.cursor.fetchall()
            return results
        except Error as e:
            print(f"❌ Search error: {e}")
            return []
    
    def _mock_search(self, query: str) -> List[Dict]:
        """Mock search for demonstration"""
        query_lower = query.lower()
        results = []
        
        for applicant in self.mock_applicants:
            # Search in all text fields
            searchable_text = (
                f"{applicant['name']} {applicant['position']} {applicant['skills']} "
                f"{applicant['summary']} {applicant['experience']} {applicant['education']}"
            ).lower()
            
            if query_lower in searchable_text:
                results.append(applicant.copy())
        
        return results
    
    def get_all_applicants(self) -> List[Dict]:
        """Get all applicants"""
        if self.mock_mode:
            return self.mock_applicants.copy()
        
        try:
            self.cursor.execute("SELECT * FROM applicants ORDER BY created_at DESC")
            return self.cursor.fetchall()
        except Error as e:
            print(f"❌ Error fetching applicants: {e}")
            return []
    
    def get_applicant_by_id(self, applicant_id: int) -> Optional[Dict]:
        """Get specific applicant by ID"""
        if self.mock_mode:
            for applicant in self.mock_applicants:
                if applicant['id'] == applicant_id:
                    return applicant.copy()
            return None
        
        try:
            self.cursor.execute("SELECT * FROM applicants WHERE id = %s", (applicant_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"❌ Error fetching applicant: {e}")
            return None
    
    def add_applicant(self, applicant_data: Dict) -> bool:
        """Add new applicant to database"""
        if self.mock_mode:
            new_id = max([a['id'] for a in self.mock_applicants]) + 1
            applicant_data['id'] = new_id
            applicant_data['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.mock_applicants.append(applicant_data)
            return True
        
        try:
            sql = """
            INSERT INTO applicants (name, email, phone, position, summary, skills, experience, education, cv_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                applicant_data['name'],
                applicant_data['email'],
                applicant_data['phone'],
                applicant_data['position'],
                applicant_data['summary'],
                applicant_data['skills'],
                applicant_data['experience'],
                applicant_data['education'],
                applicant_data['cv_path']
            )
            
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True
        except Error as e:
            print(f"❌ Error adding applicant: {e}")
            return False
    
    def update_applicant(self, applicant_id: int, applicant_data: Dict) -> bool:
        """Update existing applicant"""
        if self.mock_mode:
            for i, applicant in enumerate(self.mock_applicants):
                if applicant['id'] == applicant_id:
                    self.mock_applicants[i].update(applicant_data)
                    return True
            return False
        
        try:
            sql = """
            UPDATE applicants 
            SET name=%s, email=%s, phone=%s, position=%s, summary=%s, skills=%s, experience=%s, education=%s
            WHERE id=%s
            """
            values = (
                applicant_data['name'],
                applicant_data['email'],
                applicant_data['phone'],
                applicant_data['position'],
                applicant_data['summary'],
                applicant_data['skills'],
                applicant_data['experience'],
                applicant_data['education'],
                applicant_id
            )
            
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True
        except Error as e:
            print(f"❌ Error updating applicant: {e}")
            return False
    
    def delete_applicant(self, applicant_id: int) -> bool:
        """Delete applicant from database"""
        if self.mock_mode:
            self.mock_applicants = [a for a in self.mock_applicants if a['id'] != applicant_id]
            return True
        
        try:
            self.cursor.execute("DELETE FROM applicants WHERE id = %s", (applicant_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"❌ Error deleting applicant: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        if self.mock_mode:
            return {
                'total_applicants': len(self.mock_applicants),
                'positions': len(set(a['position'] for a in self.mock_applicants)),
                'recent_applications': len([a for a in self.mock_applicants 
                                          if '2024-01' in a['created_at']])
            }
        
        try:
            stats = {}
            
            # Total applicants
            self.cursor.execute("SELECT COUNT(*) as count FROM applicants")
            result = self.cursor.fetchone()
            stats['total_applicants'] = result['count'] if result else 0
            
            # Distinct positions
            self.cursor.execute("SELECT COUNT(DISTINCT position) as count FROM applicants")
            result = self.cursor.fetchone()
            stats['positions'] = result['count'] if result else 0
            
            # Recent applications (last 30 days)
            self.cursor.execute("""
                SELECT COUNT(*) as count FROM applicants 
                WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            """)
            result = self.cursor.fetchone()
            stats['recent_applications'] = result['count'] if result else 0
            
            return stats
        except Error as e:
            print(f"❌ Error getting statistics: {e}")
            return {'total_applicants': 0, 'positions': 0, 'recent_applications': 0}
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self.connected or self.mock_mode
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            self.connected = False
            print("✅ Database connection closed")