from flask import render_template, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from app.__helpers__.factories   import app_db
from app.auth                    import auth_bp
from app.auth.forms.registration import RegistrationForm
from app.auth.models.user        import User
from app.__config__.settings     import LOGIN_PAGE_ENDPOINT

db = app_db  


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form: RegistrationForm = RegistrationForm()
    
    if form.validate_on_submit():
        
        user = User(username=form.username.data)
        user.set_password(form.password.data)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Error: Username or email already exists.', 'danger')
            return render_template('auth/register.html', form=form)

        flash('Your account has been created!', 'success')
        return redirect(url_for(LOGIN_PAGE_ENDPOINT))
    
    return render_template('auth/register.html', form=form)