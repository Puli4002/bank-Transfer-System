class Bank:
    def __init__(self,account_number,balance):
        self.account_number=account_number
        self.balance=balance
class Savingsaccount(Bank):
    def __init__(self,account_number,balance,interest_rate):
        super().__init__(account_number,balance)
        self.interest_rate=interest_rate

    def display(self):
        print("Account Number:-",self.account_number)
        print("Bank Balance:-",self.balance)
        print("Rate of Interest:-",self.interest_rate)

s=Savingsaccount("22591201000053","2547","7%")
s.display()
