# app/auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db # или просто from app import db, если он там

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Если пользователь уже вошел, ему не нужно регистрироваться снова
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 1. Проверяем, не занят ли логин
        if User.query.filter_by(username=username).first():
            return "<h1>Ошибка</h1><p>Этот логин уже занят. <a href='/register'>Назад</a></p>"

        # 2. Создаем нового пользователя (роль 'user' ставится в модели по умолчанию)
        new_user = User(username=username)
        new_user.set_password(password) # Хешируем!
        
        db.session.add(new_user)
        db.session.commit()

        # 3. После регистрации сразу логиним пользователя
        login_user(new_user)
        return redirect(url_for('main.index'))

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Если пользователь уже вошел, отправляем на главную
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Проверка: не занят ли логин
        if User.query.filter_by(username=username).first():
            return "<h1>Ошибка</h1><p>Логин занят. <a href='/auth/register'>Назад</a></p>"

        # Создаем нового пользователя (роль 'user' по умолчанию в модели)
        new_user = User(username=username)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()

        # Сразу логиним новичка
        from flask_login import login_user
        login_user(new_user)
        return redirect(url_for('main.index'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))