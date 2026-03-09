from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Test, Question, Option, User # Импортируем наши новые модели
from app import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users')
def manage_users():
    # Получаем всех пользователей из базы
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    
    # Защита: нельзя удалить самого себя
    if user_to_delete.id == current_user.id:
        flash("Вы не можете удалить свой собственный аккаунт администратора!")
        return redirect(url_for('admin.manage_users'))
    
    db.session.delete(user_to_delete)
    db.session.commit()
    flash(f"Пользователь {user_to_delete.username} удален.")
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/user/make-admin/<int:user_id>', methods=['POST'])
def make_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.role = 'admin'
    db.session.commit()
    flash(f"Пользователь {user.username} теперь администратор.")
    return redirect(url_for('admin.manage_users'))

# Защищаем весь Blueprint: только админ может сюда заходить
@admin_bp.before_request
@login_required
def check_admin():
    if current_user.role != 'admin':
        return "<h1>Доступ запрещен</h1>", 403

@admin_bp.route('/dashboard')
def dashboard():
    # Главная страница админки: список всех тестов
    all_tests = Test.query.all()
    return render_template('admin/dashboard.html', tests=all_tests)

@admin_bp.route('/test/create', methods=['GET', 'POST'])
def create_test():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        
        new_test = Test(title=title, description=desc)
        db.session.add(new_test)
        db.session.commit()
        
        flash("Тест создан! Теперь добавьте вопросы.")
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/create_test.html')
