import os
from pathlib import Path

from flask import Flask
from sqlalchemy import event
from sqlalchemy.engine import Engine

from config import Config
from app.extensions import db, login_manager


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA busy_timeout=30000")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
    except Exception:
        pass
    finally:
        cursor.close()


def create_app():
    base_dir = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        instance_path=str(base_dir / "instance"),
        instance_relative_config=False,
        template_folder=str(base_dir / "templates"),
        static_folder=str(base_dir / "static"),
    )
    app.config.from_object(Config)
    
    # GARANTE que o banco está no mesmo instance_path do Flask
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(app.instance_path, 'estoque.db')}"


    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.join(app.instance_path, "backups"), exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from app.auth import auth_bp
    from app.routes import main_bp
    from app.models import User

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_environment():
        return {"app_name": "Controle de Estoque"}

    with app.app_context():
        db.create_all()
        ensure_default_admin(User)

    return app


def ensure_default_admin(UserModel):
    if UserModel.query.count() > 0:
        return

    admin = UserModel(
        username=Config.DEFAULT_ADMIN_USERNAME,
        full_name=Config.DEFAULT_ADMIN_FULL_NAME,
        role="admin",
        is_active_user=True,
    )
    admin.set_password(Config.DEFAULT_ADMIN_PASSWORD)
    db.session.add(admin)
    db.session.commit()
