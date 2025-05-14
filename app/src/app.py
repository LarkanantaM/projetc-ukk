from flask import Flask, render_template, session, redirect, url_for
from routes.auth import auth_bp
from models.user import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', 
                         username=user.username, 
                         email=user.email)

@app.errorhandler(404)
def not_found_error(error):
    return 'Page not found', 404

# Create database tables
def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)