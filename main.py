# from object import *
import logging

logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI, HTTPException, Request
from fastapi import FastAPI, Request, Form, Depends, File, UploadFile, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from db import crud, models, schema
from db.database import SessionLocal, engine


import os, base64
import random
import bcrypt

from fastapi.security import OAuth2PasswordRequestForm
import secrets
from datetime import datetime, timedelta
import os

class NotAuthenticatedException(Exception):
    pass

def generate_session():
    return  base64.urlsafe_b64encode(secrets.token_bytes(32))

SECRET = generate_session()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

manager = LoginManager(SECRET, token_url='/login', use_cookie=True, custom_exception=NotAuthenticatedException)
manager.cookie_name = "session"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

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
        
# if not hasattr(root, "currency"):
#     root.currency = BTrees.OOBTree.BTree()
#     currencyID = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "SGD", "HKD", "NZD", "SEK", "DKK", "NOK", "KRW", "TWD", "MYR", "IDR", "INR", "PHP", "VND", "ZAR"]
#     currencyName = ["United States Dollar", "Euro", "British Pound Sterling", "Japanese Yen", "Australian Dollar", "Canadian Dollar", "Swiss Franc", "Chinese Yuan", "Singapore Dollar", "Hong Kong Dollar", "New Zealand Dollar", "Swedish Krona", "Danish Krone", "Norwegian Krone", "South Korean Won", "New Taiwan Dollar", "Malaysian Ringgit", "Indonesian Rupiah", "Indian Rupee", "Philippine Peso", "Vietnamese Dong", "South African Rand"]
#     currencyRate = [
#         [35.41, 35.57],  # USD
#         [39.00, 39.17],  # EUR
#         [45.10, 45.25],  # GBP
#         [0.244, 0.246],  # JPY
#         [23.94, 24.15],  # AUD
#         [26.50, 26.70],  # CAD
#         [40.12, 40.32],  # CHF
#         [4.88, 4.91],    # CNY
#         [26.83, 27.00],  # SGD
#         [4.54, 4.57],    # HKD
#         [21.10, 21.20],  # NZD
#         [3.35, 3.37],    # SEK
#         [5.23, 5.25],    # DKK
#         [3.26, 3.28],    # NOK
#         [0.025, 0.026],  # KRW
#         [1.08, 1.10],    # TWD
#         [7.95, 8.00],    # MYR
#         [0.002, 0.0022], # IDR
#         [0.423, 0.425],  # INR
#         [0.615, 0.617],  # PHP
#         [0.0015, 0.0016],# VND
#         [1.92, 1.95]     # ZAR
#     ]

    
#     for i in range(len(currencyID)):
#         root.currency[currencyID[i]] = Currency(currencyID[i], currencyName[i], currencyRate[i])
#         transaction.commit()

@manager.user_loader()
def load_user(username: str):
    db =  next(get_db())
    user = crud.getUser(db, username) 
    return user

#check if the user is login
@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse(url='/login')

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

@app.get("/transfer", response_class=HTMLResponse)
async def transfer(request: Request, db: Session = Depends(get_db), user=Depends(manager)):
    if isinstance(user, models.UserAccount):
        accounts = crud.getBankAccountsOfUser(db, user.id)
        return templates.TemplateResponse("transfer.html", {"request": request, "firstname": user.firstname,  "accounts": accounts})
    return RedirectResponse(url="/admin-home", status_code=302)

#transaction
@app.get("/transaction", response_class=HTMLResponse)
async def transaction(request: Request, user=Depends(manager)):
    if isinstance(user, models.UserAccount):
        accounts = {}
        UserAccounts = user.bankAccounts
        for a in UserAccounts:
            account = {}
            account["bankType"] = a.accountType
            account["balance"] = a.balance
            account["accountNumber"] = a.banknumber
            accounts[a.banknumber] = account
        return templates.TemplateResponse("transaction.html", {"request": request, "firstname": user.firstname, "accounts": accounts})
    return RedirectResponse(url="/admin-home", status_code=302)

