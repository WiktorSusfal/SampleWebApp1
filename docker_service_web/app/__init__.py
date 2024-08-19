import os
from flask                      import Flask
from flask_login                import LoginManager
from dotenv                     import load_dotenv

from app.auth.models.user       import User
from app.__config__.settings    import LOGIN_PAGE_ENDPOINT

load_dotenv()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
    app.logger.info('Creating app')

    login_manager.init_app(app)
    login_manager.login_view = LOGIN_PAGE_ENDPOINT

    from app.main import main_bp
    from app.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.logger.info('Done registering blueprints')

    return app

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)