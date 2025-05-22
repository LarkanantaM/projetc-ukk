📘 PPDB Online System - User Manual
📋 Table of Contents
Introduction
Getting Started
User Roles
System Requirements
Features Guide
Troubleshooting
🎯 Introduction
PPDB Online System is a web-based application for managing student registrations efficiently. This manual provides detailed instructions for both administrators and users.




🚀 Getting Started
Installation
# Clone repository
git clone [repository-url]

# Navigate to project directory
cd renew-ukk-Lingga/app/src

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt



Initial Setup
# Set environment variables
set FLASK_APP=app.py
set FLASK_ENV=development

# Run application
flask run

👥 User Roles
Administrator
Default credentials:
Username: admin
Password: admin123

Access: /admin/dashboard
Capabilities:
👀 View all applications
✅ Verify documents
📊 Monitor registration status
👥 Manage user accounts
Student/Applicant
Registration at: /register
Login at: /login
Features:
📝 Complete registration form
📤 Upload documents
📊 Track application status
💳 View registration card
💻 System Requirements
Windows OS
Python 3.8+
Modern web browser
Internet connection
Minimum 2GB RAM
Storage space for uploads
📱 Features Guide
Registration Process
Create new account at /register
Login with credentials
Fill personal information
Upload required documents:
📄 Birth certificate
🏫 School certificate
📸 Passport photo
📋 Family card
Submit application
Track status through dashboard
Document Upload Guidelines
Supported formats: JPG, PNG, PDF
Maximum file size: 2MB
Required resolution: minimum 300dpi
Clear and legible scans only
Status Tracking
Status indicators:

🕒 Pending: Application submitted
👀 Review: Under verification
✅ Approved: Application accepted
❌ Rejected: Application denied
❗ Troubleshooting
Common Issues
Login Failed

Verify username/password
Check CAPS LOCK
Clear browser cache
Upload Errors

Check file size
Verify file format
Ensure stable internet
Page Not Loading

Refresh browser
Clear cache
Check internet connection