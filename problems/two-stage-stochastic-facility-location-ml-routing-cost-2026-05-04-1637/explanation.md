## Problem Intuition
A logistics company wants to decide which depots to open before seeing actual demand. Opening depots costs money upfront, but opening the right depots can reduce delivery cost later because customers are closer to at least one open facility.

The twist is that instead of running a full vehicle routing optimization after demand is realized, we approximate routing cost with a simple predictive formula. This keeps the problem small enough to brute force while still capturing the tradeoff between fixed facility costs and operational delivery costs.

## Why This Is a Two-Stage Stochastic Problem
This is a two-stage stochastic optimization model because:
1. First stage: choose facility openings before uncertainty is known.
2. Second stage: after demand scenario is revealed, compute the resulting delivery/routing cost.
3. Objective: minimize expected total cost over all scenarios.

The uncertainty comes from future customer demand, which is modeled using multiple scenarios with probabilities.

## How ML Is Used to Approximate Second-Stage Routing Cost
In a realistic logistics setting, the second stage would be a routing problem, often NP-hard and expensive to solve repeatedly.

Instead, the model uses a simple linear predictor:
- total demand
- average distance from customers to nearest open facility
- number of open facilities
- maximum customer demand

These are features that a regression model might use to estimate routing effort. The coefficients β act like learned model weights. In this exercise, they are provided directly.

## Mathematical Model
Let:
- F be facilities,
- C be customers,
- S be demand scenarios.

Decision variables:
- y_j ∈ {0,1} for each facility j.

For scenario s:
- total demand is the sum of customer demands,
- max demand is the largest customer demand,
- each customer is assigned to the nearest open facility only for distance estimation,
- average distance is the average of these nearest distances.

Routing estimate:
- r_s(Y) = β0 + β1 total_demand_s + β2 average_distance_s(Y) + β3 |Y| + β4 max_customer_demand_s

Expected cost:
- fixed cost + Σ p_s r_s(Y)

The optimization chooses the facility subset Y minimizing this expression.

## Algorithm Explanation
Because the number of facilities is small, the solution simply enumerates every non-empty subset of facilities.

For each subset:
1. Compute fixed opening cost.
2. For every scenario, compute total demand, max demand, and average distance to the nearest open facility.
3. Evaluate the ML routing cost estimate.
4. Multiply by scenario probability and sum to get expected routing cost.
5. Add fixed cost.
6. Keep the subset with the smallest total cost.

Tie-breaking is handled lexicographically by facility ids to ensure deterministic output.

## Limitations of This Approximation
- The routing cost is not exact; it is only a proxy.
- The formula ignores vehicle capacities, route sequencing, time windows, and congestion.
- The distance feature uses nearest-open-facility distances, which may not reflect real route structure.
- If the coefficients are poorly estimated, the chosen depots may be suboptimal.

## Time Complexity
If there are n facilities, there are 2^n subsets.
For each subset and each scenario, we compute distances from each customer to the nearest open facility.

Complexity is roughly:
- O(2^n * |S| * |C| * |F|)

This is acceptable here because the instances are intentionally small.

## Practical Logistics Interpretation
The model helps a company compare depot-opening strategies under uncertain demand without solving a hard routing problem repeatedly.

A planner can interpret the output as:
- which depots should be opened now,
- how much expected total cost that decision would create,
- and how demand uncertainty affects the tradeoff between fixed and operational costs.

This is a realistic simplification for strategic network design when detailed operational routing is too expensive to solve inside a larger planning loop.