from flask_login import UserMixin
from flask_sqlalchemy  import SQLAlchemy 
from passlib.context import CryptContext

from app.__helpers__.factories import app_db
from app.__config__.settings   import APP_SCHEMA_NAME, USERS_TABLE_NAME


db: SQLAlchemy = app_db
pwd_ctx        = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto") 


class User(db.Model, UserMixin):
    __tablename__  = USERS_TABLE_NAME
    __table_args__ = {'schema': APP_SCHEMA_NAME}

    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    pwd_hash = db.Column(db.String(255), nullable=False)
    login_attempt  = db.Column(db.Integer, default=0)
    account_locked = db.Column(db.Boolean, default=False)
    lockout_time   = db.Column(db.DateTime, nullable=True)
    admin_account  = db.Column(db.Boolean, default=False)
    login_attempts  = db.relationship('LoginAttempt', backref='fkuser', lazy=True)

    def set_password(self, password: str):
        self.pwd_hash = pwd_ctx.hash(password)
    
    def check_password(self, password: str) -> bool:
        return pwd_ctx.verify(password, self.pwd_hash)