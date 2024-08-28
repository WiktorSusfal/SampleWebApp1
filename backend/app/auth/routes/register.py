from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

from app.__helpers__.factories   import app_db, app_limiter
from app.auth                    import auth_bp
from app.auth.models.user        import User

db = app_db  


@auth_bp.route('/register', methods=['POST'])
@app_limiter.limit("20 per minute")
def register():
    jdata = request.json
    username = jdata.get('username')
    password = jdata.get('password')
    
    user = User(username=username)
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error: Username or email already exists.'}), 401
    
    return jsonify({'message': 'Your account has been created!'}), 200