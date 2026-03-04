import os
from app import create_app, db
from app.models import User

app = create_app()

def setup():
    with app.app_context():
        # 1. Создаем таблицы
        db.create_all()
        
        # 2. Создаем админа, если его нет
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("🚀 База инициализирована. Админ создан.")
        else:
            print("✅ База уже готова. Изменений не требуется.")

if __name__ == "__main__":
    setup()