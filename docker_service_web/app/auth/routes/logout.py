from flask                      import redirect, url_for
from flask_login                import login_required, logout_user

from app.auth                   import auth_bp
from app.__config__.settings    import LOGIN_PAGE_ENDPOINT


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for(LOGIN_PAGE_ENDPOINT))