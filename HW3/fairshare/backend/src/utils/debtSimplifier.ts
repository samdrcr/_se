export interface DebtRecord {
  debtor: string;
  creditor: string;
  amount: number;
}

export function simplifyDebts(balances: Record<string, number>): DebtRecord[] {
  const debtors: { id: string; amount: number }[] = [];
  const creditors: { id: string; amount: number }[] = [];

  for (const [id, balance] of Object.entries(balances)) {
    if (balance < -0.01) debtors.push({ id, amount: -balance });
    else if (balance > 0.01) creditors.push({ id, amount: balance });
  }

  debtors.sort((a, b) => b.amount - a.amount);
  creditors.sort((a, b) => b.amount - a.amount);

  const transactions: DebtRecord[] = [];
  let i = 0, j = 0;

  while (i < debtors.length && j < creditors.length) {
    const settle = Math.min(debtors[i].amount, creditors[j].amount);
    transactions.push({
      debtor: debtors[i].id,
      creditor: creditors[j].id,
      amount: Math.round(settle),
    });

    debtors[i].amount -= settle;
    creditors[j].amount -= settle;

    if (debtors[i].amount < 0.01) i++;
    if (creditors[j].amount < 0.01) j++;
  }
  return transactions;
}
