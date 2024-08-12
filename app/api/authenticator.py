from fastapi import APIRouter, Depends

import base64
import secrets
import bcrypt

from app.db import models, schema, crud
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.dependencies import get_db
from app.api.dependencies import *

from datetime import timedelta

authenticator = APIRouter()
authenticator.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

def createModerator(db:Session):
    if not db.query(models.AdminAccount).filter_by(username="admin").first():
        # Create a new AdminAccount if it doesn't exist
        admin_user = schema.AdminCreate(
            username="admin",
            firstname="admin",
            middlename="",
            lastname="admin",
            password=hash_password("BankMatrixAdmin"),
            balance=0,
            email="admin@gmail.com",
            phno="0000000000"
        )

        crud.createAdmin(db, admin_user)

@manager.user_loader()
def load_user(username: str):
    db =  next(get_db())
    user = crud.getUser(db, username) 
    return user

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

@authenticator.get("/login", response_class=HTMLResponse)
async def logIn(request: Request, db: Session = Depends(get_db)):
    createModerator(db)
    return templates.TemplateResponse("login.html", {"request": request})

@authenticator.post("/login", response_class=HTMLResponse)
async def login_info(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
        
    user = load_user(username)
    
    if not user:
        return f"<script> alert(\"User does not exist\"); window.history.back(); </script>"
    elif verify_password(password, user.password) == False:
        return f"<script> alert(\"Incorrect password\"); window.history.back(); </script>"
    
    access_token = manager.create_access_token(data={'sub': username}, expires=timedelta(hours=1))
    if isinstance(user, models.AdminAccount):
        if user.username == "admin" and password == "BankMatrixAdmin":
            response = RedirectResponse(url="/addAdmin", status_code=302)
        else:
            response = RedirectResponse(url="/admin-home", status_code=302)
    else:
        response = RedirectResponse(url="/home", status_code=302) 
 
    manager.set_cookie(response, access_token)
    return response

@authenticator.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session", httponly=True, secure=True, samesite="lax")
    return response