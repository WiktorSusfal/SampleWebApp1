from flask import render_template
from flask_login import login_required
from app.main import main_bp


@main_bp.route('/')
@login_required
def hello_world():
    return render_template('main/hello.html')