def generate_otp(length=6):
    """Generate a random OTP of specified length."""
    otp = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))
    return otp

# @app.get("/withdraw/otp", response_class=HTMLResponse)
# async def withdrawOtp(request: Request, selectedAccount: str=Form(None),  , phone: str = Form(None), amount: str = Form(None), user=Depends(manager)):
#     if isinstance(user, models.UserAccount):
#         if phone != user.phone:
#             return f"<script> alert(\"Invalid phone number\"); window.history.back(); </script>"
#         if not amount:
#             return f"<script> alert(\"Please enter an amount\"); window.history.back(); </script>"
#         if float(amount) <= 0 or float(amount) > accountDict["balance"]:
#             return f"<script> alert(\"Invalid amount\"); window.history.back(); </script>"
#         otp = generate_otp()
#         return templates.TemplateResponse("withdrawalOtp.html", {"request": request, "firstname": user.firstname, "otp": otp})
#     return RedirectResponse(url="/admin-home", status_code=302)

# @app.get("/transfer/review", response_class=HTMLResponse)
# async def transferReview(request: Request, user=Depends(manager)):
#     if isinstance(user, UserAccount):
#         return templates.TemplateResponse("transferReview.html", {"request": request, "firstname": user.getFirstName()})
#     return RedirectResponse(url="/admin-home", status_code=302)

# #currency exchange         
# @app.get("/currency-exchange", response_class=HTMLResponse)
# async def currencyExchange(request: Request, user=Depends(manager)):
#     if isinstance(user, UserAccount):
#         return templates.TemplateResponse("currencyExchange.html", {"request": request, "firstname": user.getFirstName()})
#     return RedirectResponse(url="/admin-home", status_code=302)

# @app.get("/admin/currency-exchange", response_class=HTMLResponse)
# async def currencyExchangeAdmin(request: Request, user=Depends(manager)):
#     if isinstance(user, AdminAccount):
#         return templates.TemplateResponse("currencyExchangeAdmin.html", {"request": request, "firstname": user.getFirstName()})
#     return RedirectResponse(url="/home", status_code=302)

# @app.post("/get-currency-rate/{currencyID}")
# async def getCurrencyRate(request: Request, user=Depends(manager), currencyID: str = ""):
#     currencyRate = root.currency[currencyID].getCurrencyRate()
#     return {"buyRate": currencyRate[0], "sellRate": currencyRate[1]}

# @app.get("/fakeAtm", response_class=HTMLResponse)
# async def fakeAtm(request: Request):
#     return templates.TemplateResponse("fakeAtm.html", {"request": request})

# @app.get("/fakeAtm/confirmation", response_class=HTMLResponse)
# async def fakeAtmConfirmation(request: Request):
#     return templates.TemplateResponse("fakeAtmConfirmation.html", {"request": request})

# @app.get("/fakeAtm/success", response_class=HTMLResponse)
# async def fakeAtmSuccess(request: Request):
#     return templates.TemplateResponse("fakeAtmSuccesshtml", {"request": request})

