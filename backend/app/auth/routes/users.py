from flask       import render_template, session, redirect, url_for
from flask_login import login_required, current_user

from app.auth                   import auth_bp
from app.auth.models.user       import User 
from app.__helpers__.utils.admin_required  import admin_required


@auth_bp.route('/users', methods=['GET'])
@login_required
def users():
    if current_user.admin_account == True:
        users = User.query.all()
    else:
        users = User.query.filter_by(id=current_user.id)
    return render_template('auth/users.html', users=users)

@auth_bp.route('/set_user_id/<int:user_id>', methods=['POST'])
@login_required
def set_user_id(user_id):
    session['user_id'] = user_id
    return redirect(url_for('auth.login_attempts'))