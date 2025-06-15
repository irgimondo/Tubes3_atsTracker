#!/usr/bin/env python3
"""
ATS - Applicant Tracking System
Main Application Entry Point

This is the main entry point for the ATS application.
It provides a clean interface to launch the GUI application.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    """Main application entry point"""
    try:
        print("🚀 Starting ATS - Applicant Tracking System...")        # Import and run the GUI application
        from gui.main_gui import main as gui_main
        gui_main()
        
    except ImportError as e:
        print(f" Import Error: {e}")
        print("Please ensure all dependencies are installed.")
        print("Run: python scripts/setup.py")
        sys.exit(1)
    except Exception as e:
        print(f" Application Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
