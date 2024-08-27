from flask       import redirect, url_for
from flask_login import login_required

from app.auth                   import auth_bp
from app.auth.models.user       import User 
from app.__helpers__.utils.admin_required   import admin_required
from app.__helpers__.factories              import app_db


@auth_bp.route('/unlock_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def unlock_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.account_locked = False
        user.login_attempt  = 0
        app_db.session.commit()
    return redirect(url_for('auth.users'))