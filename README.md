# goit-algo-fp

## Task 7 Conclusions: Monte Carlo Method vs Analytical Calculations

### Simulation Results

The program performs a Monte Carlo simulation of rolling two dice (100,000 rolls) and compares the obtained probabilities with analytical calculations.

### Analytical Probabilities (Theoretical)

When rolling two dice, there are 36 possible combinations. Probabilities for each sum:

| Sum  | Probability   | Explanation                          |
|------|---------------|--------------------------------------|
| 2    | 2.78% (1/36)  | 1 combination: (1,1)                 |
| 3    | 5.56% (2/36)  | 2 combinations: (1,2), (2,1)         |
| 4    | 8.33% (3/36)  | 3 combinations: (1,3), (2,2), (3,1)  |
| 5    | 11.11% (4/36) | 4 combinations                       |
| 6    | 13.89% (5/36) | 5 combinations                       |
| 7    | 16.67% (6/36) | 6 combinations                       |
| 8    | 13.89% (5/36) | 5 combinations                       |
| 9    | 11.11% (4/36) | 4 combinations                       |
| 10   | 8.33% (3/36)  | 3 combinations                       |
| 11   | 5.56% (2/36)  | 2 combinations                       |
| 12   | 2.78% (1/36)  | 1 combination: (6,6)                 |

### Results Comparison

The Monte Carlo method shows results that are very close to analytical calculations:

1. **Convergence**: As the number of simulations increases (100,000 rolls), the obtained probabilities approach theoretical values.

2. **Accuracy**: The difference between simulated and analytical probabilities is less than 0.5% for each sum.

3. **Distribution**: Both methods show a symmetric distribution with a peak at sum 7, which confirms the correctness of the implementation.

### Conclusion

The Monte Carlo method successfully validates the analytical calculations. The more iterations performed, the more accurately simulated probabilities approach theoretical values. This demonstrates the correctness of the software implementation and the effectiveness of the Monte Carlo method for estimating probabilities in random processes.
