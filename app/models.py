from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    """Функция для flask-login: находит пользователя в базе по его ID"""
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    """Модель пользователя (Админ или Сотрудник)"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), default='user') # 'admin' или 'user'
    is_active_account = db.Column(db.Boolean, default=True) 
    
    @property
    def is_active(self):
        return self.is_active_account

    # Связь с результатами тестов (один ко многим)
    results = db.relationship('TestResult', backref='author', lazy='dynamic')

    def set_password(self, password):
        """Превращает обычный пароль в защищенный хеш"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверяет, совпадает ли введенный пароль с хешем в базе"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Test(db.Model):
    """Модель теста (создается админом)"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    category = db.Column(db.String(64)) # Например, "Безопасность"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Test {self.title}>'

class TestResult(db.Model):
    """Модель результатов прохождения теста"""
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    # Связь с пользователем через ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)

    def __repr__(self):
        return f'<Result {self.score}/{self.total_questions} by User {self.user_id}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    
    # Тип вопроса: 'single' (один ответ) или 'multi' (несколько)
    q_type = db.Column(db.String(10), default='single') 

    # Связь с ответами (один ко многим)
    options = db.relationship('Option', backref='question', lazy='dynamic', cascade="all, delete-orphan")

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    
    # Флаг: является ли этот конкретный вариант правильным
    is_correct = db.Column(db.Boolean, default=False)
    
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)