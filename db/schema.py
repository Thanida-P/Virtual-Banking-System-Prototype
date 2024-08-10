from pydantic import BaseModel, EmailStr
from datetime import date, time
from typing import Optional

class CustomerCreate(BaseModel):
    filename:str
    firstname: str
    middlename: Optional[str]
    lastname: str
    username: str
    maritalstatus: str
    education: str
    citizenId: str
    email: EmailStr
    phno: str
    password: str
    accountType: str
    
class BankAccountCreate(BaseModel):
    accountId: int
    accountType: str
    bankID: str
    banknumber: str
    balance: float
    
class AdminCreate(BaseModel):
    firstname: str
    middlename: Optional[str]
    lastname: str
    username: str
    password: str
    email: str
    phno: str

class CustomerUpdate(BaseModel):
    firstname: str
    middlename: Optional[str]
    lastname: str
    maritalstatus: str
    education: str
    email: str
    phno: str
    
class SignUpRequest(BaseModel):
    firstName: str
    middleName: Optional[str] = None
    lastName: str
    username: str
    email: EmailStr
    phno: str
    password: str
    confirmPassword: str
    citizenId: str
    accountType: str
    maritalstatus: str
    education: str
    file: str
    termCheck: str
    filename: str
    
class AddAdminRequest(BaseModel):
    firstName: str
    middleName: Optional[str] = None
    lastName: str
    username: str
    email: EmailStr
    phno: str
    password: str
    confirmPassword: str
    
class SearchAccountRequest(BaseModel):
    searchCitizenID: str = None
    searchAccountNo: str = None
    
class UpdateAccountRequest(BaseModel):
    fullname: str = None
    email:str = None
    phno:str = None
    citizenId: str = None
    maritalstatus: str = None
    education: str = None
    
class AddAccountRequest(BaseModel):
    accountType: str
    citizenId: str
    password: str
    
class TransactionRequest(BaseModel):
    action: str
    phno: str
    amount: float
    banknumber: str
    otp: str
    
class TransferReviewRequest(BaseModel):
    banknumber: str
    banknumberReceiver: str
    transferBankId: str
    amount: float

class TransferCreate(BaseModel):
    banknumber: str
    transferBankId: str
    amount: float
    fee: float
    date: date
    time: time
    transferType: str
    receiver: str

class TransferRequest(BaseModel):
    transactionId: int
    
class DeleteBankAccountRequest(BaseModel):
    banknumber: str