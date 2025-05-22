from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import db, Formulir, Payment
import qrcode
from io import BytesIO
import os
from base64 import b64encode

user = Blueprint('user', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user.route('/dashboard')
@login_required
def dashboard():
    # Get user's form and payment data
    user_form = current_user.formulir
    payment = None
    if user_form:
        payment = Payment.query.filter_by(user_id=current_user.id)\
                             .order_by(Payment.created_at.desc())\
                             .first()
    
    return render_template('user/dashboard.html',
                         user_form=user_form,
                         payment=payment)

@user.route('/formulir', methods=['GET', 'POST'])
@login_required
def formulir():
    if current_user.formulir:
        flash('You have already submitted a form', 'warning')
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        try:
            formulir = Formulir(
                user_id=current_user.id,
                nama=request.form.get('nama'),
                alamat=request.form.get('alamat'),
                nilai=float(request.form.get('nilai'))
            )
            db.session.add(formulir)
            db.session.commit()
            flash('Form submitted successfully', 'success')
            return redirect(url_for('user.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting form: {str(e)}', 'error')
    
    return render_template('user/formulir.html')

@user.route('/submit-payment', methods=['POST'])
@login_required
def submit_payment():
    try:
        if 'payment_proof' not in request.files:
            flash('No payment proof provided', 'error')
            return redirect(url_for('user.dashboard'))
            
        payment_proof = request.files['payment_proof']
        if payment_proof.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('user.dashboard'))
            
        if payment_proof and allowed_file(payment_proof.filename):
            # Create secure filename
            filename = f"payment_{current_user.id}_{secure_filename(payment_proof.filename)}"
            
            # Ensure upload directory exists
            uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(uploads_dir, filename)
            payment_proof.save(file_path)
            
            print(f"Saved payment proof to: {file_path}")  # Debug print
            
            # Verify file exists
            if not os.path.exists(file_path):
                raise Exception("File not saved correctly")
            
            # Create payment record
            payment = Payment(
                user_id=current_user.id,
                amount=float(request.form.get('amount', 500000)),
                payment_proof=filename,
                status='pending'
            )
            
            db.session.add(payment)
            db.session.commit()
            
            flash('Payment proof uploaded successfully', 'success')
            return redirect(url_for('user.dashboard'))
            
    except Exception as e:
        print(f"Error in submit_payment: {str(e)}")  # Debug print
        flash(f'Error submitting payment: {str(e)}', 'error')
        
    return redirect(url_for('user.dashboard'))

@user.route('/print-card')
@login_required
def print_card():
    # Check if user has completed all steps
    if not current_user.formulir or not current_user.is_accepted:
        flash('Anda belum bisa mencetak kartu peserta', 'warning')
        return redirect(url_for('user.dashboard'))
    
    # Get payment status
    payment = Payment.query.filter_by(user_id=current_user.id, status='verified').first()
    if not payment:
        flash('Pembayaran belum diverifikasi', 'warning')
        return redirect(url_for('user.dashboard'))

    try:
        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'ID: {current_user.id} | Nama: {current_user.formulir.nama}')
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert QR code to base64
        buffered = BytesIO()
        qr_img.save(buffered, format="PNG")
        qr_str = b64encode(buffered.getvalue()).decode()
        
        return render_template('user/print_card.html',
                             user=current_user,
                             formulir=current_user.formulir,
                             qr_code=qr_str)
                             
    except Exception as e:
        flash(f'Error generating card: {str(e)}', 'error')
        return redirect(url_for('user.dashboard'))