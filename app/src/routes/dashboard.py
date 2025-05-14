from flask import Blueprint, render_template, request, redirect, url_for, session
from src.models.user import User

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.get_user_by_id(session['user_id'])
    return render_template('dashboard.html', user=user)