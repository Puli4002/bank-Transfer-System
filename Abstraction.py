from abc import ABC , abstractmethod
class Bank(ABC):
    @abstractmethod
    def interest_rate(self):
        pass

class Sbi(Bank):
    def interest_rate(self):
        print("the interest will based on SBI rules")

class Hdfc(Bank):
    def interest_rate(self):
        print("The interest rate will based on HDFC")
class Rbl(Bank):
    def interest_rate(self):
        print("The interest rate will based on Rbl")

s=Sbi()
h=Hdfc()
r=Rbl()
s.interest_rate()
h.interest_rate()
r.interest_rate()
