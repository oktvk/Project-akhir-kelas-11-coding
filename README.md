Aplikasi Kuis Matematika

Aplikasi kuis matematika sederhana untuk berlatih matematika. Dibuat dengan Flask (mengikuti arsitektur MVC dari sir sepri).

-- Fitur

- Login dan registrasi user
- Kuis matematika dengan 3 level kesulitan
- Profil user dengan statistik kuis
- Sistem scoring dan level up otomatis

-- Cara Pakai

1. Install Python 3.x
2. Install package yang dibutuhkan:
   ```
   pip install flask flask-sqlalchemy werkzeug
   ```
3. Jalankan aplikasi:
   ```
   python app.py
   ```
4. Buka browser dan akses `http://localhost:5000`

-- Cara Main

1. Register dulu untuk bikin akun baru
2. Login dengan akun yang sudah dibuat
3. Isi profil kamu (nama, jenis kelamin, dll)
4. Mulai main kuis matematika
5. Jawab pertanyaan yang muncul
6. Dapet 10 poin untuk setiap jawaban benar
7. Level naik otomatis kalau udah dapet skor tertentu

-- Level Kuis

1. Level 1: Pertanyaan sederhana (1-10 poin)
   - Penjumlahan (1-50)
   - Pengurangan (1-50)
   - Perkalian (1-12)

2. Level 2: Pertanyaan sedang (11-20 poin)
   - Semua operasi level 1
   - Pembagian
   - Angka lebih besar (1-100)

3. Level 3: Pertanyaan sulit (21-30 poin)
   - Semua operasi level 2
   - Pangkat
   - Soal lebih kompleks

-- Teknologi

- Backend: Python Flask
- Database: SQLite
- Frontend: HTML, CSS, Bootstrap 5

-- Struktur Database

1. User
   - id (Primary Key)
   - username
   - password (hashed)

2. ProfileUser
   - id (Primary Key)
   - user_id (Foreign Key)
   - nama
   - jk (jenis kelamin)
   - hobi
   - alamat

3. QuizProgress
   - id (Primary Key)
   - user_id (Foreign Key)
   - total_score
   - questions_attempted
   - correct_answers
   - current_level

-- Penjelasan Kode

1. Model (Database)
   - User: Menyimpan data login user (username & password)
   - ProfileUser: Menyimpan data profil user (nama, jenis kelamin, dll)
   - QuizProgress: Menyimpan progress kuis user (skor, level, dll)

2. Route (Controller)
   - /: Halaman login
   - /register: Halaman registrasi
   - /quiz: Halaman kuis matematika
   - /profile: Halaman profil user
   - /profile/edit: Halaman edit profil
   - /logout: Logout user

3. Template (View)
   - login.html: Form login
   - register.html: Form registrasi
   - quiz.html: Tampilan kuis
   - quiz_result.html: Hasil jawaban kuis
   - profile.html: Tampilan profil
   - edit_profile.html: Form edit profil

4. Fungsi Utama
   - generate_math_question(): Generate soal matematika sesuai level
   - login_required(): Cek user sudah login atau belum
   - check_password_hash(): Cek password user
   - generate_password_hash(): Enkripsi password

5. User guide
   a. User register/login
   b. Isi profil (opsional)
   c. Mulai kuis:
      - Generate soal sesuai level
      - User jawab
      - Cek jawaban
      - Update skor & level
      - Tampilkan hasil
   d. Lihat progress di profil

-- Dibuat oleh
IMMANUEL LOVEL ARIYANTO
Kelas XI IPA I 