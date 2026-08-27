import threading
import asyncio
import uuid
from ledger_store import AccountStore
from transfer_service import transfer_funds


def run_transfer(store, from_account, to_account, amount, results, index):
    try:
        result = asyncio.run(
            transfer_funds(
                from_account,
                to_account,
                amount,
                str(uuid.uuid4()),
                store
            )
        )
        results[index] = ("success", result)
    except Exception as error:
        results[index] = ("failed", str(error))

def main():
    store = AccountStore()
    store.create_account("A", 2200)
    store.create_account("B", 1000)
    total_before = (
        store.get_account("A")["balance"]
        + store.get_account("B")["balance"]
    )
    print("Total before:", total_before)
    threads = []
    results = [None] * 20
    for i in range(20): # Create 20 threads
        if i % 2 == 0:
            from_account = "A"
            to_account = "B"
        else:
            from_account = "B"
            to_account = "A"
        thread = threading.Thread(
            target=run_transfer,
            args=(
                store,
                from_account,
                to_account,
                10,
                results,
                i
            )
        )
        
        threads.append(thread)
    print("Starting threads...")
    for thread in threads:  # Start all threads
        thread.start()
    for thread in threads:  # Wait for all threads
        thread.join()
    print("\nResults:")
    for i, result in enumerate(results):
        print("Thread", i, ":", result)
    total_after = (
        store.get_account("A")["balance"]
        + store.get_account("B")["balance"]
    )
    print("\nTotal before:", total_before)
    print("Total after:", total_after)
    if total_before == total_after:
        print("PASSED - Total money is Safe")
    else:
        print("FAILED - Money is not transfer")


if __name__ == "__main__":
    main()