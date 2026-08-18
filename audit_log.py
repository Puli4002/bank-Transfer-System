class AuditLog:
    def __init__(self):
        self.events = []
    def record(self, event):
        self.events.append(event.copy())  # Add the event to the log    
    def balance_for(self, account_id, starting_balance):
        balance = starting_balance
        for event in self.events:
            if event["account_id"] != account_id:
                continue
            if event["type"] == "debit":
                balance -= event["amount"]
            elif event["type"] == "credit":
                balance += event["amount"]
        return balance




        