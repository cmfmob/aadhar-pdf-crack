import os
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
import uuid
import threading
from pdf_cracker import PDFCracker

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global dictionary to store cracking sessions
cracking_sessions = {}

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and start cracking process"""
    try:
        # Validate form data
        if 'pdf_file' not in request.files:
            return jsonify({'success': False, 'error': 'No file selected'})
        
        file = request.files['pdf_file']
        first_name = request.form.get('first_name', '').strip()
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if not first_name:
            return jsonify({'success': False, 'error': 'Please enter your first name'})
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Please upload a PDF file'})
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        
        # Save uploaded file
        filename = secure_filename(file.filename or 'uploaded_file.pdf')
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
        file.save(file_path)
        
        # Initialize cracking session
        cracking_sessions[session_id] = {
            'status': 'starting',
            'current_password': '',
            'progress': 0,
            'total_passwords': 126,  # (2025 - 1900 + 1)
            'found_password': None,
            'error': None,
            'completed': False
        }
        
        # Start cracking in background thread
        cracker = PDFCracker(file_path, first_name, session_id, cracking_sessions)
        thread = threading.Thread(target=cracker.start_cracking)
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'session_id': session_id})
        
    except Exception as e:
        app.logger.error(f"Upload error: {str(e)}")
        return jsonify({'success': False, 'error': 'An error occurred during file upload'})

@app.route('/progress')
def progress():
    """Progress tracking page"""
    session_id = session.get('session_id')
    if not session_id or session_id not in cracking_sessions:
        flash('No active session found', 'error')
        return redirect(url_for('index'))
    
    return render_template('progress.html', session_id=session_id)

@app.route('/api/progress')
def get_progress():
    """API endpoint to get current progress"""
    session_id = session.get('session_id')
    if not session_id or session_id not in cracking_sessions:
        return jsonify({'error': 'No active session'}), 404
    
    progress_data = cracking_sessions[session_id]
    return jsonify(progress_data)

@app.route('/api/progress/<session_id>')
def get_progress_by_id(session_id):
    """API endpoint to get progress by session ID"""
    if not session_id or session_id not in cracking_sessions:
        return jsonify({'error': 'No active session'}), 404
    
    progress_data = cracking_sessions[session_id]
    return jsonify(progress_data)

@app.route('/reset')
def reset():
    """Reset session and return to main page"""
    session_id = session.get('session_id')
    if session_id:
        # Clean up session data
        if session_id in cracking_sessions:
            del cracking_sessions[session_id]
        
        # Clean up uploaded file
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            if file.startswith(session_id):
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
                except:
                    pass
        
        session.pop('session_id', None)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
