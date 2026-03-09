from flask import Blueprint, render_template
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

@main_bp.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    new_pass = request.form.get('new_password')
    current_user.set_password(new_pass)
    db.session.commit()
    flash("Пароль успешно изменен!")
    return redirect(url_for('main.profile'))

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