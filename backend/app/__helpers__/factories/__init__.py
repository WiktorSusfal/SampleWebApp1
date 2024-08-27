from flask_sqlalchemy   import SQLAlchemy
from flask_limiter      import Limiter
from flask_limiter.util import get_remote_address

app_db        = SQLAlchemy()
app_limiter   = Limiter(key_func=get_remote_address, default_limits=["120 per minute"])