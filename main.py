# from fastapi import FastAPI, Request, Form, Depends, File, UploadFile
# from fastapi.responses import HTMLResponse, RedirectResponse

# from fastapi_login import LoginManager
from object import *

from fastapi import FastAPI, Request
from fastapi import FastAPI, Request, Form, Depends, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm

import os, base64
import random

from fastapi.security import OAuth2PasswordRequestForm
import ZODB, ZODB.FileStorage
import transaction
import BTrees._OOBTree
from datetime import datetime, timedelta
import os

class NotAuthenticatedException(Exception):
    pass

def generate_session():
    return base64.b64encode(os.urandom(16))

SECRET = generate_session()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

manager = LoginManager(SECRET, token_url='/login', use_cookie=True, custom_exception=NotAuthenticatedException)
manager.cookie_name = "session"

storage = ZODB.FileStorage.FileStorage('data/bankData.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

# #create root if it does not exist
if not hasattr(root, "customers"):
    root.customers = BTrees.OOBTree.BTree()
if not hasattr(root, "admin"):
    root.admin = BTrees.OOBTree.BTree()
if not hasattr(root, "accounts"):
    root.accounts = BTrees.OOBTree.BTree()
if not hasattr(root, "transfers"):
    root.transfers = BTrees.OOBTree.BTree()
if not hasattr(root, "withdrawals"):
    root.withdrawals = BTrees.OOBTree.BTree()
if not hasattr(root, "currency"):
    root.currency = BTrees.OOBTree.BTree()
    currencyID = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "SGD", "HKD", "NZD", "SEK", "DKK", "NOK", "KRW", "TWD", "MYR", "IDR", "INR", "PHP", "VND", "ZAR"]
    currencyName = ["United States Dollar", "Euro", "British Pound Sterling", "Japanese Yen", "Australian Dollar", "Canadian Dollar", "Swiss Franc", "Chinese Yuan", "Singapore Dollar", "Hong Kong Dollar", "New Zealand Dollar", "Swedish Krona", "Danish Krone", "Norwegian Krone", "South Korean Won", "New Taiwan Dollar", "Malaysian Ringgit", "Indonesian Rupiah", "Indian Rupee", "Philippine Peso", "Vietnamese Dong", "South African Rand"]
    currencyRate = [
        [35.41, 35.57],  # USD
        [39.00, 39.17],  # EUR
        [45.10, 45.25],  # GBP
        [0.244, 0.246],  # JPY
        [23.94, 24.15],  # AUD
        [26.50, 26.70],  # CAD
        [40.12, 40.32],  # CHF
        [4.88, 4.91],    # CNY
        [26.83, 27.00],  # SGD
        [4.54, 4.57],    # HKD
        [21.10, 21.20],  # NZD
        [3.35, 3.37],    # SEK
        [5.23, 5.25],    # DKK
        [3.26, 3.28],    # NOK
        [0.025, 0.026],  # KRW
        [1.08, 1.10],    # TWD
        [7.95, 8.00],    # MYR
        [0.002, 0.0022], # IDR
        [0.423, 0.425],  # INR
        [0.615, 0.617],  # PHP
        [0.0015, 0.0016],# VND
        [1.92, 1.95]     # ZAR
    ]

    
    for i in range(len(currencyID)):
        root.currency[currencyID[i]] = Currency(currencyID[i], currencyName[i], currencyRate[i])
        transaction.commit()
  
#load user
# @manager.user_loader()
# def load_user(email: str):
#     user = None

#     for t in root.teachers:
#         if email == root.teachers[t].getEmail():
#             user = root.teachers[t]
    
#     for s in root.students:
#         if email == root.students[s].getEmail():
#             user = root.students[s]

#     return user

#check if the user is login
# @app.exception_handler(NotAuthenticatedException)
# def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
#     return RedirectResponse(url='/login')

#redirect to the correct home page (teacher or student)
# @app.get("/", response_class=HTMLResponse)
# async def redirect(request: Request, user_info=Depends(manager)):
#     if isinstance(user_info, Student):
#         return RedirectResponse(url="/home_student", status_code=302)
#     elif isinstance(user_info, Teacher):
#         return RedirectResponse(url="/home_teacher", status_code=302)
 
#login
@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

#home
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("homeAdmin.html", {"request": request})

@app.get("/admin-home", response_class=HTMLResponse)
async def homeAdmin(request: Request):
    return templates.TemplateResponse("homeAdmin.html", {"request": request})

@app.get("/transfer", response_class=HTMLResponse)
async def transfer(request: Request):
    return templates.TemplateResponse("transfer.html", {"request": request})


#withdraw
@app.get("/withdraw", response_class=HTMLResponse)
async def withdraw(request: Request):
    return templates.TemplateResponse("withdrawal.html", {"request": request})

def generate_otp(length=6):
    """Generate a random OTP of specified length."""
    otp = ''.join(random.choices('0123456789', k=length))
    return otp

@app.get("/withdraw/{otp}", response_class=HTMLResponse)
async def withdrawOtp(request: Request, otp: str):
    otp = generate_otp()
    return templates.TemplateResponse("withdrawalOtp.html", {"request": request, "otp": otp})

@app.get("/transfer/review", response_class=HTMLResponse)
async def transferReview(request: Request):
    return templates.TemplateResponse("transferReview.html", {"request": request})

#currency exchange         
@app.get("/currency-exchange", response_class=HTMLResponse)
async def currencyExchange(request: Request):
    return templates.TemplateResponse("currencyExchange.html", {"request": request})

@app.get("/admin/currency-exchange", response_class=HTMLResponse)
async def currencyExchangeAdmin(request: Request):
    return templates.TemplateResponse("currencyExchangeAdmin.html", {"request": request})

@app.post("/get-currency-rate/{currencyID}")
async def getCurrencyRate(request: Request, currencyID: str):
    currencyRate = root.currency[currencyID].getCurrencyRate()
    return {"buyRate": currencyRate[0], "sellRate": currencyRate[1]}

@app.get("/fakeAtm", response_class=HTMLResponse)
async def fakeAtm(request: Request):
    return templates.TemplateResponse("fakeAtm.html", {"request": request})

@app.get("/fakeAtm/confirmation", response_class=HTMLResponse)
async def fakeAtmConfirmation(request: Request):
    return templates.TemplateResponse("fakeAtmConfirmation.html", {"request": request})

@app.get("/fakeAtm/success", response_class=HTMLResponse)
async def fakeAtmSuccess(request: Request):
    return templates.TemplateResponse("fakeAtmSuccesshtml", {"request": request})

@app.get("/admin/user-management", response_class=HTMLResponse)
async def userManagement(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})