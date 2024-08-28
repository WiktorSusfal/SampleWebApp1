from flask       import request, current_app, jsonify
from flask_login import login_user
from datetime    import datetime, timedelta, timezone

from app.auth                   import auth_bp
from app.__helpers__.factories  import app_db, app_limiter
from app.auth.models.user       import User 
from app.auth.models.login_attempt import LoginAttempt


@auth_bp.route('/login', methods=['POST'])
@app_limiter.limit("20 per minute")
def login():
    jdata = request.json
    username = jdata.get('username')
    password = jdata.get('password')
    ref_user: User = User.query.filter_by(username=username).first()

    if not ref_user:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    if ref_user.account_locked:
        if datetime.now(timezone.utc)  > ref_user.lockout_time + timedelta(seconds=current_app.config['ACCOUNT_LOCKOUT_TIME']):
            ref_user.account_locked = False
            ref_user.login_attempt = 0
            app_db.session.commit()
        else:
            return jsonify({'message': 'Your account is locked. Please try again later'}), 401
    
    login_attempt = LoginAttempt(user_id=ref_user.id, login_time=datetime.now(timezone.utc))
    if ref_user.check_password(password):
        ref_user.login_attempt = 0
        
        login_attempt.success = True
        app_db.session.add(login_attempt)
        
        app_db.session.commit()
        login_user(ref_user)
        return jsonify({'message': 'Login successful'}), 200
    else:
        login_attempt.success = False
        app_db.session.add(login_attempt)
        
        ref_user.login_attempt += 1
        if ref_user.login_attempt >= current_app.config['MAX_FAILED_LOGIN_ATTEMPTS']:
            ref_user.account_locked = True
            ref_user.lockout_time = datetime.now(timezone.utc)
            app_db.session.commit()
            return jsonify({'message': 'Your account is locked due to too many failed login attempts.'}), 401
        else:
            app_db.session.commit()
            return jsonify({'message': 'Invalid credentials'}), 401