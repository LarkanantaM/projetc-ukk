from flask import Flask
from flask_login import LoginManager
from app.models import db, User, Payment  # Add Payment to imports
from .utils import get_jurusan_name
import os

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def check_upload_directory(directory):
    """Check if upload directory exists and has correct permissions"""
    if not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False
    
    try:
        # Test file creation
        test_file = os.path.join(directory, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print(f"Directory {directory} is writable")
        return True
    except Exception as e:
        print(f"Directory {directory} is not writable: {e}")
        return False

def init_app(app):
    # Create uploads directory if it doesn't exist
    uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Set proper permissions
    try:
        os.chmod(uploads_dir, 0o755)
    except Exception as e:
        print(f"Warning: Could not set permissions on uploads directory: {e}")

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Ensure upload directory exists with correct permissions
    uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
    if not check_upload_directory(uploads_dir):
        print("WARNING: Upload directory is not properly configured!")
    print(f"Upload directory created at: {uploads_dir}")  # Debug print
    
    # List files in uploads directory for debugging
    print(f"Files in uploads directory: {os.listdir(uploads_dir)}")
    
    # Set upload configurations with absolute path
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
    app.config['UPLOAD_FOLDER'] = uploads_dir
    app.config['UPLOAD_PATH'] = 'uploads'  # Relative path for URL generation

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from .routes.auth import auth
    from .routes.user import user
    from .routes.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(admin)

    # Register template global functions
    @app.context_processor
    def utility_processor():
        return {
            'get_jurusan_name': get_jurusan_name,
            'get_latest_payment': lambda user_id: Payment.query.filter_by(user_id=user_id)
                                                             .order_by(Payment.created_at.desc())
                                                             .first()
        }

    # Create database tables
    with app.app_context():
        db.create_all()

    return app