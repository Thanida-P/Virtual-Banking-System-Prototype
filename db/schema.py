from pydantic import BaseModel, EmailStr
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