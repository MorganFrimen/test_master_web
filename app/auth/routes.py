from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

# --- ЛОГИКА ВХОДА (LOGIN) ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        # ПРОВЕРКА: Если юзер есть и пароль подошел — ЛОГИНИМ
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        
        # Если не подошел — просто перерисовываем страницу с ошибкой
        flash("Неверный логин или пароль") 
        return render_template('auth/login.html', error="Неверный логин или пароль")

    return render_template('auth/login.html')

# --- ЛОГИКА РЕГИСТРАЦИИ (REGISTER) ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ВОТ ЗДЕСЬ должна быть проверка на "Логин занят"
        if User.query.filter_by(username=username).first():
            return render_template('auth/register.html', error="Этот логин уже занят")

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('main.index'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required # Доступно только тем, кто вошел
def logout():
    logout_user() # Flask-Login удаляет сессию
    return redirect(url_for('auth.login')) # Перенаправляем на вход