from ledger_store import *
from audit_log import AuditLog

class TransferValidationError(Exception):
    pass
class TransferAlreadyProcessedError(Exception):
    pass

processed_transfers = {}  # Store successful transfers here
audit_log = AuditLog()   # Create one audit log

def validate_transfer(from_account, to_account, amount):
    if not from_account.strip():
        raise TransferValidationError("Source account cannot be empty")
    if not to_account.strip():
        raise TransferValidationError("Destination account cannot be empty")
    if from_account == to_account:
        raise TransferValidationError("Source and destination accounts must be different")
    if not isinstance(amount, int):
        raise TransferValidationError("Amount must be an integer")
    if amount <= 0:
        raise TransferValidationError("Amount must be greater than zero")

async def transfer_funds(
    from_account,
    to_account,
    amount,
    idempotency_key,
    store=None
):
    validate_transfer(from_account,to_account,amount)   # First validate the input
    if idempotency_key in processed_transfers:   # Check whether this request was already processed
        return processed_transfers[idempotency_key]
    for attempt in range(2):  # Try the transfer maximum two times
        debit_done = False
        try:
            from_data = store.get_account(from_account)  # Read both accounts
            to_data = store.get_account(to_account)
            from_version = from_data["version"]
            to_version = to_data["version"]
            store.debit(from_account,amount,from_version)   # Debit source account
            debit_done = True
            audit_log.record({
                "type": "debit",
                "account_id": from_account,  # Record debit in audit log
                "amount": amount,
                "idempotency_key": idempotency_key
            })   
            store.credit(to_account,amount,to_version)    # Credit destination account
            audit_log.record({
                "type": "credit",  # Record credit in audit log
                "account_id": to_account,
                "amount": amount,
                "idempotency_key": idempotency_key
            })
            final_from = store.get_account(from_account)  # Get final balances
            final_to = store.get_account(to_account)
            result = {
                "success": True,
                "fromBalance": final_from["balance"],
                "toBalance": final_to["balance"]
            }
            processed_transfers[idempotency_key] = result   # Save result for idempotency
            return result
        except VersionConflictError:
            if debit_done:
                current_source = store.get_account(from_account)   # If debit already happened, rollback first
                store.credit(from_account,amount,current_source["version"])
                audit_log.record({
                    "type": "credit",       # Record rollback
                    "account_id": from_account,
                    "amount": amount,
                    "idempotency_key": idempotency_key
                })
            if attempt == 0:   # Retry only once
                continue
            raise
        except Exception:
            if debit_done:   # If source was already debited, # put the money back.
                current_source = store.get_account(from_account) 
                store.credit(from_account,amount,current_source["version"])
                audit_log.record({
                    "type": "credit",
                    "account_id": from_account,
                    "amount": amount,
                    "idempotency_key": idempotency_key
                })
            raise