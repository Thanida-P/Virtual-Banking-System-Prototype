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
import bcrypt

from fastapi.security import OAuth2PasswordRequestForm
import ZODB, ZODB.FileStorage
import transaction
import BTrees._OOBTree
import secrets
from datetime import datetime, timedelta
import os

class NotAuthenticatedException(Exception):
    pass

def generate_session():
    return  base64.urlsafe_b64encode(secrets.token_bytes(32))

SECRET = generate_session()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

manager = LoginManager(SECRET, token_url='/login', use_cookie=True, custom_exception=NotAuthenticatedException)
manager.cookie_name = "session"

storage = ZODB.FileStorage.FileStorage('data/bankdatabase.fs')
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
@manager.user_loader()
def load_user(username: str):
    user = None

    for c in root.customers:
        if username == root.customers[c].getUsername():
            user = root.customers[c]
    
    for s in root.admin:
        if username == root.admin[s].getUsername():
            user = root.admin[s]

    return user

#check if the user is login
@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse(url='/login')

#redirect to the correct home page (teacher or student)
@app.get("/", response_class=HTMLResponse)
async def redirect(request: Request, user_info=Depends(manager)):
    if isinstance(user_info, UserAccount):
        return RedirectResponse(url="/home", status_code=302)
    elif isinstance(user_info, AdminAccount):
        return RedirectResponse(url="/home_admin", status_code=302)
 
#login
@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

#home
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/admin-home", response_class=HTMLResponse)
async def homeAdmin(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("homeAdmin.html", {"request": request})

@app.get("/transfer", response_class=HTMLResponse)
async def transfer(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("transfer.html", {"request": request})


#withdraw
@app.get("/withdraw", response_class=HTMLResponse)
async def withdraw(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("withdrawal.html", {"request": request})

def generate_otp(length=6):
    """Generate a random OTP of specified length."""
    otp = ''.join(random.choices('0123456789', k=length))
    return otp

@app.get("/withdraw/{otp}", response_class=HTMLResponse)
async def withdrawOtp(request: Request, otp: str, user=Depends(manager)):
    otp = generate_otp()
    return templates.TemplateResponse("withdrawalOtp.html", {"request": request, "otp": otp})

@app.get("/transfer/review", response_class=HTMLResponse)
async def transferReview(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("transferReview.html", {"request": request})

#currency exchange         
@app.get("/currency-exchange", response_class=HTMLResponse)
async def currencyExchange(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("currencyExchange.html", {"request": request})

@app.get("/admin/currency-exchange", response_class=HTMLResponse)
async def currencyExchangeAdmin(request: Request):
    return templates.TemplateResponse("currencyExchangeAdmin.html", {"request": request})

@app.post("/get-currency-rate/{currencyID}")
async def getCurrencyRate(request: Request, user=Depends(manager), currencyID: str = ""):
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

@app.get("/signUp", response_class=HTMLResponse)
async def signUp(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/signUpSubmission", response_class=HTMLResponse)
async def signUpSubmission(request: Request, firstName: str = Form(None), middleName: str = Form(None), lastName: str = Form(None), username: str = Form(None), maritalstatus: str = Form(None), education: str = Form(None), citizenId: str = Form(None), email: str = Form(None), phno: str = Form(None), password: str = Form(None), confirmPassword: str = Form(None), bankAccount: str = Form(None), termCheck: str = Form(None), file: UploadFile = File(None)):
    required_params = [firstName, middleName, lastName, username, citizenId, email, phno, password, confirmPassword, bankAccount, file, maritalstatus, education]
    if any(param is None for param in required_params):
        return f"<script> alert(\"Please fill out all fields\"); window.history.back(); </script>"

    elif termCheck != "true":
        return f"<script> alert(\"Please check the terms and conditions\"); window.history.back(); </script>"
    
    elif password != confirmPassword:
        return f"<script> alert(\"Password does not match\"); window.history.back(); </script>"
    elif not allowed_file(file.filename):
        return f"<script> alert(\"Invalid file type\"); window.history.back(); </script>"
    else:
        filename = file.filename
        filedata = file.file.read()
        if not os.path.exists(f"profile/{username}"):
            os.makedirs(f"profile/{username}")
        filepath = f"profile/{username}/{filename}" if username else "profile/{filename}"
        with open(filepath, "wb") as f:
            f.write(filedata)
            
        hashPassword = hash_password(password)

        for user in root.customers.values():
            if user.getCitizenID() == citizenId:
                return f"<script> alert(\"User already exists\"); window.history.back(); </script>"
            if user.getUsername() == username:
                return f"<script> alert(\"Username already exists\"); window.history.back(); </script>"
            
        user = UserAccount(filename, firstName, middleName, lastName, username, hashPassword, citizenId, maritalstatus, education, email, phno)
        root.customers[user.getUsername()] = user
        transaction.commit()
        return RedirectResponse(url="/login", status_code=302)

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

@app.get("/login", response_class=HTMLResponse)
async def logIn(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login_info(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
        
    user = load_user(username)
    
    if not user:
        return f"<script> alert(\"User does not exist\"); window.history.back(); </script>"
    elif verify_password(password, user.getPassword()) == False:
        return f"<script> alert(\"Incorrect password\"); window.history.back(); </script>"
    
    access_token = manager.create_access_token(data={'sub': username}, expires=timedelta(hours=1))
    
    response = RedirectResponse(url="/home", status_code=302)
        
    manager.set_cookie(response, access_token)
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session", httponly=True, secure=True, samesite="lax")
    return response