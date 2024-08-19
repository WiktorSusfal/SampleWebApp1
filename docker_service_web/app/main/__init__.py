from flask import Blueprint

main_bp = Blueprint('main', __name__)

from app.main.routes.hello_world import hello_world