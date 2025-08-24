// Main JavaScript file for PDF Password Cracker

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    const firstNameInput = document.getElementById('first_name');
    const pdfFileInput = document.getElementById('pdf_file');

    // Form validation and submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
                return false;
            }

            // Show loading state
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            submitBtn.disabled = true;
        });
    }

    // Real-time form validation
    if (firstNameInput) {
        firstNameInput.addEventListener('input', function() {
            const value = this.value.trim();
            const isValid = /^[A-Za-z]+$/.test(value) && value.length > 0;
            
            if (isValid) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
                updatePasswordPreview(value);
            } else {
                this.classList.remove('is-valid');
                if (value.length > 0) {
                    this.classList.add('is-invalid');
                }
                updatePasswordPreview('');
            }
        });
    }

    // File input validation
    if (pdfFileInput) {
        pdfFileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                if (file.type !== 'application/pdf') {
                    showFileError('Please select a PDF file');
                    this.value = '';
                    return;
                }
                
                if (file.size > 16 * 1024 * 1024) { // 16MB limit
                    showFileError('File size must be less than 16MB');
                    this.value = '';
                    return;
                }
                
                clearFileError();
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    }

    // Initialize tooltips
    initializeTooltips();
});

// Form validation function
function validateForm() {
    const firstName = document.getElementById('first_name').value.trim();
    const pdfFile = document.getElementById('pdf_file').files[0];
    
    let isValid = true;
    
    // Validate first name
    if (!firstName || !/^[A-Za-z]+$/.test(firstName)) {
        showFieldError('first_name', 'Please enter a valid first name (letters only)');
        isValid = false;
    }
    
    // Validate PDF file
    if (!pdfFile) {
        showFieldError('pdf_file', 'Please select a PDF file');
        isValid = false;
    } else if (pdfFile.type !== 'application/pdf') {
        showFieldError('pdf_file', 'Please select a valid PDF file');
        isValid = false;
    }
    
    return isValid;
}

// Show field error
function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    field.classList.add('is-invalid');
    
    // Remove existing error message
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
    
    // Add new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

// Show file error
function showFileError(message) {
    const fileInput = document.getElementById('pdf_file');
    fileInput.classList.add('is-invalid');
    
    // Remove existing error
    clearFileError();
    
    // Add error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback file-error';
    errorDiv.textContent = message;
    fileInput.parentNode.appendChild(errorDiv);
}

// Clear file error
function clearFileError() {
    const existingError = document.querySelector('.file-error');
    if (existingError) {
        existingError.remove();
    }
}

// Update password preview based on name input
function updatePasswordPreview(name) {
    const previewElement = document.querySelector('.password-preview');
    if (previewElement) {
        if (name) {
            const namePattern = name.toUpperCase().substr(0, 4).padEnd(4, 'X');
            previewElement.textContent = `Example: ${namePattern}1990, ${namePattern}1991, etc.`;
        } else {
            previewElement.textContent = 'Example: NAME1990, NAME1991, etc.';
        }
    }
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Utility function to format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Utility function to validate email format
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Auto-dismiss alerts after 5 seconds
setTimeout(function() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        const bsAlert = new bootstrap.Alert(alert);
        setTimeout(() => bsAlert.close(), 5000);
    });
}, 1000);

// Animate stats numbers
function animateStats() {
    const totalCracks = document.getElementById('totalCracks');
    const successRate = document.getElementById('successRate');
    
    if (totalCracks) {
        let start = 0;
        const end = 1247;
        const duration = 2000;
        const increment = end / (duration / 16);
        
        const timer = setInterval(() => {
            start += increment;
            if (start >= end) {
                totalCracks.textContent = end.toLocaleString();
                clearInterval(timer);
            } else {
                totalCracks.textContent = Math.floor(start).toLocaleString();
            }
        }, 16);
    }
    
    if (successRate) {
        let start = 0;
        const end = 78;
        const duration = 2000;
        const increment = end / (duration / 16);
        
        const timer = setInterval(() => {
            start += increment;
            if (start >= end) {
                successRate.textContent = end + '%';
                clearInterval(timer);
            } else {
                successRate.textContent = Math.floor(start) + '%';
            }
        }, 16);
    }
}

// Enhanced form interactions
function addFormEnhancements() {
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
}

// Initialize enhanced features
document.addEventListener('DOMContentLoaded', function() {
    // Delay stats animation for better UX
    setTimeout(animateStats, 500);
    addFormEnhancements();
    
    // Add loading state to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.type === 'submit') {
                setTimeout(() => {
                    this.classList.add('loading');
                }, 100);
            }
        });
    });
});

// Prevent multiple form submissions
let formSubmitted = false;
document.addEventListener('submit', function(e) {
    if (formSubmitted) {
        e.preventDefault();
        return false;
    }
    formSubmitted = true;
});

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
