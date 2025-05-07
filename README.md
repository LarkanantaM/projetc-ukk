# 🎓 PROJECT_PMB_SISWA  

Developed by : Lingga arkananta mahardika

*A Web-Based Student Admission System using Flask*

---

## 📝 Deskripsi Proyek

Sistem Manajemen Penerimaan Mahasiswa berbasis web yang memudahkan siswa untuk mendaftar dan admin untuk mengelola proses penerimaan. Sistem ini mencakup autentikasi pengguna, formulir pendaftaran, dan dashboard admin.

---

## 🚀 Fitur Utama

- 🔐 Autentikasi Pengguna (Login / Register)  
- 🧾 Formulir Pendaftaran Mahasiswa  
- 🖥️ Dashboard Admin  
- 📊 Pelacakan Status Aplikasi  
- 👥 Manajemen Role (Admin / Siswa)

---

## 🧰 Tech Stack

- 🐍 Python 3.x  
- 🌐 Flask Framework  
- 🗃️ SQLAlchemy ORM  
- 🛡️ Flask-Login  
- 🎨 Bootstrap 5  
- 🗂️ SQLite

---
## 📁 Struktur Proyek

project-pmb/
├── app/
│ ├── init.py
│ ├── auth/
│ │ ├── init.py
│ │ ├── forms.py
│ │ └── routes.py
│ ├── models/
│ │ ├── init.py
│ │ └── user.py
│ ├── templates/
│ │ ├── auth/
│ │ │ ├── login.html
│ │ │ └── register.html
│ │ └── base.html
│ └── static/
├── config.py
├── run.py
└── requirements.txt

Salin
Edit


## ⚙️ Instalasi

1. 🔽 Clone repositori:
```bash
git clone https://github.com/yourusername/PROJECT_PMB_SISWA.git
cd PROJECT_PMB_SISWA
🧪 Buat virtual environment:

bash
Salin
Edit
python -m venv venv
venv\Scripts\activate  # Windows
# atau
source venv/bin/activate  # Mac/Linux
📦 Install dependencies:

bash
Salin
Edit
pip install -r requirements.txt
🗄️ Inisialisasi database:

bash
Salin
Edit
flask db init
flask db migrate
flask db upgrade
👑 Buat admin user:

bash
Salin
Edit
flask create-admin admin admin@example.com password123
▶️ Menjalankan Aplikasi
bash
Salin
Edit
python run.py
🌐 Akses aplikasi di: http://localhost:5000

👨‍🎓 Panduan Penggunaan
Untuk Siswa:
✍️ Registrasi akun baru

🔐 Login menggunakan akun

📄 Isi formulir pendaftaran

📍 Lacak status aplikasi

Untuk Admin:
🔐 Login sebagai admin

📊 Akses dashboard

✅ Tinjau & setujui / tolak aplikasi

👥 Kelola akun pengguna

🤝 Kontribusi
Fork proyek ini

Buat branch fitur baru:
git checkout -b fitur/NamaFitur

Commit perubahanmu:
git commit -m 'Menambahkan NamaFitur'

Push ke branch:
git push origin fitur/NamaFitur

Buka Pull Request

📄 Lisensi
📜 MIT License – lihat file LICENSE untuk detailnya.

📬 Kontak
Nama Anda – your.email@example.com
🔗 GitHub Repository
