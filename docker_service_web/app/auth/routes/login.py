from flask       import render_template, redirect, url_for, flash
from flask_login import login_user

from app.auth                   import auth_bp
from app.__config__.settings    import MAIN_PAGE_ENDPOINT
from app.auth.models.user       import User 
from app.auth.forms.login       import LoginForm


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form: LoginForm = LoginForm()
    if form.validate_on_submit():
        ref_user: User = User.query.filter_by(username=form.username.data).first()
        if ref_user and ref_user.check_password(password=form.password.data):
            login_user(ref_user)
            return redirect(url_for(MAIN_PAGE_ENDPOINT))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)