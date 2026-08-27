import asyncio
from ledger_store import AccountStore
from transfer_service import transfer_funds
import uuid

class BrokenCreditStore(AccountStore):
     def __init__ (self):
          super().__init__()
          self.has_return_money=False
     """A version of the store where credit() always fails, so we can
     prove the debit gets rolled back correctly."""
     def credit(self, account_id, amount, expected_version):
         if not self.has_return_money:
              self.has_return_money=True
              raise RuntimeError("simulated failure — credit step is broken onpurpose")
         return super().credit(account_id, amount, expected_version)


def main():
     store = BrokenCreditStore()
     store.create_account("A", starting_balance=1000)
     store.create_account("B", starting_balance=1000)

     total_before = store.get_account("A")["balance"]
     print(f"Account A balance before attempted transfer:{total_before}")

     try:
         asyncio.run(
             transfer_funds(
                 from_account="A",
                 to_account="B",
                 amount=100,
                 idempotency_key=str(uuid.uuid4()),
                 store=store,
             )
         )
         print("Transfer reported success — but credit was supposed tofail!")
     except Exception as exc:
         print(f"Transfer failed as expected: {exc}")

     total_after = store.get_account("A")["balance"]
     print(f"Account A balance after failed transfer: {total_after}")

     assert total_before == total_after, (f"ATOMICITY BROKEN — A went from {total_before} to{total_after}, ""money was lost even though the transfer failed.")
     print("PASSED — A's balance was correctly restored after the failed credit.")


if __name__ == "__main__":
     main()
