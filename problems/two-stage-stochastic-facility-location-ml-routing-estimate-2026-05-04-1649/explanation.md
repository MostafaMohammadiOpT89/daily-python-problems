## Problem Intuition
This problem models a common logistics planning question: where should a company place depots before it knows the exact daily demand? Opening more depots can reduce delivery distance, but it also increases fixed costs. Because demand is uncertain, the decision should balance upfront investment against expected downstream delivery effort.

## Why This Is a Two-Stage Stochastic Problem
It is two-stage because:
- Stage 1: choose which depots to open before uncertainty is revealed.
- Stage 2: once a demand scenario is observed, compute the resulting delivery cost.

The uncertainty lies in the customer demand scenario. Each scenario has a probability, and the objective is to minimize the expected total cost across those scenarios.

## How ML Is Used to Approximate Second-Stage Routing Cost
Instead of solving a detailed vehicle routing problem, the second-stage cost is approximated using a linear regression-style predictor. The model uses features that are meaningful for logistics:
- total demand: more packages usually means more delivery effort,
- average distance to the nearest open facility: longer travel distances usually raise cost,
- number of open facilities: operational complexity may increase with more sites,
- maximum customer demand: a large single customer can increase route burden.

This turns the hard routing subproblem into a fast evaluation formula.

## Mathematical Model
Let y_i = 1 if facility i is opened, and 0 otherwise.
For each scenario s:
- total_demand_s = sum_j d_{j,s}
- max_customer_demand_s = max_j d_{j,s}
- average_distance_s = average_j min_{i:y_i=1} dist(j,i)

Routing cost estimate:
RC_s(y) = beta_0 + beta_1 total_demand_s + beta_2 average_distance_s + beta_3 sum_i y_i + beta_4 max_customer_demand_s

Expected total cost:
sum_i f_i y_i + sum_s p_s RC_s(y)

Subject to:
- y_i in {0,1}
- at least one facility must be opened

## Algorithm Explanation
Because the problem sizes are small, the solution brute-forces all non-empty subsets of facilities:
1. Enumerate each possible opening combination.
2. Compute fixed opening cost.
3. For every demand scenario, compute the ML-estimated routing cost.
4. Take the probability-weighted average of scenario costs.
5. Choose the subset with the smallest total expected cost.

To break ties, the implementation returns the lexicographically smallest set of facility indices.

## Limitations of This Approximation
- The routing estimate is not an exact vehicle routing solution.
- The linear model may underfit or overfit real operations.
- Interactions such as vehicle capacity, route consolidation, and time windows are ignored.
- Average distance to the nearest depot is a coarse proxy for real route length.

## Time Complexity
Let F be the number of facilities, C the number of customers, and S the number of scenarios.
- There are 2^F - 1 facility subsets.
- For each subset, computing scenario costs requires O(S * C * F) in the straightforward implementation.

So the total complexity is O(2^F * S * C * F), which is feasible for the small instances in this exercise.

## Practical Logistics Interpretation
In practice, this models a company that must decide depot locations before knowing tomorrow’s demand. The ML estimator acts like a fast surrogate for a much more expensive routing optimizer, allowing planners to test many network designs quickly and select a cost-effective one under uncertainty.