import time 
class AccountNotFoundError(Exception):
    pass
class InsufficientFundsError(Exception):
    pass
class VersionConflictError(Exception):
    pass

class AccountStore:
    def __init__(self):
        self.accounts = {}
    def create_account(self, account_id, starting_balance):
        self.accounts[account_id] = {
            "account_id": account_id,
            "balance": starting_balance,
            "version": 0
        }
    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError("Account not found")
        return self.accounts[account_id].copy()
    def debit(self, account_id, amount, expected_version):
        if account_id not in self.accounts:
            raise AccountNotFoundError("Account not found")
        account = self.accounts[account_id]  
        if account["version"] != expected_version:  # Check whether another update happened
            raise VersionConflictError("Account version has changed")  
        if account["balance"] < amount:    # Check whether account has enough money
            raise InsufficientFundsError("Not enough balance") 
        time.sleep(0.001) 
        account["balance"] -= amount    # Remove money
        account["version"] += 1   # Increase version after successful update
        return account["version"]
    def credit(self, account_id, amount, expected_version):
        if account_id not in self.accounts:
            raise AccountNotFoundError("Account not found")
        account = self.accounts[account_id]   
        if account["version"] != expected_version:  # Check version
            raise VersionConflictError("Account version has changed") 
        account["balance"] += amount  # Add money
        account["version"] += 1  # Increase version
        return account["version"]

    