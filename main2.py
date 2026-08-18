"""
transfer_service.py

This is the "brain" of the send-money feature. It sits on top of
AccountStore and AuditLog and is responsible for making sure a
transfer is safe, even when things go wrong halfway through.

Three problems this file solves:

1. ATOMICITY
   A transfer is really two separate writes (debit A, credit B).
   If the debit works but the credit fails, we can't just leave A
   short of money with nothing to show for it - so we credit A back
   (a "compensating transaction" / rollback) before giving up.

2. IDEMPOTENCY
   If the same request comes in twice with the same idempotency_key
   (for example because a client's network call timed out and it
   retried), we must not move the money twice. We remember results
   by idempotency_key and just replay the old result the second time.

3. CONCURRENCY
   Someone else might change an account between the moment we read
   it and the moment we write to it. When that happens, the store
   raises VersionConflictError. We retry the WHOLE transfer exactly
   once, re-reading fresh account versions before trying again.
"""

import weakref

from ledger_store import (
    AccountNotFoundError,
    InsufficientFundsError,
    VersionConflictError,
)
from audit_log import AuditLog


class TransferValidationError(Exception):
    """Raised when the input to a transfer doesn't make sense."""
    pass


class TransferAlreadyProcessedError(Exception):
    """
    Not really a failure - this exists to describe the idempotent-replay
    situation, in case any caller wants to check for it explicitly.
    transfer_funds itself does not raise this; it just quietly returns
    the original result.
    """
    pass


# ---------------------------------------------------------------------------
# Per-store state (processed idempotency keys + audit log)
# ---------------------------------------------------------------------------
#
# We keep one AuditLog and one "already processed" dictionary PER
# AccountStore, instead of using plain global variables. Otherwise, if
# your program (or your tests) ever create two separate AccountStore
# objects, they'd end up sharing the same idempotency cache and audit
# log by accident, which would be wrong.
#
# We use a WeakKeyDictionary so that if an AccountStore is thrown away,
# its leftover state gets cleaned up automatically instead of leaking
# memory forever.

_state_by_store = weakref.WeakKeyDictionary()


def _get_state(store):
    if store is None:
        raise ValueError("transfer_funds needs a store to work with")

    if store not in _state_by_store:
        _state_by_store[store] = {
            "processed_transfers": {},
            "audit_log": AuditLog(),
        }

    return _state_by_store[store]


def get_audit_log(store):
    """Look up the AuditLog that belongs to a particular store. Useful for
    tests and for reconciliation jobs that want to check the log."""
    return _get_state(store)["audit_log"]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_transfer(from_account, to_account, amount):
    if from_account is None or not from_account.strip():
        raise TransferValidationError("Source account cannot be blank")

    if to_account is None or not to_account.strip():
        raise TransferValidationError("Destination account cannot be blank")

    if from_account == to_account:
        raise TransferValidationError("Source and destination accounts must be different")

    # bool is technically a subclass of int in Python, so we explicitly
    # reject True/False here even though isinstance(True, int) is True.
    if not isinstance(amount, int) or isinstance(amount, bool):
        raise TransferValidationError("Amount must be a whole number")

    if amount <= 0:
        raise TransferValidationError("Amount must be greater than zero")


# ---------------------------------------------------------------------------
# The main entry point
# ---------------------------------------------------------------------------

async def transfer_funds(from_account, to_account, amount, idempotency_key, store=None):
    # Step 1: validate BEFORE touching the store at all - even on a
    # replayed idempotent call, we still re-validate first.
    validate_transfer(from_account, to_account, amount)

    state = _get_state(store)
    processed_transfers = state["processed_transfers"]
    audit_log = state["audit_log"]

    # Step 2: idempotency check. If we've already done this exact
    # request before, just hand back the same answer - don't touch
    # the accounts again.
    if idempotency_key in processed_transfers:
        return processed_transfers[idempotency_key]

    last_conflict_error = None
    max_attempts = 2  # one normal try, plus exactly one retry

    for attempt_number in range(max_attempts):
        try:
            result = _attempt_transfer_once(
                from_account, to_account, amount, idempotency_key, store, audit_log
            )
            # Success! Remember this result so a duplicate request with
            # the same idempotency_key gets the same answer later.
            processed_transfers[idempotency_key] = result
            return result

        except VersionConflictError as error:
            # Someone else touched one of the accounts while we were
            # working. Save the error in case we run out of attempts,
            # and loop around to try again with freshly-read versions.
            last_conflict_error = error
            continue

    # If we get here, we used up all our attempts and still hit a
    # version conflict every time. Let it propagate - the caller
    # (or the user) needs to know and can decide to try again later.
    raise last_conflict_error


