from flask import Flask, render_template, session, redirect, url_for, abort
from functools import wraps
from models import db
from models.user import User, UserRole
from config import Config

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin():
            abort(403)  # Forbidden access
            
        return f(*args, **kwargs)
    return decorated_function

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        admin = User.query.filter_by(role=UserRole.ADMIN.value).first()
        if not admin:
            admin = User(
                username='admin',
                fullname='Administrator',
                email='admin@ppdb.com',
                role=UserRole.ADMIN.value
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully")
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        registration_progress = 1
        
        return render_template('dashboard.html', 
                             username=user.username, 
                             email=user.email,
                             progress=registration_progress)

    @app.route('/admin/dashboard')
    @admin_required
    def admin_dashboard():
        total_pendaftar = User.query.filter_by(is_admin=False).count()
        pending_verifikasi = User.query.filter_by(status='pending').count()
        terverifikasi = User.query.filter_by(status='approved').count()
        ditolak = User.query.filter_by(status='rejected').count()
        
        pendaftar_list = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).limit(10).all()
        
        return render_template('admin_dashboard.html',
                             total_pendaftar=total_pendaftar,
                             pending_verifikasi=pending_verifikasi,
                             terverifikasi=terverifikasi,
                             ditolak=ditolak,
                             pendaftar_list=pendaftar_list)

    @app.errorhandler(404)
    def not_found_error(error):
        return 'Page not found', 404

    return app

# Create the Flask application instance
application = create_app()
app = application  # For Flask CLI compatibility

# Only for development
if __name__ == '__main__':
    application.run(debug=True)