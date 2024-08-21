from flask_login import LoginManager

def create_login_manager() -> LoginManager:
    login_manager = LoginManager()
    
    from app.auth.models.user import User
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    login_manager.user_loader(load_user)
    return login_manager