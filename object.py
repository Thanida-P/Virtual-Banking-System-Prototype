import persistent

class Account(persistent.Persistent):
    def __init__(self, profilePic, firstname, middlename, lastname, username, password):
        self.profilePic = profilePic
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.username = username
        self.password = password

class AdminAccount(Account, persistent.Persistent):
    def __init__(self, profilePic, firstname, middlename, lastname, username, password, adminID):
        Account.__init__(self, profilePic, firstname, middlename, lastname, username, password)
        self.adminID = adminID

class UserAccount(Account, persistent.Persistent):
    def __init__(self, profilePic, firstname, middlename, lastname, username, password, maritalstatus, education):
        Account.__init__(self, profilePic, firstname, middlename, lastname, username, password)
        self.maritalstatus = maritalstatus
        self.education = education

class BankAccount(persistent.Persistent):
    def __init__(self, firstname, middlename, lastname, bankID, banknumber, balance):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.bankID = bankID
        self.banknumber = banknumber
        self.balance = balance
        self.transactions = []
        self.currency = {}
        
class Transaction(persistent.Persistent):
    def __init__(self, transactionID, account, amount, date, time, transferType):
        self.transactionID = transactionID
        self.account = account
        self.amount = amount
        self.date = date
        self.time = time
        self.transferType = transferType

class Transfer(Transaction):
    def __init__(self, transactionID, account, receiver, amount, date, time):
        super().__init__(transactionID, account, amount, date, time)
        self.receiver = receiver

class Withdraw(Transaction):
    def __init__(self, transactionID, account, amount, date, time):
        super().__init__(transactionID, account, amount, date, time)

class Currency(persistent.Persistent):
    def __init__(self, currencyID, currencyname, currencyrate):
        self.currencyID = currencyID
        self.currencyname = currencyname
        self.currencyrate = currencyrate