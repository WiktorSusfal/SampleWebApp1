from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from app.auth.routes.login  import login
from app.auth.routes.logout import logout