from flask       import render_template, redirect, url_for, session
from flask_login import login_required

from app.auth                       import auth_bp
from app.auth.models.user           import User
from app.auth.models.login_attempt  import LoginAttempt
from app.__helpers__.utils.admin_required  import admin_required


@auth_bp.route('/login_attempts', methods=['GET'])
@login_required
def login_attempts():
    user_id = session.get('user_id')
    
    user = User.query.get(user_id)
    if user:
        login_history = LoginAttempt.query.filter_by(user_id=user.id).all()
        return render_template('auth/login_attempts.html', login_history=login_history, user=user)
    return redirect(url_for('auth.users'))