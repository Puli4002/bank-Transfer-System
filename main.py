import asyncio
from ledger_store import AccountStore
from transfer_service import transfer_funds


async def main():
    store = AccountStore()
    store.create_account("A", 0)   # Create some accounts
    store.create_account("B", 1000)

    while True:

        print("\n===== BANK TRANSFER SYSTEM =====")
        print("1. View Accounts")
        print("2. Check account")
        print("3. Transfer money")
        print("4. Exit")

        choice = input("Enter your choice:")
        if choice == "1":
            print(f"Avaliable Accounts   : {list(store.accounts.keys())}")
        elif choice == "2":
            account_id = input("Enter account ID:").upper().strip()
            try:
                account = store.get_account(account_id)
                print("\nAccount Details")
                print("Account ID:", account["account_id"])
                print("Balance:", account["balance"])
                print("Version:", account["version"])
            except Exception as error:
                print("Error:", error)
        elif choice == "3":
            print("\n----- Money Transfer -----")
            from_account = input("Enter source account:").upper().strip()
            to_account = input("Enter destination account:").upper().strip()
            try:
                amount = int(input("Enter amount:"))
                idempotency_key = input("Enter idempotency_key:")
                result = await transfer_funds(
                    from_account=from_account,
                    to_account=to_account,
                    amount=amount,
                    idempotency_key=idempotency_key,
                    store=store
                )
                print("\nTransfer successful!")
                print("Source account balance:",
                      result["fromBalance"])
                print("Destination account balance:",
                      result["toBalance"])
            except ValueError:
                print("Please enter a valid number for amount.")
            except Exception as error:
                print("Transfer failed:", error)
        elif choice == "4":
            print("Thank you for using the Bank Transfer System.")
            break
        else:
            print("Invalid Option Choosen")

if __name__ == "__main__":
    asyncio.run(main())