from sqlalchemy.orm import Session

from . import models, schema

def getUser(db: Session, username: str):
    user = db.query(models.UserAccount).filter(models.UserAccount.username == username).first()

    if not user:
        user = db.query(models.AdminAccount).filter(models.AdminAccount.username == username).first()
    
    return user

def createCustomer(db: Session, customer: schema.CustomerCreate):
    new_user = models.UserAccount(
        profilePic=customer.filename,
        firstname=customer.firstname,
        middlename=customer.middlename,
        lastname=customer.lastname,
        username=customer.username,
        password=customer.password,
        citizenID=customer.citizenId,
        maritalstatus=customer.maritalstatus,
        education=customer.education,
        email=customer.email,
        phone=customer.phno
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def createBankAccount(db: Session, account: schema.BankAccountCreate):
    new_account = models.BankAccount(
        accountId = account.accountId,
        accountType = account.accountType,
        bankID = account.bankID,
        banknumber = account.banknumber,
        balance = account.balance
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

def createAdmin(db: Session, admin: schema.AdminCreate):
    new_admin = models.AdminAccount(
        firstname = admin.firstname,
        middlename = admin.middlename,
        lastname = admin.lastname,
        username = admin.username,
        password = admin.password,
        email = admin.email,
        phone = admin.phno,
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

def updateCustomer(db: Session, citizenId: str, updatingData: schema.CustomerUpdate):
    customer = db.query(models.UserAccount).filter(models.UserAccount.citizenID == citizenId).first()
    
    if customer:
        customer.firstname = updatingData.firstname
        customer.middlename = updatingData.middlename
        customer.lastname = updatingData.lastname
        customer.email = updatingData.email
        customer.phone = updatingData.phno
        customer.maritalstatus = updatingData.maritalstatus
        customer.education = updatingData.education
        
        db.commit()
        
def getBankAccountsOfUser(db: Session, accountId: str):
    bankAccounts = {}
    for account in db.query(models.BankAccount).filter(models.BankAccount.accountId == accountId).all():
        bankAccount = {}
        bankAccounts["bankType"] = account.accountType
        bankAccounts["balance"] = account.balance
        bankAccounts["accountNumber"] = account.banknumber
        bankAccounts[account.banknumber] = bankAccount
    return bankAccounts
        
