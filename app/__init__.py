from flask import Flask
import logging
import os
from config import Config
from .extensions import db, login_manager, bcrypt, csrf, oauth
from .utils import register_template_utils
from .models import User


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('werkzeug').setLevel(logging.INFO)

    register_extensions(app)
    register_blueprints(app)
    configure_login_manager()
    register_template_utils(app)

    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Database tables created/verified successfully")
                
        except Exception as e:
            app.logger.error(f"Database error: {e}")
            # Don't raise on production to allow app to start
            if app.config.get('DEBUG'):
                raise

    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    
    # Initialize OAuth
    oauth.init_app(app)
    
    # Configure Google OAuth
    google_client_id = os.environ.get('GOOGLE_CLIENT_ID', 'your-google-client-id')
    google_client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', 'your-google-client-secret')
    
    oauth.register(
        name='google',
        client_id=google_client_id,
        client_secret=google_client_secret,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


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
