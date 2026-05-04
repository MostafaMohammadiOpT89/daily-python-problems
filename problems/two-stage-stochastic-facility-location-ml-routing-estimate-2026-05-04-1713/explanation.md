## Problem Intuition
The company must make a strategic decision now: which depots to open. That decision affects both the immediate fixed cost and the future delivery cost.

If the company opens facilities close to customers, the estimated routing cost tends to be lower. But opening more facilities is expensive. The challenge is to balance these two effects under uncertain customer demand.

## Why This Is a Two-Stage Stochastic Problem
This is a two-stage stochastic optimization problem because:
1. **Stage 1:** choose the depot-opening plan before demand is known.
2. **Stage 2:** after demand is revealed, compute the delivery cost associated with that plan.

The second-stage cost depends on the realized scenario. The objective is to minimize the **expected** total cost over all possible scenarios.

## How ML Is Used to Approximate Second-Stage Routing Cost
Exact routing is often expensive to solve, especially inside a larger optimization problem. To keep the exercise tractable, routing cost is approximated with a linear prediction model.

The estimator uses four features:
- total demand,
- average distance from customers to the nearest open facility,
- number of open facilities,
- maximum customer demand.

This is a simplified surrogate model: it behaves like a machine-learning regression formula and stands in for an expensive routing solver.

## Mathematical Model
Let y_j be 1 if facility j is opened, 0 otherwise.

For each scenario s:
- total_demand_s = sum_i d_{is}
- max_customer_demand_s = max_i d_{is}
- avg_dist_s(y) = average over customers of the distance to the nearest open facility

Estimated routing cost:

r_s(y) = beta_0 + beta_1 total_demand_s + beta_2 avg_dist_s(y) + beta_3 sum_j y_j + beta_4 max_customer_demand_s

Total expected cost:

sum_j f_j y_j + sum_s p_s r_s(y)

Subject to:
- y_j in {0,1}
- sum_j y_j >= 1

## Algorithm Explanation
The number of facilities is small, so the solution uses brute force:
1. Enumerate every non-empty subset of facilities.
2. Compute the fixed opening cost for the subset.
3. For each demand scenario, compute:
   - total demand,
   - max demand,
   - average distance from each customer to the nearest open depot,
   - estimated routing cost using the linear model.
4. Multiply each scenario cost by its probability and sum them.
5. Keep the subset with the lowest expected total cost.

Tie-breaking is deterministic: if two subsets have the same cost, the lexicographically smaller facility-id list is chosen.

## Limitations of This Approximation
- The routing cost is not exact; it is only a prediction.
- The linear estimator cannot capture all operational details of real vehicle routing.
- Capacity, vehicle limits, time windows, and route feasibility are ignored.
- Because the model is approximate, the chosen facilities may differ from the true optimum under exact routing.

## Time Complexity
If there are F facilities, the algorithm checks all non-empty subsets, so there are O(2^F) combinations.

For each subset, it evaluates every scenario and computes customer-to-facility distances, giving a total complexity of approximately:

O(2^F * S * C * F)

where S is the number of scenarios and C is the number of customers.

This is feasible for the small instances used in this exercise.

## Practical Logistics Interpretation
In practice, this model helps a logistics planner decide where to place depots when future demand is uncertain.

A higher number of opened facilities usually improves proximity to customers, which reduces expected delivery effort. However, the company pays fixed costs for every depot it opens. The model therefore captures the classic trade-off between network coverage and operating cost, while using an ML-style surrogate to estimate delivery expense quickly.
