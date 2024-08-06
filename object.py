import persistent

class Account(persistent.Persistent):
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance