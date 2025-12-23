import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt


@dataclass
class SimulationResult:
    probabilities: Dict[int, float]
    counts: Dict[int, int]


class DiceSimulation:
    def __init__(self, rolls_count: int) -> None:
        """Store simulation parameters for dice rolls."""
        self.rolls_count = rolls_count

    def simulate(self) -> SimulationResult:
        """Run Monte Carlo simulation and return counts and probabilities."""
        counts: Dict[int, int] = {total: 0 for total in range(2, 13)}
        for roll_index in range(self.rolls_count):
            first_die = random.randint(1, 6)
            second_die = random.randint(1, 6)
            total = first_die + second_die
            counts[total] += 1
        probabilities = {total: count / self.rolls_count for total, count in counts.items()}
        return SimulationResult(probabilities=probabilities, counts=counts)

    def analytical_probabilities(self) -> Dict[int, float]:
        """Return analytical probabilities for sums of two fair dice."""
        totals = {
            2: 1,
            3: 2,
            4: 3,
            5: 4,
            6: 5,
            7: 6,
            8: 5,
            9: 4,
            10: 3,
            11: 2,
            12: 1,
        }
        return {total: count / 36 for total, count in totals.items()}

    def compare(self, simulation: SimulationResult) -> List[Tuple[int, float, float, float]]:
        """Compare simulated and analytical probabilities."""
        analytical = self.analytical_probabilities()
        comparison: List[Tuple[int, float, float, float]] = []
        for total in range(2, 13):
            simulated_value = simulation.probabilities[total]
            analytical_value = analytical[total]
            difference = simulated_value - analytical_value
            comparison.append((total, simulated_value, analytical_value, difference))
        return comparison

    def plot(self, simulation: SimulationResult) -> None:
        """Plot simulated probabilities as a bar chart."""
        totals = list(simulation.probabilities.keys())
        values = list(simulation.probabilities.values())
        plt.figure(figsize=(8, 5))
        plt.bar(totals, values, color="#4c72b0")
        plt.title("Monte Carlo Dice Sum Probabilities")
        plt.xlabel("Sum")
        plt.ylabel("Probability")
        plt.xticks(totals)
        plt.show()


class SimulationDemo:
    def __init__(self, rolls_count: int = 100_000) -> None:
        """Prepare a simulation demo with a default number of rolls."""
        self.simulation = DiceSimulation(rolls_count)

    def run(self) -> None:
        """Run the simulation and print a comparison table."""
        result = self.simulation.simulate()
        comparison = self.simulation.compare(result)
        header = "Sum | Simulated | Analytical | Difference"
        print(header)
        print("-" * len(header))
        for total, simulated_value, analytical_value, difference in comparison:
            print(f"{total:>3} | {simulated_value:.4f}    | {analytical_value:.4f}    | {difference:+.4f}")
        self.simulation.plot(result)


if __name__ == "__main__":
    demo = SimulationDemo()
    demo.run()
