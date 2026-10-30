from collections import defaultdict
from typing import List, Dict, Tuple

class Ingredient:
    def __init__(self, name: str, calories: int, protein: float):
        self.name = name
        self.calories = calories
        self.protein = protein

class DietOptimizer:
    def __init__(self, ingredients: List[Ingredient]):
        self.ingredients = ingredients

    def generate_optimal_meal(self, max_calories: int) -> Tuple[Dict[str, int], float, int]:
        dp = [0.0] * (max_calories + 1)
        item_choice = [None] * (max_calories + 1)

        for c in range(max_calories + 1):
            for item in self.ingredients:
                if item.calories <= c:
                    if dp[c - item.calories] + item.protein > dp[c]:
                        dp[c] = dp[c - item.calories] + item.protein
                        item_choice[c] = item

        best_calories = dp.index(max(dp))
        max_protein = dp[best_calories]

        meal_plan = defaultdict(int)
        curr_cal = best_calories
        while curr_cal > 0 and item_choice[curr_cal] is not None:
            item = item_choice[curr_cal]
            meal_plan[item.name] += 1
            curr_cal -= item.calories

        return dict(meal_plan), max_protein, best_calories

if __name__ == "__main__":
    db = [
        Ingredient("Whey Protein (1 Scoop)", 103, 21.0),
        Ingredient("Oatmeal (50g)", 185, 6.5),
        Ingredient("Boiled Chicken Breast (100g)", 165, 31.0),
        Ingredient("Mozzarella Cheese (50g)", 150, 12.0),
        Ingredient("Whole Egg (1 Unit)", 75, 6.0),
        Ingredient("Unsweetened Soy Milk (400ml)", 135, 13.0)
    ]
    optimizer = DietOptimizer(db)
    target_calories = 600
    
    print("=== 🏋️ MacroForge Diet Optimizer ===")
    print(f"Constraint: Calorie limit set to {target_calories} kcal\n")
    plan, total_protein, total_calories = optimizer.generate_optimal_meal(target_calories)
    
    print("💡 Algorithm_s Optimal Meal Composition:")
    for name, count in plan.items():
        print(f"  - {name} x {count} serving(s)")
    print("-" * 30)
    print(f"Total Calories Consumed: {total_calories} kcal")
    print(f"Total Protein Yield: {total_protein:.1f} g")
