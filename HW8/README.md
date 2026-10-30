# Homework 3: Practical Algorithm Implementations

## Project Documentation and Algorithmic Analysis

This document provides a comprehensive overview of the two software engineering projects developed for Homework 3. Both projects demonstrate the practical application of advanced algorithmic concepts and data structures to solve complex, real-world computational problems.

---

## Project 1: FairShare Core (Minimum Cash Flow Algorithm)

### System Description

FairShare Core is an automated debt simplification engine designed to manage and resolve shared expenses among groups of people, such as roommates living in a shared rental property. In a typical shared living scenario, individuals frequently pay for communal items (utilities, groceries, maintenance), resulting in a complex web of interconnected debts.

Traditionally, settling these debts requires everyone to pay back the exact person they owe, leading to an excessive number of transactions, high transaction fees, and administrative overhead. FairShare Core solves this problem by calculating the net balance of every individual and computing a settlement path that requires the absolute minimum number of transactions to clear all debts.

### Core Features

- **Dynamic Expense Tracking:** Users can input expenses specifying the payer, the total amount, and the specific list of participants who need to split the cost. The system automatically updates internal ledgers.
- **Net Balance Calculation:** The system aggregates all shared expenses into a single net balance for each user. A positive balance indicates a net creditor (owed money), while a negative balance indicates a net debtor (owes money).
- **Transaction Optimization:** The system outputs a clean, linear list of instructions detailing exactly who needs to pay whom, and exactly how much, reducing the total transaction volume to at most (N - 1) transfers, where N is the number of participants.

### Algorithmic Implementation and Complexity

The core of this project utilizes a **Greedy Algorithm paired with a Priority Queue (Max-Heap)** to match the largest debtors with the largest creditors.

1.  **Data Structure Selection:** Python's built-in `heapq` module is used. Because `heapq` implements a Min-Heap by default, the algorithm inserts negative balance values to simulate a Max-Heap behavior.
2.  **Execution Flow:**
    - The algorithm separates users into a `creditors` heap and a `debtors` heap based on their net balances.
    - It iteratively pops the maximum creditor and the maximum debtor from their respective heaps.
    - The algorithm settles the smaller of the two absolute amounts between this pair.
    - If a balance is not completely resolved, the remaining balance is pushed back into the appropriate heap.
3.  **Time Complexity:**
    - Calculating net balances takes O(E \* P), where E is the number of expenses and P is the average number of participants per expense.
    - Building the initial heaps takes O(N log N), where N is the number of users.
    - The settlement loop processes at most N-1 transactions. Each heap pop and push operation takes O(log N). Thus, the settlement phase operates in O(N log N) time complexity.
    - Overall Time Complexity: O(E \* P + N log N), which is highly efficient for large datasets compared to naive O(N^2) approaches.

---

## Project 2: MacroForge (Diet Optimizer)

### System Description

MacroForge is an intelligent nutritional planning system designed to assist individuals in achieving specific fitness goals, such as lean bulking or strict cutting phases. Tracking macronutrients (proteins, carbohydrates, fats) while adhering to a strict caloric limit is mathematically challenging for humans to do manually.

MacroForge automates this process by applying computational optimization techniques to a user-defined database of ingredients. It calculates the exact combination of food servings required to maximize a target macronutrient (in this case, protein) without exceeding a specified hard limit on total daily or meal-specific calories.

### Core Features

- **Standardized Ingredient Database:** The system uses an object-oriented approach to define ingredients, encapsulating attributes such as name, caloric value per serving, and protein yield per serving.
- **Constraint-Based Optimization:** Users define a hard ceiling for available calories (e.g., 600 kcal remaining for a post-workout meal). The system guarantees the final meal plan will not exceed this limit.
- **Automated Meal Plan Generation:** The output is a highly readable list of exact servings for each ingredient, alongside the final calculated nutritional totals.

### Algorithmic Implementation and Complexity

This project solves a classic computer science problem known as the **Unbounded Knapsack Problem using Dynamic Programming (DP)**.

1.  **State Definition:**
    - An array `dp` of size (max_calories + 1) is initialized to 0.0.
    - `dp[c]` represents the maximum grams of protein that can be accumulated using exactly `c` calories.
2.  **State Transition Equation:**
    - For every calorie capacity `c` from 0 to the target limit, and for every available ingredient:
    - `dp[c] = max(dp[c], dp[c - item.calories] + item.protein)`
    - This ensures that the optimal sub-solution for a smaller calorie limit is reused to build the optimal solution for larger calorie limits.
3.  **Backtracking Mechanism:**
    - To provide actionable output (the actual recipe, not just the final protein number), an auxiliary array `item_choice` tracks the exact ingredient added at each caloric step.
    - Once the optimal calorie target is found, the algorithm backtracks through `item_choice` to tally the exact servings of each ingredient used to reach that state.
4.  **Time and Space Complexity:**
    - Time Complexity: O(W \* N), where W is the maximum calorie limit and N is the total number of available ingredients in the database. The nested loops ensure every ingredient is evaluated at every caloric step.
    - Space Complexity: O(W), requiring two arrays of size W to store the dynamic programming states and the backtracking references.
