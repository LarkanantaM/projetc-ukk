from flask import Blueprint, render_template, abort
from functools import wraps
from flask import session, redirect, url_for
from models.user import User

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    users = User.query.filter_by(role='user').all()
    return render_template('admin_dashboard.html', users=users)