def _attempt_transfer_once(from_account, to_account, amount, idempotency_key, store, audit_log):
    """
    Does exactly ONE attempt at moving the money: read fresh versions,
    debit the source, credit the destination, and roll back the debit
    if the credit fails for any reason. Raises on failure.
    """

    # Step 3: read both accounts fresh, so we have their current versions.
    from_account_data = store.get_account(from_account)
    to_account_data = store.get_account(to_account)

    # Step 4: debit the source account.
    store.debit(from_account, amount, from_account_data["version"])
    audit_log.record({
        "type": "debit",
        "account_id": from_account,
        "amount": amount,
        "idempotency_key": idempotency_key,
    })

    # Step 5: credit the destination account.
    try:
        store.credit(to_account, amount, to_account_data["version"])
    except Exception as credit_error:
        # The debit already happened but the credit didn't - we must
        # NOT leave the ledger in this half-done state. Put the money
        # back on the source account before letting the error escape.
        _rollback_debit(store, audit_log, from_account, amount, idempotency_key)
        raise credit_error

    audit_log.record({
        "type": "credit",
        "account_id": to_account,
        "amount": amount,
        "idempotency_key": idempotency_key,
    })

    final_from = store.get_account(from_account)
    final_to = store.get_account(to_account)

    return {
        "success": True,
        "fromBalance": final_from["balance"],
        "toBalance": final_to["balance"],
    }


def _rollback_debit(store, audit_log, account_id, amount, idempotency_key):
    """
    Credits `account_id` back the amount that was just debited from it,
    because the other half of the transfer failed. We retry this once
    too, in case the account changed again in the meantime - we really
    do not want a rollback to silently fail and leave money missing.
    """
    for attempt_number in range(2):
        try:
            current_account = store.get_account(account_id)
            store.credit(account_id, amount, current_account["version"])
            audit_log.record({
                "type": "credit",
                "account_id": account_id,
                "amount": amount,
                "idempotency_key": idempotency_key,
                "note": "rollback of a failed transfer",
            })
            return
        except VersionConflictError:
            continue

    # If we still couldn't roll back after retrying, this is a serious
    # problem - money is stuck debited with no matching credit. We
    # raise loudly instead of pretending everything is fine.
    raise RuntimeError(
        f"CRITICAL: could not roll back debit on account '{account_id}'. "
        f"Manual reconciliation required."
    )


# ---------------------------------------------------------------------------
# Stretch goal: a chain of transfers that succeeds or fails as one unit
# ---------------------------------------------------------------------------

async def transfer_chain(transfers, store=None):
    """
    transfers: a list of (from_account, to_account, amount) tuples.

    Runs each transfer in order. If any transfer in the chain fails
    AFTER earlier ones already succeeded, we reverse all the earlier
    ones (in reverse order) before letting the error propagate, so the
    whole chain behaves as one all-or-nothing unit.
    """
    completed = []  # list of (from_account, to_account, amount) that succeeded

    for from_account, to_account, amount in transfers:
        # Each individual transfer still needs its own unique idempotency
        # key so it isn't confused with any other transfer.
        step_key = f"chain-{id(transfers)}-{len(completed)}"
        try:
            await transfer_funds(from_account, to_account, amount, step_key, store=store)
            completed.append((from_account, to_account, amount))
        except Exception as error:
            # Undo everything that already succeeded, most recent first,
            # by sending the money back the other way.
            for undone_from, undone_to, undone_amount in reversed(completed):
                undo_key = f"chain-undo-{id(transfers)}-{undone_from}-{undone_to}-{undone_amount}-{len(completed)}"
                await transfer_funds(undone_to, undone_from, undone_amount, undo_key, store=store)
            raise error

    return {"success": True, "steps_completed": len(completed)}