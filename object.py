import persistent

class Account(persistent.Persistent):
    def __init__(self, firstname, middlename, lastname, username, password, email, phone):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
    
    def getFirstName(self):
        return self.firstname
    
    def getMiddleName(self):
        return self.middlename
    
    def getLastName(self):
        return self.lastname
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def getEmail(self):
        return self.email
    
    def getPhone(self):
        return self.phone

class AdminAccount(Account, persistent.Persistent):
    def __init__(self, firstname, middlename, lastname, username, password, adminID, email, phone):
        Account.__init__(self, firstname, middlename, lastname, username, password, email, phone)
        self.adminID = adminID
    
    def getAdminID(self):
        return self.adminID

class UserAccount(Account, persistent.Persistent):
    def __init__(self, profilePic, firstname, middlename, lastname, username, password, citizenID, maritalstatus, education, email, phone):
        Account.__init__(self, firstname, middlename, lastname, username, password, email, phone)
        self.profilePic = profilePic
        self.citizenID = citizenID
        self.maritalstatus = maritalstatus
        self.education = education
        
    def getProfilePicName(self):
        return self.profilePic
    
    def getCitizenID(self):
        return self.citizenID
    
    def getMaritalStatus(self):
        return self.maritalstatus
    
    def getEducation(self):
        return self.education

class BankAccount(persistent.Persistent):
    def __init__(self, account, bankType, bankID, banknumber, balance):
        self.account = account
        self.bankType = bankType
        self.bankID = bankID
        self.banknumber = banknumber
        self.balance = balance
        self.transactions = []
        self.currency = {}
        
class Transaction(persistent.Persistent):
    def __init__(self, transactionID, account, amount, fee, date, time, transferType):
        self.transactionID = transactionID
        self.account = account
        self.amount = amount
        self.fee = fee
        self.date = date
        self.time = time
        self.transferType = transferType

class Transfer(Transaction):
    def __init__(self, transactionID, account, receiver, amount, fee, date, time, transferType):
        super().__init__(transactionID, account, amount, fee, date, time, transferType)
        self.receiver = receiver

class Withdraw(Transaction):
    def __init__(self, transactionID, account, amount, fee, date, time, transferType, otp):
        super().__init__(transactionID, account, amount, fee, date, time, transferType)
        self.otp = otp
    
    def getOtp(self):
        return self.otp
    
    def setOtp(self, otp):
        self.otp = otp

class Currency(persistent.Persistent):
    def __init__(self, currencyID, currencyname, currencyrate):
        self.currencyID = currencyID
        self.currencyname = currencyname
        self.currencyrate = currencyrate
        
    def getCurrencyID(self):
        return self.currencyID
    
    def getCurrencyName(self):
        return self.currencyname
    
    def getCurrencyRate(self):  
        return self.currencyrate