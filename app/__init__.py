from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 1. Создаем объекты расширений вне функции. 
# Это нужно, чтобы другие модули (models.py, routes.py) могли их импортировать, 
# не вызывая само приложение.
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Функция-фабрика для создания и настройки приложения"""
    app = Flask(__name__)

    # 2. Настройки (Конфигурация)
    app.config['SECRET_KEY'] = 'dev-key-777'
    # База данных будет лежать в папке instance/project.db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. Инициализация расширений внутри приложения
    db.init_app(app)
    login_manager.init_app(app)
    
    # Указываем Flask-Login, куда перенаправлять гостя, если он лезет на закрытую страницу
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Пожалуйста, войдите в систему."

    # 4. Регистрация Blueprints (наших папок-модулей)
    # Мы импортируем их ВНУТРИ функции, чтобы избежать циклической зависимости
    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app import models 

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app