@app.get("/admin/user-management", response_class=HTMLResponse)
async def userManagement(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("admin.html", {"request": request, "firstname": user.firstname})

@app.post("/searchAccount")
async def searchAccount(request: schema.SearchAccountRequest, db: Session = Depends(get_db)):
    customer = None
    account = None
    if request.searchCitizenID is not None:
        customer = crud.getUserFromCitizenId(db, request.searchCitizenID)
    
    if request.searchAccountNo is not None:
        account = crud.getBankAccount(db, request.searchAccountNo)
        customer = crud.getUserFromCitizenId(db, request.searchCitizenID)

    if customer is None:
        return {"status": "failed", "message": "User not found"}
    if account is None and customer is not None and request.searchAccountNo is not None:
        return {"status": "failed", "message": "Bank Account not found"}
    
    filename = "profile/" + customer.username + "/" + customer.profilePic
    if customer.middlename == "":
        fullname = customer.firstname + " " + customer.lastname
    else:
        fullname = customer.firstname + " " + customer.middlename + " " + customer.lastname
        
    username = customer.username
    email = customer.email
    phno = customer.phone
    citizenId = customer.citizenID
    marital = customer.maritalstatus.capitalize()
    if customer.education == "unknown":
        education = "Prefer not to answer"
    education = customer.education.capitalize()

    if account is not None:
        bankAccounttype = ""
        if account.accountType == "savings":
            bankAccounttype = "Savings Account"
        elif account.accountType == "checking":
            bankAccounttype = "Checking Account"
        elif account.accountType == "business":
            bankAccounttype = "Business Account"
        bankId = account.bankID
        banknumber = account.banknumber
        balance = account.balance
        return {"status": "success", "filename": filename, "fullname": fullname, "username": username, "email": email, "phno": phno, "citizenId": citizenId, "marital": marital, "education": education, "bankAccounttype": bankAccounttype, "bankId": bankId, "banknumber": banknumber, "balance": balance}
    return {"status": "success", "filename": filename, "fullname": fullname, "username": username, "email": email, "phno": phno, "citizenId": citizenId, "marital": marital, "education": education}
    
@app.put("/updateAccount")
async def updateAccount(request: schema.UpdateAccountRequest, db: Session = Depends(get_db)):
    if request.fullname is not None:
        names = request.fullname.split(" ")

        if len(names) == 1:
            return {"status": "failed", "message": "Invalid name"}
        elif len(names) == 2:
            firstname = names[0]
            lastname = names[1]
            middlename = ""
        else:
            firstname = names[0]
            middlename = names[1]
            lastname = names[2]

    data = schema.CustomerUpdate(
        firstname=firstname,
        middlename=middlename,
        lastname=lastname,
        maritalstatus=request.maritalstatus,
        education=request.education,
        email=request.email,
        phno=request.phno,
    )

    crud.updateCustomer(db, request.citizenId, data)
   
@app.delete("/deleteBankAccount")
def deleteBankAccount(request: Request, db: Session = Depends(get_db), banknumber: str = Form(None)):
    crud.deleteBankAccount(db, banknumber)
    
@app.get("/userInfo", response_class=HTMLResponse)
async def userInfo(request: Request, user=Depends(manager)):
    if isinstance(user, models.UserAccount):
        middlename = user.middlename
        if middlename == "":
            fullname = user.firstname + " " + user.lastname
        else:
            fullname = user.firstname + " " + user.middlename + " " + user.lastname
        accounts = {}
        UserAccounts = user.bankAccounts
        for a in UserAccounts:
            account = {}
            account["bankType"] = a.accountType
            account["balance"] = a.balance
            account["accountNumber"] = a.banknumber
            accounts[a.banknumber] = account
        
        return templates.TemplateResponse("userprofile.html", {
            "request": request, 
            "firstname": user.firstname, 
            "fullname": fullname, 
            "email": user.email, 
            "phone": user.phone, 
            "citizenId": user.citizenID, 
            "maritalstatus": user.maritalstatus, 
            "education": user.education, 
            "username": user.username,
            "accounts": accounts
        })
    return RedirectResponse(url="/admin-home", status_code=302)

@app.get("/signUp", response_class=HTMLResponse)
async def signUp(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/signUpSubmission")
async def signUpSubmission(request: schema.SignUpRequest, db: Session = Depends(get_db)):
    
    if request.password != request.confirmPassword:
        return JSONResponse(
            status_code=400,
            content={"detail": "Password does not match"}
        )
    
    # Decode Base64 data
    file_data = request.file
    try:
        file_data_bytes = base64.b64decode(file_data)
    except (TypeError, ValueError):
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid file data"}
        )
    filename = request.filename
    if filename and not allowed_file(filename):
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid file type"}
        )
    
    user_directory = f"static/profile/{request.username}"
    os.makedirs(user_directory, exist_ok=True)
    
    file_path = os.path.join(user_directory, filename)
    with open(file_path, "wb") as f:
        f.write(file_data_bytes)
            
    hashPassword = hash_password(request.password)

    user_exists = db.query(models.UserAccount).filter(
        (models.UserAccount.username == request.username) | 
        (models.UserAccount.citizenID == request.citizenId)
    ).first() is not None
    if user_exists:
        return JSONResponse(
            status_code=400,
            content={"detail": "User already exists"}
        )
    
    customerSchema = schema.CustomerCreate(
        filename=filename,
        firstname=request.firstName,
        middlename=request.middleName,
        lastname=request.lastName,
        username=request.username,
        maritalstatus=request.maritalstatus,
        education=request.education,
        citizenId=request.citizenId,
        email=request.email,
        phno=request.phno,
        password=hashPassword,
        accountType=request.accountType
    )

    
    new_user = crud.createCustomer(db, customerSchema)

    bankID = "BMT"
    banknumber = str(random.randint(1000000000000, 99999999999999))
    while db.query(models.BankAccount).filter_by(bankID=bankID, banknumber=banknumber).first():
        banknumber = str(random.randint(1000000000000, 99999999999999))

    bankSchema = schema.BankAccountCreate(
        accountId=new_user.id,
        accountType=request.accountType,
        bankID=bankID,
        banknumber=banknumber,
        balance=1000.0
    )

    crud.createBankAccount(db, bankSchema)
    return JSONResponse(
        status_code=201,
        content={"detail": "Account created successfully!"}
    )

