from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class FoodItem:
    name: str
    cost: int
    calories: int


class FoodOptimizer:
    def __init__(self, items: Dict[str, Dict[str, int]]) -> None:
        """Load food items from a nested dictionary."""
        self.items = [
            FoodItem(name=name, cost=details["cost"], calories=details["calories"])
            for name, details in items.items()
        ]

    def greedy_algorithm(self, budget: int) -> Tuple[List[str], int, int]:
        """Select items by highest calories-per-cost without exceeding budget."""
        sorted_items = sorted(
            self.items,
            key=lambda item: item.calories / item.cost,
            reverse=True,
        )
        selected_names: List[str] = []
        total_cost = 0
        total_calories = 0
        for item in sorted_items:
            if total_cost + item.cost <= budget:
                selected_names.append(item.name)
                total_cost += item.cost
                total_calories += item.calories
        return selected_names, total_cost, total_calories

    def dynamic_programming(self, budget: int) -> Tuple[List[str], int, int]:
        """Compute the optimal set of items for maximum calories under budget."""
        item_count = len(self.items)
        dp_table = [[0 for _ in range(budget + 1)] for _ in range(item_count + 1)]

        for row_index in range(1, item_count + 1):
            current_item = self.items[row_index - 1]
            for cost_limit in range(budget + 1):
                if current_item.cost <= cost_limit:
                    dp_table[row_index][cost_limit] = max(
                        dp_table[row_index - 1][cost_limit],
                        dp_table[row_index - 1][cost_limit - current_item.cost] + current_item.calories,
                    )
                else:
                    dp_table[row_index][cost_limit] = dp_table[row_index - 1][cost_limit]

        selected_names: List[str] = []
        remaining_budget = budget
        for row_index in range(item_count, 0, -1):
            if dp_table[row_index][remaining_budget] != dp_table[row_index - 1][remaining_budget]:
                item = self.items[row_index - 1]
                selected_names.append(item.name)
                remaining_budget -= item.cost

        selected_names.reverse()
        total_cost = sum(item.cost for item in self.items if item.name in selected_names)
        total_calories = dp_table[item_count][budget]
        return selected_names, total_cost, total_calories


class FoodDemo:
    def __init__(self) -> None:
        """Prepare the demo dataset for the optimizer."""
        self.items = {
            "pizza": {"cost": 50, "calories": 300},
            "hamburger": {"cost": 40, "calories": 250},
            "hot-dog": {"cost": 30, "calories": 200},
            "pepsi": {"cost": 10, "calories": 100},
            "cola": {"cost": 15, "calories": 220},
            "potato": {"cost": 25, "calories": 350},
        }

    def run(self, budget: int = 90) -> None:
        """Run greedy and dynamic programming solutions and print results."""
        optimizer = FoodOptimizer(self.items)
        greedy_result = optimizer.greedy_algorithm(budget)
        dynamic_result = optimizer.dynamic_programming(budget)
        print("Greedy:", greedy_result)
        print("Dynamic programming:", dynamic_result)


if __name__ == "__main__":
    demo = FoodDemo()
    demo.run()
