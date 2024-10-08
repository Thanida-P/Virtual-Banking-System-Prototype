from app.db.database import SessionLocal
import bcrypt
from fastapi_login import LoginManager
import base64
import secrets
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./templates")

class NotAuthenticatedException(Exception):
    pass

def generate_session():
    return  base64.urlsafe_b64encode(secrets.token_bytes(32))

SECRET = generate_session()

manager = LoginManager(SECRET, token_url='/login', use_cookie=True, not_authenticated_exception=NotAuthenticatedException)
manager.cookie_name = "session"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
