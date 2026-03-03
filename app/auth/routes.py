from flask import Blueprint, render_template, redirect, url_for, flash
from app import db # Импортируем базу данных из главного пакета

# Создаем Blueprint. Название 'auth' будет использоваться в url_for('auth.login')
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    # Пока просто возвращаем текст, позже заменим на render_template('auth/login.html')
    return "<h1>Страница входа</h1><p>Введите логин и пароль</p>"

@auth_bp.route('/logout')
def logout():
    return "<h1>Выход из системы</h1>"