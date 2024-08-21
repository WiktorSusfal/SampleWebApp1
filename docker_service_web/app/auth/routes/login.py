from flask       import request, current_app, render_template, redirect, url_for, flash
from flask_login import login_user
from datetime    import datetime, timedelta, timezone

from app.auth                   import auth_bp
from app.__config__.settings    import MAIN_PAGE_ENDPOINT
from app.__helpers__.factories  import app_db
from app.auth.models.user       import User 
from app.auth.models.login_attempt import LoginAttempt
from app.auth.forms.login       import LoginForm


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html', form=LoginForm(request.form))

    username = request.form['username']
    password = request.form['password']
    ref_user: User = User.query.filter_by(username=username).first()

    if not ref_user:
        flash('Invalid username or password')
        return render_template('auth/login.html', form=LoginForm(request.form))
    
    if ref_user.account_locked:
        if datetime.now(timezone.utc)  > ref_user.lockout_time + timedelta(seconds=current_app.config['ACCOUNT_LOCKOUT_TIME']):
            ref_user.account_locked = False
            ref_user.login_attempt = 0
            app_db.session.commit()
        else:
            flash('Your account is locked. Please try again later.')
            return render_template('auth/login.html', form=LoginForm(request.form))
    
    login_attempt = LoginAttempt(user_id=ref_user.id, login_time=datetime.now(timezone.utc))
    if ref_user.check_password(password):
        ref_user.login_attempt = 0
        
        login_attempt.success = True
        app_db.session.add(login_attempt)
        
        app_db.session.commit()
        login_user(ref_user)
        return redirect(url_for(MAIN_PAGE_ENDPOINT))
    else:
        login_attempt.success = False
        app_db.session.add(login_attempt)
        
        ref_user.login_attempt += 1
        if ref_user.login_attempt >= current_app.config['MAX_FAILED_LOGIN_ATTEMPTS']:
            ref_user.account_locked = True
            ref_user.lockout_time = datetime.now(timezone.utc)
            flash('Your account is locked due to too many failed login attempts.')
        else:
            flash('Invalid username or password')
        app_db.session.commit()
    
    return render_template('auth/login.html', form=LoginForm(request.form))