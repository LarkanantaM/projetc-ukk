from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models import db, User, Formulir, Payment
from functools import wraps
import os
from datetime import datetime
from app.utils import get_jurusan_name

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get basic statistics
    all_forms = Formulir.query.all()
    pending_forms = Formulir.query.join(User).filter(User.is_accepted.is_(None)).all()
    accepted_forms = Formulir.query.join(User).filter(User.is_accepted.is_(True)).all()
    rejected_forms = Formulir.query.join(User).filter(User.is_accepted.is_(False)).all()
    
    return render_template('auth/admin_dashboard.html',
                         all_forms=all_forms,
                         pending_forms=pending_forms,
                         accepted_forms=accepted_forms,
                         rejected_forms=rejected_forms,
                         get_jurusan_name=get_jurusan_name)

@admin.route('/dashboard-data')
@login_required
@admin_required
def dashboard_data():
    # Get basic statistics
    all_forms = Formulir.query.all()
    pending_forms = Formulir.query.join(User).filter(User.is_accepted.is_(None)).all()
    accepted_forms = Formulir.query.join(User).filter(User.is_accepted.is_(True)).all()
    rejected_forms = Formulir.query.join(User).filter(User.is_accepted.is_(False)).all()
    
    # Calculate jurusan statistics
    jurusan_stats = {
        'RPL': Formulir.query.filter_by(jurusan='RPL').count(),
        'TSM': Formulir.query.filter_by(jurusan='TSM').count(),
        'HOTEL': Formulir.query.filter_by(jurusan='HOTEL').count()
    }
    
    # Calculate daily statistics for the past week
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    daily_stats = db.session.query(
        func.date(Formulir.created_at).label('date'),
        func.count(Formulir.id).label('count')
    ).filter(Formulir.created_at >= week_ago)\
     .group_by(func.date(Formulir.created_at))\
     .all()
    
    return jsonify({
        'total': len(all_forms),
        'pending': len(pending_forms),
        'accepted': len(accepted_forms),
        'rejected': len(rejected_forms),
        'jurusan_stats': jurusan_stats,
        'daily_stats': [{'date': str(d.date), 'count': d.count} for d in daily_stats]
    })

@admin.route('/get-form-details/<int:form_id>')
@login_required
@admin_required
def get_form_details(form_id):
    form = Formulir.query.get_or_404(form_id)
    return jsonify({
        'id': form.id,
        'nama': form.nama,
        'tempat_lahir': form.tempat_lahir,
        'tanggal_lahir': str(form.tanggal_lahir),
        'alamat': form.alamat,
        'jurusan': form.jurusan,
        'asal_sekolah': form.asal_sekolah,
        'nilai_rata': form.nilai_rata
    })

@admin.route('/review/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def review_application(user_id):
    try:
        user = User.query.get_or_404(user_id)
        action = request.form.get('action')
        
        if action == 'accept':
            user.is_accepted = True
            flash(f'Application for {user.username} has been accepted', 'success')
        elif action == 'reject':
            user.is_accepted = False
            flash(f'Application for {user.username} has been rejected', 'warning')
        else:
            flash('Invalid action', 'error')
            return redirect(url_for('admin.dashboard'))
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Error processing application: {str(e)}', 'error')
    
    return redirect(url_for('admin.dashboard'))

@admin.route('/verify-payment/<int:payment_id>', methods=['POST'])
@login_required
@admin_required
def verify_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    action = request.form.get('action')
    
    try:
        if action == 'verify':
            payment.status = 'verified'
            message = 'Pembayaran berhasil diverifikasi'
        elif action == 'reject':
            payment.status = 'rejected'
            message = 'Pembayaran ditolak'
        else:
            return jsonify({'success': False, 'message': 'Invalid action'})
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': message,
            'status': payment.status
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error memproses pembayaran: {str(e)}'
        })

@admin.route('/payment-details/<int:payment_id>')
@login_required
@admin_required
def payment_details(payment_id):
    try:
        payment = Payment.query.get_or_404(payment_id)
        user = User.query.get(payment.user_id)
        formulir = Formulir.query.filter_by(user_id=payment.user_id).first()
        
        # Get the correct path for the payment proof
        image_url = url_for('static', filename=f'uploads/{payment.payment_proof}')
        
        return jsonify({
            'success': True,
            'image_url': image_url,
            'user_name': formulir.nama if formulir else user.username,
            'amount': payment.amount,
            'created_at': payment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'status': payment.status
        })
    except Exception as e:
        print(f"Error in payment_details: {str(e)}")  # Debug print
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500