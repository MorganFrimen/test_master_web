from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Test, Question, Option, User # Импортируем наши новые модели
from datetime import datetime
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

@admin_bp.route('/user/toggle-status/<int:user_id>', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    if current_user.role != 'admin':
        return "Доступ запрещен", 403
        
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash("Нельзя заблокировать самого себя!")
        return redirect(url_for('admin.manage_users'))
    
    # Меняем True на False и наоборот
    user.is_active_account = not user.is_active_account
    db.session.commit()
    
    status = "разблокирован" if user.is_active_account else "заблокирован"
    flash(f"Пользователь {user.username} {status}.")
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
@login_required
def create_test():
    # 1. Защита: только админ может создавать тесты
    if current_user.role != 'admin':
        return "Доступ запрещен", 403

    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        category = request.form.get('category') # Получаем из выпадающего списка

        if not title:
            flash("❌ Название теста не может быть пустым")
            return redirect(url_for('admin.create_test'))
        
        # 2. Создаем тест
        new_test = Test(title=title, description=desc, category=category)
        db.session.add(new_test)
        db.session.commit()
        
        flash(f"✅ Тест '{title}' создан! Добавьте вопросы.")
        
        # 3. УМНЫЙ ПЕРЕХОД: идем сразу к добавлению вопросов
        # Мы передаем id нового теста, чтобы знать, куда привязывать вопросы
        return redirect(url_for('admin.add_questions', test_id=new_test.id))
        
    return render_template('admin/create_test.html')

@admin_bp.route('/test/<int:test_id>/questions')
@login_required
def add_questions(test_id):
    test = Test.query.get_or_404(test_id)
    return f"<h1>Добавление вопросов для теста: {test.title}</h1><p>Скоро здесь будет конструктор вопросов!</p>"