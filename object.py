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
    def __init__(self, profilePic, firstname, middlename, lastname, username, password, citizenID, maritalstatus, education):
        Account.__init__(self, profilePic, firstname, middlename, lastname, username, password)
        self.citizenID = citizenID
        self.maritalstatus = maritalstatus
        self.education = education

class BankAccount(persistent.Persistent):
    def __init__(self, account, bankID, banknumber, balance):
        self.account = account
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
    def __init__(self, transactionID, account, amount, fee, date, time, transferType):
        super().__init__(transactionID, account, amount, fee, date, time, transferType)

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
    
# For Admin Currency Exchange

class CurrencyExchangeRate(persistent.Persistent):
    def __init__(self,from_currency, to_currency, sell_rate, buy_rate):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.sell_rate = sell_rate
        self.buy_rate = buy_rate

    def getFromCurrency(self):
        return self.from_currency
    
    def getToCurrency(self):
        return self.to_currency
    
    def getSellRate(self):
        return self.sell_rate
    
    def getBuyRate(self):
        return self.buy_rate
    

