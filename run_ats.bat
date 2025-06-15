@echo off
title ATS - Applicant Tracking System

echo ====================================
echo    ATS - Applicant Tracking System
echo ====================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Checking MySQL connection...
python -c "import mysql.connector; mysql.connector.connect(host='localhost', user='root', password='', database='ats_db').close(); print('Database connection OK')" 2>nul
if errorlevel 1 (
    echo Warning: Cannot connect to MySQL database
    echo Please ensure MySQL is running and ats_db database exists
    echo You can run setup.py to initialize the database
    echo.
)

echo Starting ATS application...
echo.
python main_gui.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start the application
    echo Please check the error messages above
    pause
)
