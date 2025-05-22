# 📚 PPDB Online System

> A modern web-based application for managing student registrations with role-based access and automated workflows.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🌟 Overview

PPDB Online System is a student registration management platform with:
- Role-based access control (Admin & Student)
- Real-time application tracking
- Secure document upload & QR verification

### 🏠 Halaman Utama
<div align="center">
  <img src="static/images/dokumentasi/landing.png" alt="Homepage" width="100%"/>
  <p>Tampilan halaman utama sistem PMB</p>
</div>

### 🏠 Halaman Utama
<div align="center">
  <img src="static/images/dokumentasi/keterangan pendaftaran.png" alt="Homepage" width="100%"/>
  <p>Tampilan halaman utama sistem PMB</p>
</div>

### 🏠 Halaman Utama
<div align="center">
  <img src="static/images/dokumentasi/detail pendaftaran2.png" alt="Homepage" width="100%"/>
  <p>Tampilan halaman utama sistem PMB</p>
</div>

### 📃 Halaman Register
<div align="center">
  <img src="static/images/dokumentasi/Register.png" alt="Register" width="100%"/>
  <p>Tampilan halaman register sistem PMB</p>
</div>

### 👤 Halaman Login
<div align="center">
  <img src="static/images/dokumentasi/Login.png" alt="Login" width="100%"/>
  <p>Tampilan halaman login sistem PMB</p>
</div>

### 🖊️ Halaman User Dashboard
<div align="center">
  <img src="static/images/dokumentasi/User.png" alt="User Dashboard" width="100%"/>
  <p>Tampilan halaman dashboard user sistem PMB</p>
</div>

### 📃🖊️ Halaman Form Data Diri
<div align="center">
  <img src="static/images/dokumentasi/FormDataDiri.png" alt="Admin2" width="100%"/>
  <p>Tampilan halaman Data Diri sistem PMB</p>
</div>


### 📃🖊️ Halaman Form Akademik
<div align="center">
  <img src="static/images/dokumentasi/FormAkademik.png" alt="Admin2" width="100%"/>
  <p>Tampilan halaman Data Akademik sistem PMB</p>
</div>

### 📃🖊️ Halaman Form Verivication
<div align="center">
  <img src="static/images/dokumentasi/FormVerif.png" alt="Admin2" width="100%"/>
  <p>Tampilan halaman Verivikasi Data sistem PMB</p>
</div>

### ⚙️ Halaman Admin
<div align="center">
  <img src="static/images/dokumentasi/Admin1.png" alt="Admin1" width="100%"/>
  <p>Tampilan halaman utama admin sistem PMB</p>
</div>

### ⚙️ Halaman Admin Panel
<div align="center">
  <img src="static/images/dokumentasi/Admin2.png" alt="Admin2" width="100%"/>
  <p>Tampilan halaman Panel Admin sistem PMB</p>
</div>

---

+Note (FOR MAKE ADMIN USER AND PASSWORD)
$env:FLASK_APP = "app.py"
flask shell
admin = User(username='admin')
admin.set_password('admin123')
admin.role = 'admin'
db.session.add(admin)
db.session.commit()
exit()


## 🎯 Features

### 🔐 Authentication & Roles
- Secure login system
- Admin & Student access roles
- Role-based permissions

### 📝 Registration Management
- Clean & responsive registration form
- Progress tracker
- Document upload
- Auto-generated registration number
- QR code for verification

### 👨‍💼 Admin Dashboard
- Overview of registration statistics
- Review applicant details
- Verify documents
- Update application status
- Manage user accounts

### 🎓 Student Portal
- Complete registration forms
- Upload necessary documents
- Track application status
- View/download registration card with QR code

---

## 🛠️ Tech Stack

| Layer        | Tools Used            |
| ------------ | --------------------- |
| Framework    | Flask (Python)        |
| Database     | SQLAlchemy (SQLite)   |
| Frontend     | HTML, CSS, JavaScript |
| Auth         | Flask-Login           |
| File Upload  | Flask-Upload          |
| QR Code      | `qrcode` Python lib   |

---

## ⚙️ Installation

