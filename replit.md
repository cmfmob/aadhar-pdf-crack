# Overview

This is a PDF Password Cracker web application built with Flask that attempts to unlock password-protected PDF files using name-based password patterns. The application generates passwords by combining a user's first name with years ranging from 1900 to 2025, then systematically tests each combination against the uploaded PDF file. It features a web interface for file uploads, real-time progress tracking, and asynchronous password cracking using threading.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Technology**: HTML5 with Bootstrap 5 for responsive UI and Font Awesome for icons
- **Structure**: Template-based rendering using Flask's Jinja2 templating engine
- **Components**: 
  - Main upload form (`index.html`) for file selection and name input
  - Progress tracking page (`progress.html`) with real-time updates
  - Client-side validation and form handling via vanilla JavaScript
- **Styling**: Custom CSS with gradient backgrounds, card-based layouts, and animated progress indicators

## Backend Architecture
- **Framework**: Flask web framework with Python
- **Design Pattern**: MVC pattern with separation of concerns
- **Core Components**:
  - `app.py`: Main Flask application with route handlers
  - `pdf_cracker.py`: PDF processing and password testing logic
  - `main.py`: Application entry point
- **Session Management**: In-memory session storage using Python dictionaries
- **File Handling**: Secure file uploads with validation and temporary storage

## Password Cracking Strategy
- **Algorithm**: Brute force approach using name-based patterns
- **Pattern Generation**: Combines first 4 characters of name (padded with 'X') with years 1900-2025
- **PDF Processing**: Uses PyPDF2 library for PDF encryption testing and decryption
- **Concurrency**: Threading implementation for non-blocking password testing

## Data Storage
- **File Storage**: Local filesystem storage in `uploads/` directory
- **Session Data**: In-memory storage for tracking cracking progress and results
- **Temporary Files**: Automatic cleanup of uploaded files after processing

## Security Considerations
- **File Validation**: Restricts uploads to PDF files only with size limits (16MB)
- **Filename Security**: Uses Werkzeug's secure_filename for safe file handling
- **Session Security**: Configurable secret key for session management
- **Input Sanitization**: Client and server-side validation for user inputs

# External Dependencies

## Python Libraries
- **Flask**: Web framework for HTTP handling and templating
- **PyPDF2**: PDF manipulation and encryption testing
- **Werkzeug**: WSGI utilities for secure file handling
- **uuid**: Unique session identifier generation
- **threading**: Asynchronous password cracking operations

## Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Font Awesome 6**: Icon library for visual elements
- **Vanilla JavaScript**: Client-side form validation and user interaction

## System Dependencies
- **Python 3.x**: Runtime environment
- **File System**: Local storage for temporary file uploads
- **HTTP Server**: Flask development server (production deployment would require WSGI server)

## Configuration
- **Environment Variables**: `SESSION_SECRET` for production security
- **File System**: Requires read/write permissions for uploads directory
- **Memory**: In-memory session storage (not persistent across restarts)