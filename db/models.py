from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date, Time, case
from sqlalchemy.orm import relationship

from .database import Base

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(255), nullable=False)
    middlename = Column(String(255), nullable=True)
    lastname = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'accounts',
        'polymorphic_on': case(
            (type == "admin_account", "admin_account"),
            (type == "user_account", "user_account"),
            else_="employee"
        )
    }

class AdminAccount(Account):
    __tablename__ = 'admin_accounts'

    id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin_account',
    }

class UserAccount(Account):
    __tablename__ = 'user_accounts'

    id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)
    profilePic = Column(String(255), nullable=True)
    citizenID = Column(String(255), unique=True, nullable=False)
    maritalstatus = Column(String(255), nullable=True)
    education = Column(String(255), nullable=True)
    bankAccounts = relationship("BankAccount", back_populates="account")

    __mapper_args__ = {
        'polymorphic_identity': 'user_account',
    }

class BankAccount(Base):
    __tablename__ = 'bank_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    accountId = Column(Integer, ForeignKey('user_accounts.id'))
    accountType = Column(String(255), nullable=False)
    bankID = Column(String(255), nullable=False)
    banknumber = Column(String(255), unique=True, nullable=False)
    balance = Column(Float, nullable=False)
    transactions = relationship("Transaction", back_populates="bankAccount")

    account = relationship("UserAccount", back_populates="bankAccounts")

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transactionID = Column(String(255), unique=True, nullable=False)
    bankAccount_id = Column(Integer, ForeignKey('bank_accounts.id'))
    amount = Column(Float, nullable=False)
    fee = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    transferType = Column(String(255), nullable=False)

    bankAccount = relationship("BankAccount", back_populates="transactions")

    __mapper_args__ = {
        'polymorphic_identity': 'transaction',
        'polymorphic_on': transferType
    }

class Transfer(Transaction):
    __tablename__ = 'transfers'

    id = Column(Integer, ForeignKey('transactions.id'), primary_key=True)
    receiver = Column(String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'transfer',
    }

class Withdraw(Transaction):
    __tablename__ = 'withdraws'

    id = Column(Integer, ForeignKey('transactions.id'), primary_key=True)
    otp = Column(String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'withdraw',
    }

class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    currencyID = Column(String(255), unique=True, nullable=False)
    currencyname = Column(String(255), nullable=False)
    currencyrate = Column(Float, nullable=False)