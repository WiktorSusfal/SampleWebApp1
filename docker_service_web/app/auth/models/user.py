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

    def set_password(self, password: str):
        self.pwd_hash = pwd_ctx.hash(password)
    
    def check_password(self, password: str) -> bool:
        return pwd_ctx.verify(password, self.pwd_hash)