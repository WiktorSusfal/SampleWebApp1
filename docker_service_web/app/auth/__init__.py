from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from app.auth.routes.login          import login
from app.auth.routes.logout         import logout
from app.auth.routes.register       import register
from app.auth.routes.users          import users
from app.auth.routes.login_attempts import login_attempts
from app.auth.routes.unlock_user    import unlock_user