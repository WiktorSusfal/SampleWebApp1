from flask       import render_template, redirect, url_for, flash
from flask_login import login_user

from app.auth                   import auth_bp
from app.__config__.settings    import MAIN_PAGE_ENDPOINT
from app.auth.models.user       import User 
from app.auth.forms.login       import LoginForm


users = {'admin': {'password': 'admin'}}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form: LoginForm = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for(MAIN_PAGE_ENDPOINT))
        else:
            flash('Invalid username or password')
    return render_template('auth/login.html', form=form)