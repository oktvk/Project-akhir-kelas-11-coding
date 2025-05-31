from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import random
import math

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///math_quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    profile = db.relationship('ProfileUser', backref='user', uselist=False)
    quiz_progress = db.relationship('QuizProgress', backref='user', uselist=False)

class ProfileUser(db.Model):
    __tablename__ = "profileuser"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    jk = db.Column(db.String(100), nullable=False)
    hobi = db.Column(db.String(100), nullable=True)
    alamat = db.Column(db.String(255), nullable=True)

class QuizProgress(db.Model):
    __tablename__ = "quizprogress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_score = db.Column(db.Integer, default=0)
    questions_attempted = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    current_level = db.Column(db.Integer, default=1)

def login_required(f):
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

def generate_math_question(level):
    if level == 1:
        operations = ['+', '-', '*']
        operation = random.choice(operations)
        if operation == '+':
            num1 = random.randint(1, 50)
            num2 = random.randint(1, 50)
            answer = num1 + num2
            question = f"{num1} + {num2} = ?"
        elif operation == '-':
            num1 = random.randint(1, 50)
            num2 = random.randint(1, num1)
            answer = num1 - num2
            question = f"{num1} - {num2} = ?"
        else:
            num1 = random.randint(1, 12)
            num2 = random.randint(1, 12)
            answer = num1 * num2
            question = f"{num1} × {num2} = ?"
    elif level == 2:
        operations = ['+', '-', '*', '/']
        operation = random.choice(operations)
        if operation == '/':
            num2 = random.randint(1, 12)
            answer = random.randint(1, 12)
            num1 = num2 * answer
            question = f"{num1} ÷ {num2} = ?"
        else:
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            if operation == '+':
                answer = num1 + num2
                question = f"{num1} + {num2} = ?"
            elif operation == '-':
                answer = num1 - num2
                question = f"{num1} - {num2} = ?"
            else:
                answer = num1 * num2
                question = f"{num1} × {num2} = ?"
    else:
        operations = ['+', '-', '*', '/', '^']
        operation = random.choice(operations)
        if operation == '^':
            num1 = random.randint(1, 10)
            num2 = random.randint(2, 3)
            answer = num1 ** num2
            question = f"{num1} ^ {num2} = ?"
        else:
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            if operation == '+':
                answer = num1 + num2
                question = f"{num1} + {num2} = ?"
            elif operation == '-':
                answer = num1 - num2
                question = f"{num1} - {num2} = ?"
            elif operation == '*':
                answer = num1 * num2
                question = f"{num1} × {num2} = ?"
            else:
                num2 = random.randint(1, 12)
                answer = random.randint(1, 12)
                num1 = num2 * answer
                question = f"{num1} ÷ {num2} = ?"
    return question, answer

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('quiz'))
        return render_template('login.html', error='Username atau password salah.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            return render_template('register.html', error='Username dan password wajib diisi.')
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username sudah terdaftar.')
        hashed = generate_password_hash(password)
        new_user = User(username=username, password=hashed)
        db.session.add(new_user)
        db.session.commit()
        
        prof = ProfileUser(user_id=new_user.id, nama='-', jk='-', hobi='', alamat='-')
        db.session.add(prof)
        
        quiz_progress = QuizProgress(user_id=new_user.id)
        db.session.add(quiz_progress)
        
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    user = User.query.get(session['user_id'])
    progress = QuizProgress.query.filter_by(user_id=user.id).first()
    
    if request.method == 'POST':
        user_answer = float(request.form.get('answer', 0))
        correct_answer = float(request.form.get('correct_answer', 0))
        
        progress.questions_attempted += 1
        if abs(user_answer - correct_answer) < 0.01:
            progress.correct_answers += 1
            progress.total_score += 10
            message = "Correct! Well done!"
        else:
            message = f"Wrong! The correct answer was {correct_answer}"
        
        if progress.total_score >= progress.current_level * 100:
            progress.current_level = min(3, progress.current_level + 1)
        
        db.session.commit()
        return render_template('quiz_result.html', message=message, progress=progress)
    
    question, answer = generate_math_question(progress.current_level)
    return render_template('quiz.html', question=question, correct_answer=answer, progress=progress)

@app.route('/profile')
@login_required
def profile():
    profile = ProfileUser.query.filter_by(user_id=session['user_id']).first()
    progress = QuizProgress.query.filter_by(user_id=session['user_id']).first()
    return render_template('profile.html', profile=profile, progress=progress)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    profile = ProfileUser.query.filter_by(user_id=session['user_id']).first()
    if request.method == 'POST':
        nama = request.form.get('nama', '')
        jk = request.form.get('jk', '')
        hobi = request.form.get('hobi', '')
        alamat = request.form.get('alamat', '')
        if not nama or not jk or not alamat:
            return render_template('edit_profile.html', profile=profile, error='Nama, Jenis Kelamin, dan Alamat wajib diisi.')
        profile.nama = nama
        profile.jk = jk
        profile.hobi = hobi
        profile.alamat = alamat
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('edit_profile.html', profile=profile)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)