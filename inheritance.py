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
s1=Savingsaccount("2259120155436","2727","8%")
s2=Savingsaccount("22591201000055","2047","2%")
s.display()
s1.display()
s2.display()
