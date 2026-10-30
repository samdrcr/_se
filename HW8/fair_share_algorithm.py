import heapq
from collections import defaultdict
from typing import List, Tuple, Dict

class FairShareCore:
    def __init__(self):
        self.balances = defaultdict(float)

    def add_expense(self, payer: str, amount: float, participants: List[str]):
        if not participants or amount <= 0:
            return
        split_amount = amount / len(participants)
        self.balances[payer] += amount
        for person in participants:
            self.balances[person] -= split_amount

    def optimize_transactions(self) -> List[Tuple[str, str, float]]:
        creditors = []
        debtors = []
        for person, balance in self.balances.items():
            if balance > 0.01:
                heapq.heappush(creditors, (-balance, person))
            elif balance < -0.01:
                heapq.heappush(debtors, (balance, person)) 

        transactions = []
        while creditors and debtors:
            max_credit_val, creditor = heapq.heappop(creditors)
            max_debt_val, debtor = heapq.heappop(debtors)
            max_credit = -max_credit_val
            max_debt = -max_debt_val
            settled_amount = min(max_credit, max_debt)
            transactions.append((debtor, creditor, round(settled_amount, 2)))
            if max_credit > max_debt:
                heapq.heappush(creditors, (-(max_credit - settled_amount), creditor))
            elif max_debt > max_credit:
                heapq.heappush(debtors, (-(max_debt - settled_amount), debtor))
        return transactions

if __name__ == "__main__":
    ledger = FairShareCore()
    ledger.add_expense("Sam", 1500, ["Sam", "Alice", "Bob", "Charlie", "David"])
    ledger.add_expense("Bob", 850, ["Sam", "Bob", "Charlie", "David"])
    ledger.add_expense("Alice", 400, ["Alice", "Bob", "David"])

    print("=== FairShare Algorithm ===")
    print("📊 Net Balances Before Optimization:")
    for person, balance in sorted(ledger.balances.items(), key=lambda x: x[1], reverse=True):
        if abs(balance) > 0.01:
            print(f"  {person}: {balance:+.2f} TWD")
            
    print("\n💡 Optimized Settlement Plan (Minimum Transactions):")
    for debtor, creditor, amount in ledger.optimize_transactions():
        print(f"  💸 {debtor} needs to pay {creditor} : {amount} TWD")
