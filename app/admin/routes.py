from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Test, Question, Option # Импортируем наши новые модели
from app import db

admin_bp = Blueprint('admin', __name__)

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