import PyPDF2
import logging
import time
import os

class PDFCracker:
    def __init__(self, file_path, first_name, session_id, sessions_dict):
        self.file_path = file_path
        self.first_name = first_name.upper()[:4].ljust(4, 'X')  # Pad with X if name is too short
        self.session_id = session_id
        self.sessions = sessions_dict
        self.logger = logging.getLogger(__name__)
        
    def generate_passwords(self):
        """Generate all possible passwords based on name pattern"""
        passwords = []
        for year in range(1900, 2026):
            password = f"{self.first_name}{year}"
            passwords.append(password)
        return passwords
    
    def test_password(self, pdf_path, password):
        """Test if password can unlock the PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Check if PDF is encrypted
                if not pdf_reader.is_encrypted:
                    return False
                
                # Try to decrypt with password
                if pdf_reader.decrypt(password):
                    # Additional validation - try to access first page
                    if len(pdf_reader.pages) > 0:
                        try:
                            # Try to extract text from first page to confirm access
                            first_page = pdf_reader.pages[0]
                            first_page.extract_text()
                            return True
                        except:
                            return False
                    return True
                
                return False
                
        except Exception as e:
            self.logger.error(f"Error testing password {password}: {str(e)}")
            return False
    
    def start_cracking(self):
        """Main cracking process"""
        try:
            # Update status
            self.sessions[self.session_id]['status'] = 'running'
            
            # First check if file is actually a PDF and is encrypted
            try:
                with open(self.file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    if not pdf_reader.is_encrypted:
                        self.sessions[self.session_id]['error'] = 'PDF is not password protected'
                        self.sessions[self.session_id]['status'] = 'error'
                        self.sessions[self.session_id]['completed'] = True
                        return
            except Exception as e:
                self.sessions[self.session_id]['error'] = f'Invalid PDF file: {str(e)}'
                self.sessions[self.session_id]['status'] = 'error'
                self.sessions[self.session_id]['completed'] = True
                return
            
            # Generate all possible passwords
            passwords = self.generate_passwords()
            total_passwords = len(passwords)
            
            self.logger.info(f"Starting to crack PDF with {total_passwords} possible passwords")
            self.logger.info(f"Using name pattern: {self.first_name}")
            
            # Test each password
            for i, password in enumerate(passwords):
                # Update current password being tested
                self.sessions[self.session_id]['current_password'] = password
                self.sessions[self.session_id]['progress'] = i + 1
                
                self.logger.debug(f"Testing password: {password}")
                
                # Test the password
                if self.test_password(self.file_path, password):
                    # Password found! - ensure progress shows 100%
                    self.sessions[self.session_id]['progress'] = total_passwords
                    self.sessions[self.session_id]['found_password'] = password
                    self.sessions[self.session_id]['status'] = 'success'
                    # Small delay to ensure frontend gets the final progress update
                    time.sleep(0.1)
                    self.sessions[self.session_id]['completed'] = True
                    self.logger.info(f"Password found: {password}")
                    return
                
                # Small delay for faster cracking
                time.sleep(0.02)
            
            # No password found - ensure progress shows 100%
            self.sessions[self.session_id]['progress'] = total_passwords
            self.sessions[self.session_id]['status'] = 'failed'
            self.sessions[self.session_id]['error'] = 'Password not found, please try with another first name.'
            # Small delay to ensure frontend gets the final progress update
            time.sleep(0.1)
            self.sessions[self.session_id]['completed'] = True
            self.logger.info("Password cracking completed - no password found")
            
        except Exception as e:
            self.logger.error(f"Cracking error: {str(e)}")
            self.sessions[self.session_id]['error'] = f'An error occurred: {str(e)}'
            self.sessions[self.session_id]['status'] = 'error'
            self.sessions[self.session_id]['completed'] = True
        
        finally:
            # Clean up uploaded file
            try:
                if os.path.exists(self.file_path):
                    os.remove(self.file_path)
            except:
                pass
