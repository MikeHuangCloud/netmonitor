from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """初始化資料庫"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # 建立預設管理員帳號
        from .user import User
        from config import Config
        
        admin = User.query.filter_by(username=Config.DEFAULT_ADMIN_USERNAME).first()
        if not admin:
            admin = User(
                username=Config.DEFAULT_ADMIN_USERNAME,
                is_admin=True
            )
            admin.set_password(Config.DEFAULT_ADMIN_PASSWORD)
            db.session.add(admin)
            db.session.commit()
            print(f"Created default admin user: {Config.DEFAULT_ADMIN_USERNAME}")
