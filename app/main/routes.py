from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db

# Создаем "чертеж" модуля
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('main/index.html', title='Главная')

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html')

@main_bp.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_pass = request.form.get('old_password')
        new_pass = request.form.get('new_password')
        confirm_pass = request.form.get('confirm_password')

        # 1. Проверяем старый пароль
        if not current_user.check_password(old_pass):
            return render_template('main/change_password.html', error="Неверный текущий пароль")

        # 2. Проверяем совпадение новых паролей
        if new_pass != confirm_pass:
            return render_template('main/change_password.html', error="Новые пароли не совпадают")

        # 3. Сохраняем (метод set_password сам захеширует новый пароль)
        current_user.set_password(new_pass)
        db.session.commit()
        
        # Можно добавить сообщение об успехе, но пока просто редирект
        return redirect(url_for('main.profile'))

    return render_template('main/change_password.html')

@main_bp.route('/profile/delete', methods=['POST'])
@login_required
def delete_profile():
    # Админу нельзя удалять себя так просто
    if current_user.role == 'admin':
        flash("Админ не может удалить свой профиль через эту форму.")
        return redirect(url_for('main.profile'))
    
    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for('auth.logout'))

@main_bp.route('/available-tests')
@login_required
def available_tests():
    return render_template('main/available-tests.html', tests=[])