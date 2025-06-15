"""
Configuration file for ATS application
"""

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',  # Updated password
    'database': 'ats_db',
    'auth_plugin': 'mysql_native_password',  # Use native password auth
    'autocommit': True,
    'use_unicode': True,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'sql_mode': 'TRADITIONAL',
    'raise_on_warnings': True,
    'allow_local_infile': False
}

# Application settings
APP_CONFIG = {
    'similarity_threshold': 0.7,  # Minimum similarity for fuzzy matching
    'max_results': 50,  # Maximum number of results to return
    'supported_formats': ['.pdf'],  # Supported CV file formats
}

# File paths
PATHS = {
    'data_dir': 'data',
    'logs_dir': 'logs',
    'temp_dir': 'temp'
}

# UI settings
UI_CONFIG = {
    'window_size': '1200x800',
    'font_family': 'Arial',
    'font_size': 11,
    'theme': 'default'
}
