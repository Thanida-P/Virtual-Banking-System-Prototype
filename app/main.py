import logging

logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI, HTTPException, Request, status
from fastapi import FastAPI, Request, Form, Depends, File, UploadFile, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from app.db import crud, models, schema
from app.db.database import SessionLocal, engine


import os, base64
import random
import bcrypt

import secrets
from datetime import datetime, timedelta
import os

from app.api.authenticator import *
from app.api.userAccountManagement import *
from app.api.transfer import *
from app.api.transaction import *
from app.api.dependencies import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(authenticator)
app.include_router(userAccount)
app.include_router(transferMoney)
app.include_router(transactionMoney)

if os.getenv("SERVICE") == "authenticator":
    from app.api.authenticator import authenticator as auth_router
    app.include_router(auth_router, prefix="/authenticator")
elif os.getenv("SERVICE") == "userAccount":
    from app.api.userAccountManagement import userAccount as userAccount_router
    app.include_router(userAccount_router, prefix="/userAccount")
elif os.getenv("SERVICE") == "transfer":
    from app.api.transfer import transferMoney as transfer_router
    app.include_router(transfer_router, prefix="/transfer")
elif os.getenv("SERVICE") == "transaction":
    from app.api.transaction import transactionMoney as transaction_router
    app.include_router(transaction_router, prefix="/transaction")

#check if the user is login
@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse(url='/login')

@manager.user_loader()
def load_user(username: str):
    db =  next(get_db())
    user = crud.getUser(db, username) 
    return user

#redirect to the correct home page (teacher or student)
@app.get("/", response_class=HTMLResponse)
async def redirect(request: Request, user_info=Depends(manager)):
    if isinstance(user_info, models.UserAccount):
        return RedirectResponse(url="/home", status_code=302)
    elif isinstance(user_info, models.AdminAccount):
        return RedirectResponse(url="/admin-home", status_code=302)


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request,  db: Session = Depends(get_db), user=Depends(manager)):
    if isinstance(user, models.UserAccount):
        id = user.id
        defaultBank = db.query(models.BankAccount).filter(models.BankAccount.accountId == id).first()
        balance = float(defaultBank.balance)
        return templates.TemplateResponse("home.html", {"request": request, "firstname": user.firstname, "balance": balance})
    return RedirectResponse(url="/admin-home", status_code=302)

@app.get("/admin-home", response_class=HTMLResponse)
async def homeAdmin(request: Request, user=Depends(manager)):
    if isinstance(user, models.AdminAccount):
        return templates.TemplateResponse("homeAdmin.html", {"request": request, "firstname": user.firstname})
    return RedirectResponse(url="/home", status_code=302)