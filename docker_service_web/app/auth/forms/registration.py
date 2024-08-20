from flask_wtf import FlaskForm 
from wtforms   import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                        DataRequired(message="Field cannot be empty")
                    ,   Length(min=2, max=20, message="Username must be 2 - 20 characters long.")]
                )
    password = PasswordField('Password', validators=[
                        DataRequired(message="Field cannot be empty")
                    ,   Length(min=8, max=20 , message="Password must be 8 - 20 characters long.")
                    ,   Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter.")
                    ,   Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter.")
                    ,   Regexp(r'(?=.*\d)'   , message="Password must contain at least one digit.")
                    ,   Regexp(r'(?=.*[!@#$%^&*(),.?":{}|<>])', message="Password must contain at least one special character.")]
                )
    submit   = SubmitField('Register')