### 🔧 Clone Repository
```bash
git clone <repository-url>
cd ppdb-online
🐍 Set Up Virtual Environment
bash
Salin
Edit
python -m venv .venv
.venv\Scripts\activate  # For Windows
📦 Install Dependencies
bash
Salin
Edit
pip install -r requirements.txt
🛠️ Configure Environment
bash
Salin
Edit
set FLASK_APP=app.py
set FLASK_ENV=development
🧱 Initialize Database
bash
Salin
Edit
flask db init
flask db migrate
flask db upgrade
👤 Create Admin Account
bash
Salin
Edit
flask create-admin
🚀 Run the App
bash
Salin
Edit
flask run
Access via:
🖥️ http://localhost:5000
🔧 Admin: http://localhost:5000/admin

👤 Default Admin Login
Username: admin

Password: admin123

📋 Registration Flow
📝 Register a student account

✍️ Fill in biodata & academic info

📤 Upload required documents

📊 Track your application

💳 Generate your QR registration card

🔒 Security
Password hashing

Role-based access control

Session management

Secure file upload

Form & input validation

📄 Supported Documents
Birth Certificate

School Certificate

Passport Photo

Family Card

Academic Transcripts

🎨 UI/UX Highlights
Responsive & mobile-friendly

Modern interface

Progress indicators

Real-time status notifications

💻 System Requirements
Python 3.8+

Flask 2.0+

Modern Web Browser

Internet connection

Storage for uploaded files

📞 Support
For issues or contributions, please reach out:

📧 Email: support@ppdb.com

💬 Live Chat: Available on website

📝 License
This project is licensed under the MIT License.

markdown
Salin
Edit

---

### 📌 Tips for Usage:
- Ganti `<repository-url>` dengan URL GitHub repo Anda.
- Bila Anda menggunakan `.env` file untuk variabel, ubah bagian `set FLASK_APP=...` jadi `FLASK_APP=app.py` di `.env`.

Jika Anda ingin saya bantu:
- Menghasilkan versi **Markdown file siap pakai**
- Menambahkan **badge CI/CD**, atau
- Membuat versi **README berbahasa Indonesia** juga

Silakan beri tahu!






Anda bilang:
buat dalam 1 halaman markdown


ChatGPT bilang:
Berikut ini adalah versi README.md satu halaman yang rapi dan menarik untuk ditampilkan di GitHub:

markdown
Salin
Edit
# 📚 PPDB Online System

> Sistem PPDB berbasis web modern dengan autentikasi pengguna, kontrol akses berbasis peran, dan manajemen pendaftaran otomatis.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🌟 Fitur Unggulan

### 🔐 Autentikasi & Peran Pengguna
- Login aman
- Role: Admin & Siswa
- Kontrol akses berbasis peran

### 📝 Manajemen Pendaftaran
- Formulir pendaftaran ramah pengguna
- Pelacakan progres pendaftaran
- Upload dokumen
- Nomor pendaftaran otomatis
- Kartu QR untuk verifikasi

### 👨‍💼 Fitur Admin
- Dashboard statistik pendaftar
- Lihat & verifikasi data pendaftar
- Ubah status aplikasi
- Kelola akun pengguna

### 🎓 Fitur Siswa
- Isi formulir pendaftaran
- Upload dokumen
- Lihat status aplikasi
- Unduh kartu pendaftaran (QR code)

---

## 🛠️ Teknologi

| Kategori     | Teknologi               |
| ------------ | ----------------------- |
| Backend      | Flask (Python)          |
| Database     | SQLAlchemy              |
| Frontend     | HTML, CSS, JavaScript   |
| Autentikasi  | Flask-Login             |
| File Upload  | Flask-Upload            |
| QR Code      | `qrcode` library        |

---

## ⚙️ Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd ppdb-online
2. Buat Virtual Environment
bash
Salin
Edit
python -m venv .venv
.venv\Scripts\activate  # Windows
3. Instal Dependensi
bash
Salin
Edit
pip install -r requirements.txt
4. Konfigurasi Environment
bash
Salin
Edit
set FLASK_APP=app.py
set FLASK_ENV=development
5. Inisialisasi Database
bash
Salin
Edit
flask db init
flask db migrate
flask db upgrade
6. Buat Akun Admin
bash
Salin
Edit
flask create-admin
🚀 Menjalankan Aplikasi
bash
Salin
Edit
flask run
🌐 Website: http://localhost:5000

🔧 Admin Dashboard: http://localhost:5000/admin

👤 Default Admin
Username: admin

Password: admin123

📋 Alur Pendaftaran
Registrasi akun siswa

Isi biodata dan info akademik

Upload dokumen

Lacak status aplikasi

Unduh kartu pendaftaran (QR)

🔐 Keamanan
Password hashing

Role-based access

Manajemen sesi

Validasi input

Upload file aman

📎 Dokumen yang Didukung
Akta kelahiran

Ijazah/sekolah

Pas foto

Kartu keluarga

Transkrip nilai

🎨 Tampilan & UX
Desain responsif (mobile-friendly)

Antarmuka modern

Indikator progres

Notifikasi status

💻 Kebutuhan Sistem
Python 3.8+

Flask 2.0+

Browser modern

