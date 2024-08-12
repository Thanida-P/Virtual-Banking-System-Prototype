import base64
import random
from fastapi import APIRouter, Depends, Request
from app.api.dependencies import *
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from app.db import models, schema, crud
from sqlalchemy.orm import Session
import os

userAccount = APIRouter()

userAccount.mount("/static", StaticFiles(directory="app/static"), name="static")


@userAccount.get("/admin/user-management", response_class=HTMLResponse)
async def userManagement(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("admin.html", {"request": request, "firstname": user.firstname})

@userAccount.post("/searchAccount")
async def searchAccount(request: schema.SearchAccountRequest, db: Session = Depends(get_db)):
    customer = None
    account = None
    if request.searchCitizenID is not None:
        customer = crud.getUserFromCitizenId(db, request.searchCitizenID)
    
    if request.searchAccountNo is not None:
        account = crud.getBankAccount(db, request.searchAccountNo)
        citizenId = db.query(models.UserAccount).filter(models.UserAccount.id == account.accountId).first().citizenID
        customer = crud.getUserFromCitizenId(db,citizenId)

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
    
@userAccount.put("/updateAccount")
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
    
@userAccount.get("/addAccount", response_class=HTMLResponse)
async def addAccount(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("addAccount.html", {"request": request, "firstname": user.firstname})
   
@userAccount.post("/addAccount")
async def addAccount(request: schema.AddAccountRequest, db: Session = Depends(get_db), user=Depends(manager)):
    if request.citizenId == user.citizenID and verify_password(request.password, user.password):
        bankID = "BMT"
        banknumber = str(random.randint(1000000000000, 99999999999999))
        while db.query(models.BankAccount).filter_by(bankID=bankID, banknumber=banknumber).first():
            banknumber = str(random.randint(1000000000000, 99999999999999))

        bankSchema = schema.BankAccountCreate(
            accountId=user.id,
            accountType=request.accountType,
            bankID=bankID,
            banknumber=banknumber,
            balance=1000.0
        )
        crud.createBankAccount(db, bankSchema)
        return RedirectResponse(url="/home", status_code=302)
        
            
@userAccount.delete("/deleteBankAccount")
def deleteBankAccount(request: schema.DeleteBankAccountRequest, db: Session = Depends(get_db), user= Depends(manager)):
    if crud.checkBankAccount(db, request.banknumber) == False:
        return JSONResponse(
            status_code=400,
            content={"detail": "Cannot delete bank account. Contact the bank!"}
        )
    else:
        crud.deleteBankAccount(db, request.banknumber)
        return JSONResponse(
            status_code=200,
            content={"detail": "Bank Account deleted"}
        )
    
@userAccount.get("/userInfo", response_class=HTMLResponse)
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

        pic_url = user.username + "/" + user.profilePic
        
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
            "accounts": accounts,
            "filename": pic_url
        })
    return RedirectResponse(url="/admin-home", status_code=302)

@userAccount.get("/signUp", response_class=HTMLResponse)
async def signUp(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@userAccount.post("/signUpSubmission")
async def signUpSubmission(request: schema.SignUpRequest, db: Session = Depends(get_db)):
    
    if request.password != request.confirmPassword:
        return JSONResponse(
            status_code=400,
            content={"detail": "Password does not match"}
        )
    
    user_exists = db.query(models.UserAccount).filter(
        (models.UserAccount.username == request.username) | 
        (models.UserAccount.citizenID == request.citizenId)
    ).first() is not None
    if user_exists:
        return JSONResponse(
            status_code=400,
            content={"detail": "User already exists"}
        )
    
    # Decode Base64 data
    file_data = request.file
    try:
        if file_data.startswith('data:image/jpeg;base64,'):
            file_data = file_data.replace('data:image/jpeg;base64,', '')
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
    
    user_directory = f"app/static/profile/{request.username}"
    os.makedirs(user_directory, exist_ok=True)
    
    file_path = os.path.join(user_directory, filename)
    with open(file_path, "wb") as f:
        f.write(file_data_bytes)
            
    hashPassword = hash_password(request.password)

    
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

@userAccount.get("/addAdmin", response_class=HTMLResponse)
async def addAdmins(request: Request, user=Depends(manager)):
    if isinstance(user, models.AdminAccount) and user.username == "admin" and verify_password("BankMatrixAdmin", user.password) == True:
        return templates.TemplateResponse("add_admin.html", {"request": request})
    if isinstance(user, models.AdminAccount):
        return RedirectResponse(url="/admin-home", status_code=302)
    return RedirectResponse(url="/home", status_code=302)
    
@userAccount.post("/addAdmin", response_class=HTMLResponse)
async def addAdmin(request: schema.AddAdminRequest, db: Session = Depends(get_db)):
    firstName = request.firstName
    middleName = request.middleName
    lastName = request.lastName
    username = request.username
    email = request.email
    phno = request.phno
    password = request.password
    confirmPassword = request.confirmPassword
    
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