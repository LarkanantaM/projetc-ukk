from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.main import bp
from app.models import Registration, Payment

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get user's registration and payment info
    registration = Registration.query.filter_by(user_id=current_user.id).first()
    payments = Payment.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard/user_dashboard.html',
                         user=current_user,
                         registration=registration,
                         payments=payments)