# Two-Stage Stochastic Facility Location with ML Routing Cost Estimation

## Business Context
A regional logistics company must decide which depots to open before the next planning period. Opening a depot requires a fixed investment, but once depots are open, customer demand is revealed later through one of several possible demand scenarios. After demand is known, the company would normally solve a routing problem to estimate delivery cost from the open depots to customers.

To keep the exercise computationally simple, instead of solving an exact vehicle routing problem, the second-stage delivery cost is estimated using a lightweight machine-learning style predictive formula based on demand and geometry.

## Problem Statement
You are given:
- candidate facilities (depots) with fixed opening costs,
- customers with coordinates,
- demand scenarios with probabilities,
- coefficients of a simple predictive model for routing cost.

Your task is to choose the subset of facilities to open so that the expected total cost is minimized.

For each possible open-facility set, compute the expected second-stage routing cost across all scenarios using the provided estimator. Return the facility subset with minimum total expected cost and the corresponding cost.

## First-Stage Decision Explanation
Before uncertainty is revealed, the company chooses which depots to open.

Decision variable:
- open facility j or not.

This decision incurs fixed opening costs immediately.

## Second-Stage Uncertainty Explanation
After opening facilities, a demand scenario is realized. Each scenario provides:
- customer demands,
- a probability of occurrence.

Given the realized scenario and the chosen open facilities, the routing cost is not solved exactly. Instead, it is estimated from the scenario data and open-facility geometry.

## ML Estimation Idea
Use the following predictive model for routing cost:

routing_cost_estimate =
β0 + β1 * total_demand + β2 * average_distance_to_nearest_open_facility + β3 * number_of_open_facilities + β4 * max_customer_demand

Where:
- total_demand is the sum of customer demands in the scenario,
- average_distance_to_nearest_open_facility is the average, over customers, of the Euclidean distance to the closest open facility,
- number_of_open_facilities is the size of the chosen set,
- max_customer_demand is the maximum demand among customers in the scenario.

If no facility is open, treat the routing estimate as infeasible; such a combination should be ignored.

## Mathematical Model

### Sets
- F: set of candidate facilities
- C: set of customers
- S: set of demand scenarios

### Parameters
- f_j: fixed opening cost of facility j ∈ F
- p_s: probability of scenario s ∈ S
- d_{i}: demand of customer i in scenario s
- (x_j, y_j): coordinates of facility j
- (a_i, b_i): coordinates of customer i
- β0, β1, β2, β3, β4: ML model coefficients

### First-Stage Decision Variables
- y_j ∈ {0,1}: 1 if facility j is opened, 0 otherwise

### Scenario-Dependent Second-Stage Quantities
For each scenario s and chosen open set Y:
- total_demand_s = Σ_{i∈C} d_{i,s}
- max_customer_demand_s = max_{i∈C} d_{i,s}
- nearest_distance_{i}(Y) = min_{j∈F: y_j=1} distance((a_i,b_i),(x_j,y_j))
- average_distance_s(Y) = (1/|C|) Σ_{i∈C} nearest_distance_i(Y)
- routing_cost_s(Y) = β0 + β1·total_demand_s + β2·average_distance_s(Y) + β3·(Σ_{j∈F} y_j) + β4·max_customer_demand_s

### Objective Function
Minimize total expected cost:

minimize  Σ_{j∈F} f_j y_j + Σ_{s∈S} p_s routing_cost_s(Y)

### Constraints
- y_j ∈ {0,1} for all j ∈ F
- At least one facility must be open to serve customers.

### Expected Cost Calculation
For a chosen open set Y:
- Fixed cost = Σ_{j∈F} f_j y_j
- Expected routing cost = Σ_{s∈S} p_s routing_cost_s(Y)
- Total expected cost = fixed cost + expected routing cost

## Input Format
The input is a JSON string with the following fields:
- facilities: list of objects, each with:
  - id: string
  - x: number
  - y: number
  - fixed_cost: number
- customers: list of objects, each with:
  - id: string
  - x: number
  - y: number
- scenarios: list of objects, each with:
  - probability: number
  - demands: list of numbers, one per customer in the same order as customers
- beta: list of 5 numbers [β0, β1, β2, β3, β4]

## Output Format
Return a JSON string with:
- open_facilities: list of facility ids to open, in input order
- minimum_expected_cost: number

## Constraints
- 1 ≤ number of facilities ≤ 10
- 1 ≤ number of customers ≤ 20
- 1 ≤ number of scenarios ≤ 20
- Scenario probabilities sum to 1
- All coordinates are real numbers
- Demands are nonnegative numbers
- Fixed costs and coefficients are real numbers
- Brute force enumeration is acceptable because instance sizes are small

## Example Input
{"facilities":[{"id":"D1","x":0,"y":0,"fixed_cost":80},{"id":"D2","x":10,"y":0,"fixed_cost":70}],"customers":[{"id":"C1","x":2,"y":1},{"id":"C2","x":8,"y":1}],"scenarios":[{"probability":0.6,"demands":[5,3]},{"probability":0.4,"demands":[2,7]}],"beta":[5,2,1,4,0.5]}

## Example Output
{"open_facilities":["D2"],"minimum_expected_cost":108.406}
