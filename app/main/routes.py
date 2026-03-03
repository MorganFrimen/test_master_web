from flask import Blueprint, render_template

# Создаем "чертеж" модуля
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('main/index.html', title='Главная')