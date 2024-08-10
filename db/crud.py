from sqlalchemy.orm import Session

from . import models, schema

def getUser(db: Session, username: str):
    user = db.query(models.UserAccount).filter(models.UserAccount.username == username).first()

    if not user:
        user = db.query(models.AdminAccount).filter(models.AdminAccount.username == username).first()
    
    return user

def getUserFromCitizenId(db: Session, citizenId: str):
    return db.query(models.UserAccount).filter(models.UserAccount.citizenID == citizenId).first()

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
        
def deleteBankAccount(db: Session, banknumber: str):
    account = db.query(models.BankAccount).filter(models.BankAccount.banknumber == banknumber).first()
    db.delete(account)
    db.commit()

def checkBankAccount(db: Session, banknumber: str):
    account = db.query(models.BankAccount).filter(models.BankAccount.banknumber == banknumber).first()
    ownBank = db.query(models.BankAccount).filter(models.BankAccount.accountId == account.accountId).all()
    
    if len(ownBank) > 1:
        return True
    else:
        return False

def getBankAccount(db: Session, banknumber: str):
    return db.query(models.BankAccount).filter(models.BankAccount.banknumber == banknumber).first()

def getBankAccountsOfUser(db: Session, accountId: str):
    bankAccounts = {}
    for account in db.query(models.BankAccount).filter(models.BankAccount.accountId == accountId).all():
        bankAccount = {}
        bankAccount["bankType"] = account.accountType
        bankAccount["balance"] = account.balance
        bankAccount["accountNumber"] = account.banknumber
        bankAccounts[account.banknumber] = bankAccount
    return bankAccounts

def createTransfer(db: Session, transfer: schema.TransferCreate):
    new_transfer = models.Transfer(
        bankAccount_id = transfer.banknumber,
        amount = transfer.amount,
        fee = transfer.fee,
        date = transfer.date,
        time = transfer.time,
        transferType = transfer.transferType,
        transferBankId = transfer.transferBankId,
        receiver = transfer.receiver
    )
    db.add(new_transfer)
    db.commit()
    db.refresh(new_transfer)
    return new_transfer

def getTransfer(db: Session, transfer_id: int):
    return db.query(models.Transfer).filter(models.Transfer.id == transfer_id).first()

def updateBalanceTransfer(db: Session, banknumber: str, amount: float, receiver: str, bankId: str):
    account = db.query(models.BankAccount).filter(models.BankAccount.banknumber == banknumber).first()
    account.balance -= amount
    receiverAccount = db.query(models.BankAccount).filter(models.BankAccount.banknumber == receiver and models.BankAccount.bankID == bankId).first()
    if receiverAccount == None:
        return False
    receiverAccount.balance += amount
    db.commit()
    db.refresh(account)
    return True

def deleteTransfer(db: Session, transfer_id: int):
    transfer = db.query(models.Transfer).filter(models.Transfer.id == transfer_id).first()
    db.delete(transfer)
    db.commit()
    
def updateBalanceTransaction(db: Session, banknumber: str, amount: float, action: str):
    account = db.query(models.BankAccount).filter(models.BankAccount.banknumber == banknumber).first()
    if action == "withdraw":
        account.balance -= amount
    elif action == "deposit":
        account.balance += amount
    db.commit()
    db.refresh(account)
    return True