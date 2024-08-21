from flask_sqlalchemy  import SQLAlchemy

from app.auth.models.user       import User 
from app.__helpers__.factories import app_db
from app.__config__.settings   import APP_SCHEMA_NAME, LOG_ATTEMPTS_TABLE_NAME


db: SQLAlchemy = app_db


class LoginAttempt(db.Model):
    __tablename__  = LOG_ATTEMPTS_TABLE_NAME
    __table_args__ = {'schema': APP_SCHEMA_NAME}

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    login_time  = db.Column(db.DateTime, nullable=False)
    success     = db.Column(db.Boolean, nullable=False)

    user = db.relationship('User', foreign_keys='LoginAttempt.user_id')