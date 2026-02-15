from flask import Flask
from config import Config, ProductionConfig
from .extensions import db, login_manager, bcrypt, csrf
from .utils import register_template_utils
from .models import User
import os


def create_app(config_class: type[Config] = None) -> Flask:
    if config_class is None:
        config_class = ProductionConfig if os.environ.get('FLASK_ENV') == 'production' else Config
    
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_extensions(app)
    register_blueprints(app)
    configure_login_manager()
    register_template_utils(app)

    # Only create tables in development
    if os.environ.get('FLASK_ENV') != 'production':
        with app.app_context():
            db.create_all()

    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)


def register_blueprints(app: Flask) -> None:
    from .views.auth import auth_bp
    from .views.dashboard import dashboard_bp
    from .views.admin import admin_bp
    from .views.manager import manager_bp
    from .views.clipper import clipper_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(manager_bp)
    app.register_blueprint(clipper_bp)


def configure_login_manager() -> None:
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        return User.query.get(int(user_id))


# Create app instance for gunicorn
app = create_app()
