import os
from flask                      import Flask, current_app
from flask_talisman             import Talisman
from flask_login                import LoginManager
from flask_sqlalchemy           import SQLAlchemy

from app.__config__.settings    import LOGIN_PAGE_ENDPOINT


def create_app(app_db: SQLAlchemy) -> Flask:
    app = Flask(__name__, template_folder='../../templates')
    app.config['SECRET_KEY']                     = os.getenv('APP_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI']        = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SECURE']          = True
    app.config['SESSION_COOKIE_HTTPONLY']        = True
    app.config['SESSION_COOKIE_SAMESITE']        = 'Lax'
    app.config['MAX_FAILED_LOGIN_ATTEMPTS']      = 5
    app.config['ACCOUNT_LOCKOUT_TIME']           = 10 * 60  
    app.config['ADMIN_DEFAULT_USERNAME']         = 'admin'
    app.config['ADMIN_DEFAULT_PASSWORD']         = 'admin'

    Talisman(app, force_https=True)

    app_db.init_app(app)
    with app.app_context():
        if int(os.getenv('APP_RESET_USERS')) == 1:
            reset_users(app_db)

    login_manager = create_login_manager()
    login_manager.init_app(app)
    login_manager.login_view = LOGIN_PAGE_ENDPOINT

    from app.main import main_bp
    from app.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

def create_login_manager() -> LoginManager:
    login_manager = LoginManager()
    
    from app.auth.models.user import User
    def load_user(user_id: int):
        return User.query.get(int(user_id))
    
    login_manager.user_loader(load_user)
    return login_manager


def reset_users(app_db: SQLAlchemy):
    from app.auth.models.user import User
    from app.auth.models.login_attempt import LoginAttempt
    app_db.session.query(LoginAttempt).delete()
    app_db.session.query(User).delete()
    app_db.session.commit()

    admin = User(username=current_app.config['ADMIN_DEFAULT_USERNAME'], admin_account=True)
    admin.set_password(current_app.config['ADMIN_DEFAULT_PASSWORD'])

    app_db.session.add(admin)
    app_db.session.commit()