@app.get("/addAdmin", response_class=HTMLResponse)
async def addAdmins(request: Request, user=Depends(manager)):
    if isinstance(user, models.AdminAccount) and user.id == 1:
        return templates.TemplateResponse("add_admin.html", {"request": request})
    if isinstance(user, models.AdminAccount):
        return RedirectResponse(url="/home_admin", status_code=302)
    return RedirectResponse(url="/home", status_code=302)
    
@app.post("/addAdmin", response_class=HTMLResponse)
async def addAdmin(request: Request, db: Session = Depends(get_db), firstName: str = Form(None), middleName: str = Form(None), lastName: str = Form(None), username: str = Form(None), email: str = Form(None), phno: str = Form(None), password: str = Form(None), confirmPassword: str = Form(None)):
    required_params = [firstName, lastName, username, email, phno, password, confirmPassword]
    if any(param is None for param in required_params):
        return f"<script> alert(\"Please fill out all fields\"); window.history.back(); </script>"   
    elif password != confirmPassword:
        return f"<script> alert(\"Password does not match\"); window.history.back(); </script>"
    else:        
        hashPassword = hash_password(password)
        
        
        user_exists = db.query(models.UserAccount).filter(models.UserAccount.username == username).first() is not None or db.query(models.AdminAccount).filter(models.AdminAccount.username == username).first() is not None
        if user_exists:
            return f"<script> alert(\"User already exists\"); window.history.back(); </script>"
            
        adminSchema = schema.AdminCreate(
            firstname = firstName,
            middlename = middleName,
            lastname = lastName,
            username = username,
            email = email,
            phno = phno,
            password = hashPassword
        )
        
        crud.createAdmin(db, adminSchema)
           
        return RedirectResponse(url="/login", status_code=302)

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

@app.get("/login", response_class=HTMLResponse)
async def logIn(request: Request, db: Session = Depends(get_db)):
    createModerator(db)
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
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
        if user.username == "admin" and user.id == 1:
            response = RedirectResponse(url="/addAdmin", status_code=302)
        else:
            response = RedirectResponse(url="/admin-home", status_code=302)
    else:
        response = RedirectResponse(url="/home", status_code=302) 
 
    manager.set_cookie(response, access_token)
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session", httponly=True, secure=True, samesite="lax")
    return response