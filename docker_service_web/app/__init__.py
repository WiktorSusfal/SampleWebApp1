from dotenv           import load_dotenv

from app.__helpers__.factories import app_db
from app.__helpers__.factories.main_app import create_app


load_dotenv()
main_app      = create_app(app_db)