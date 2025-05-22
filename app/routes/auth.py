from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Formulir, db
from functools import wraps
from datetime import datetime
from werkzeug.utils import secure_filename
import os

auth = Blueprint('auth', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('user.dashboard'))
    
    # Get all forms with their associated users
    all_forms = Formulir.query.join(User).all()
    pending_forms = Formulir.query.join(User).filter(User.is_accepted.is_(None)).all()
    accepted_forms = Formulir.query.join(User).filter(User.is_accepted.is_(True)).all()
    rejected_forms = Formulir.query.join(User).filter(User.is_accepted.is_(False)).all()
    
    return render_template('auth/admin_dashboard.html',
                         pending_forms=pending_forms,
                         accepted_forms=accepted_forms,
                         rejected_forms=rejected_forms,
                         all_forms=all_forms,
                         accepted_count=len(accepted_forms),  # Add this line
                         rejected_count=len(rejected_forms),  # Add this line
                         pending_count=len(pending_forms))    # Add this line

@auth.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    return render_template('main.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login berhasil!', 'success')
            
            # Redirect admin to admin dashboard
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            # Redirect regular users to user dashboard    
            return redirect(url_for('user.dashboard'))
        
        flash('Username atau password salah', 'error')
    
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(username=username, role='user')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        # Admin view
        pending_forms = Formulir.query.join(User).filter(User.is_accepted.is_(None)).all()
        accepted_forms = Formulir.query.join(User).filter(User.is_accepted.is_(True)).all()
        rejected_forms = Formulir.query.join(User).filter(User.is_accepted.is_(False)).all()
        all_forms = Formulir.query.all()
        return render_template('auth/dashboard.html',
                            pending_forms=pending_forms,
                            accepted_forms=accepted_forms,
                            rejected_forms=rejected_forms,
                            all_forms=all_forms)
    else:
        # Regular user view
        return render_template('auth/dashboard.html', 
                            user_form=current_user.formulir)

@auth.route('/formulir', methods=['GET', 'POST'])
@login_required
def formulir():
    if current_user.role == 'admin':
        flash('Admins cannot submit forms', 'error')
        return redirect(url_for('auth.dashboard'))

    if current_user.formulir:
        flash('You have already submitted a form', 'warning')
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        try:
            # Konversi tanggal_lahir ke objek date
            tanggal_lahir_str = request.form['tanggal_lahir']
            tanggal_lahir = datetime.strptime(tanggal_lahir_str, '%Y-%m-%d').date()

            # Handle upload ijazah
            ijazah = request.files['ijazah']
            ijazah_filename = None
            if ijazah and ijazah.filename != '':
                filename = f"{current_user.username}_{ijazah.filename}"
                upload_folder = os.path.join(os.getcwd(),'app', 'static', 'uploads')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                ijazah.save(os.path.join(upload_folder, filename))
                ijazah_filename = filename

            formulir = Formulir(
                user_id=current_user.id,
                nama=request.form['nama'],
                tempat_lahir=request.form['tempat_lahir'],
                tanggal_lahir=tanggal_lahir,
                alamat=request.form['alamat'],
                asal_sekolah=request.form['asal_sekolah'],
                kelamin=request.form['kelamin'],
                agama=request.form['agama'],
                jurusan=request.form['jurusan'],
                nilai_rata=float(request.form['nilai_rata']),
                ijazah_filename=ijazah_filename
            )
            db.session.add(formulir)
            db.session.commit()
            flash('Form submitted successfully', 'success')
            return redirect(url_for('auth.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting form: {str(e)}', 'error')

    return render_template('auth/formulir.html')

@auth.route('/view-formulir/<int:user_id>')
@login_required
@admin_required
def view_formulir_admin(user_id):
    # Get the formulir data
    formulir = Formulir.query.filter_by(user_id=user_id).first_or_404()
    
    if not formulir:
        flash('Formulir not found', 'error')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('auth/view_formulir.html', data=formulir)

@auth.route('/view-formulir')
@login_required
def view_formulir():
    if current_user.role == 'admin':
        return redirect(url_for('auth.dashboard'))
        
    if not current_user.formulir:
        flash('You have not submitted any form yet', 'warning')
        return redirect(url_for('auth.dashboard'))
    return render_template('auth/view_formulir.html', data=current_user.formulir)

@auth.route('/uploads/<path:filename>')
@login_required
def uploads(filename):
    uploads_dir = os.path.join(current_app.root_path,'static', 'uploads')
    return send_from_directory(uploads_dir, filename)

@auth.route('/review/<int:user_id>', methods=['POST'])
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
            return redirect(url_for('auth.dashboard'))
        
        db.session.commit()
        return redirect(url_for('auth.dashboard'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error processing application: {str(e)}', 'error')
        return redirect(url_for('auth.dashboard'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('auth.login'))