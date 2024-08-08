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
    
    def setFirstName(self, firstname):
        self.firstname = firstname
    
    def setMiddleName(self, middlename):
        self.middlename = middlename
    
    def setLastName(self, lastname):
        self.lastname = lastname
    
    def setEmail(self, email):
        self.email = email
    
    def setPhone(self, phone):
        self.phone = phone

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
        self.bankAccounts = []
        
    def getProfilePicName(self):
        return self.profilePic
    
    def getCitizenID(self):
        return self.citizenID
    
    def getMaritalStatus(self):
        return self.maritalstatus
    
    def getEducation(self):
        return self.education
    
    def getBankAccounts(self):
        return self.bankAccounts
    
    def getBankAccount(self, bankNumber):
        for bankAccount in self.bankAccounts:
            if bankAccount.getBankNumber() == bankNumber:
                return bankAccount
        return None
    
    def addBankAccount(self, bankAccount):
        self.bankAccounts.append(bankAccount)
    
    def setMaritalStatus(self, maritalstatus):
        self.maritalstatus = maritalstatus
    
    def setEducation(self, education):
        self.education = education
    
    def setProfilePicName(self, profilePic):
        self.profilePic = profilePic

class BankAccount(persistent.Persistent):
    def __init__(self, account, bankType, bankID, banknumber, balance, currency):
        self.account = account
        self.bankType = bankType
        self.bankID = bankID
        self.banknumber = banknumber
        self.balance = balance
        self.transactions = []
        self.currency = currency
        
    def getAccount(self):
        return self.account
    
    def getBankType(self):
        return self.bankType
    
    def getBankID(self):
        return self.bankID
    
    def getBankNumber(self):
        return self.banknumber
        
    def getBalance(self):
        return self.balance
    
    def getTransactions(self):
        return self.transactions
    
    def getCurrency(self):
        return self.currency
        
        
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
    

