# Two-Stage Stochastic Facility Location with ML-Based Routing Cost Estimation

## Business Context
A logistics company must decide which candidate depots to open before customer demand is known. Opening a depot incurs a fixed cost. After demand is realized, the company must serve all customers from the opened depots. Instead of solving an exact vehicle routing problem, the company uses a simple machine-learning-style estimator to predict the routing cost based on the realized demand and the chosen set of open depots.

This exercise models the trade-off between paying fixed opening costs now and reducing expected delivery costs later.

## Problem Statement
You are given:
- a set of candidate facilities (depots), each with a fixed opening cost,
- a set of customers, each with coordinates,
- a list of demand scenarios, each with a probability,
- coefficients of a linear estimator used to approximate second-stage routing cost.

Your task is to choose which facilities to open so that the expected total cost is minimized.

For any chosen set of open facilities, the second-stage routing cost for a scenario is not computed by solving routing exactly. Instead, it is estimated by a linear formula using scenario demand and geometry.

Return the facility subset with minimum expected total cost and the corresponding cost.

## First-Stage Decision Explanation
Before demand is known, the decision maker selects a subset of candidate facilities to open.

This is the first-stage decision because it must be made before uncertainty is revealed. The first-stage cost is the sum of opening costs of the selected facilities.

## Second-Stage Uncertainty Explanation
After the facility-opening decision is made, one demand scenario is realized. Each scenario specifies customer demands and has a probability of occurrence.

Once demand is known, the company would normally solve a routing or delivery problem. In this exercise, that routing cost is approximated by a predictive model instead of being optimized exactly.

## ML Estimation Idea
The second-stage routing cost is estimated with a simple linear model:

routing_cost_estimate = beta_0 + beta_1 * total_demand + beta_2 * average_distance_to_nearest_open_facility + beta_3 * number_of_open_facilities + beta_4 * max_customer_demand

where:
- total_demand is the sum of customer demands in the scenario,
- average_distance_to_nearest_open_facility is the average over customers of their Euclidean distance to the nearest open facility,
- number_of_open_facilities is the count of opened facilities,
- max_customer_demand is the largest demand among customers in the scenario.

If no facility is open, the configuration is infeasible.

## Mathematical Model

### Sets
- F: set of candidate facilities
- C: set of customers
- S: set of demand scenarios

### Parameters
- f_j: fixed opening cost of facility j in F
- (x_j, y_j): coordinates of facility j
- (u_i, v_i): coordinates of customer i
- d_{is}: demand of customer i in scenario s
- p_s: probability of scenario s
- beta_0, beta_1, beta_2, beta_3, beta_4: ML estimator coefficients

### First-Stage Decision Variables
- y_j in {0, 1}: 1 if facility j is opened, 0 otherwise

### Scenario-Dependent Second-Stage Quantities
For each scenario s and selected set of open facilities:
- total_demand_s = sum_{i in C} d_{is}
- max_customer_demand_s = max_{i in C} d_{is}
- average_distance_s(y) = (1 / |C|) * sum_{i in C} min_{j in F : y_j = 1} dist(i, j)
- estimated_routing_cost_s(y) = beta_0 + beta_1 * total_demand_s + beta_2 * average_distance_s(y) + beta_3 * sum_{j in F} y_j + beta_4 * max_customer_demand_s

### Objective Function
Minimize expected total cost:

minimize  sum_{j in F} f_j y_j + sum_{s in S} p_s * estimated_routing_cost_s(y)

### Constraints
- y_j in {0, 1} for all j in F
- At least one facility must be open:
  sum_{j in F} y_j >= 1

### Expected Cost Calculation
For each feasible facility subset Y:
1. Compute fixed opening cost = sum of opening costs of facilities in Y
2. For each scenario s, compute the ML-estimated routing cost using Y
3. Compute expected second-stage cost = sum_{s in S} p_s * routing_cost_estimate_s(Y)
4. Total cost = fixed opening cost + expected second-stage cost

Choose the subset Y with minimum total cost.

## Input Format
The input is a single JSON string with the following keys:
- facilities: list of facilities, each with fields:
  - id: string
  - x: number
  - y: number
  - fixed_cost: number
- customers: list of customers, each with fields:
  - id: string
  - x: number
  - y: number
- scenarios: list of scenarios, each with fields:
  - probability: number
  - demands: list of numbers, one per customer in input order
- beta: list of 5 numbers [beta_0, beta_1, beta_2, beta_3, beta_4]

All scenarios have demand vectors of the same length as the customer list.

## Output Format
Return a JSON string with:
- selected_facilities: list of opened facility ids in input order
- minimum_expected_cost: number rounded to 6 decimal places

## Constraints
- 1 <= number of facilities <= 15
- 1 <= number of customers <= 20
- 1 <= number of scenarios <= 20
- Facility opening costs and demand values are nonnegative
- Scenario probabilities sum to 1
- Coordinates are real numbers
- Brute force evaluation over all facility subsets is acceptable

## Example Input
{"facilities":[{"id":"F1","x":0,"y":0,"fixed_cost":10},{"id":"F2","x":10,"y":0,"fixed_cost":6}],"customers":[{"id":"C1","x":1,"y":1},{"id":"C2","x":9,"y":1}],"scenarios":[{"probability":0.5,"demands":[2,3]},{"probability":0.5,"demands":[4,1]}],"beta":[5,0.8,1.2,0.5,0.3]}

## Example Output
{"selected_facilities":["F2"],"minimum_expected_cost":16.165685}
