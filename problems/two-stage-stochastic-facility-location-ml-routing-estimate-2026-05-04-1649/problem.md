# Two-Stage Stochastic Facility Location with ML-Based Routing Cost Estimation

## Business Context
A logistics company must decide which depots to open before daily demand is known. Opening a depot has a fixed cost, but it can reduce downstream delivery effort because it may shorten customer-to-depot travel distances. After the depots are selected, customer demand becomes known for the day, and the company must estimate the routing/delivery cost needed to serve that demand.

In this exercise, instead of solving an exact vehicle routing problem, we use a simple machine-learning-style regression formula to estimate the second-stage routing cost under each demand scenario.

## Problem Statement
You are given:
- a set of candidate facilities (depots), each with a fixed opening cost,
- customer locations and scenario-dependent demand values,
- a set of demand scenarios with probabilities,
- coefficients of a simple predictive model for routing cost.

Your task is to evaluate every possible subset of facilities to open and choose the subset with the minimum expected total cost.

The total cost of a chosen facility set is:
- the sum of fixed opening costs of opened facilities,
- plus the expected estimated routing cost over all demand scenarios.

## First-Stage Decision Explanation
Before demand is realized, the company chooses which facilities to open. This is the first-stage decision and must be made without knowing which demand scenario will occur.

## Second-Stage Uncertainty Explanation
After the facility opening decision is fixed, one demand scenario is revealed. Customer demand changes by scenario, which affects the estimated delivery workload. The second-stage cost is not computed by an exact route optimization model; instead, it is estimated by a predictive formula that depends on:
- total demand,
- average distance from customers to the nearest open facility,
- number of open facilities,
- maximum customer demand.

## ML Estimation Idea
Use the following simplified predictive model for routing cost:

routing_cost_estimate = beta_0 + beta_1 * total_demand + beta_2 * average_distance_to_nearest_open_facility + beta_3 * number_of_open_facilities + beta_4 * max_customer_demand

This is treated as a lightweight surrogate model learned from historical routing data.

## Mathematical Model

### Sets
- F: set of candidate facilities, indexed by i
- C: set of customers, indexed by j
- S: set of demand scenarios, indexed by s

### Parameters
- f_i: fixed cost to open facility i
- (x_i, y_i): coordinates of facility i
- (u_j, v_j): coordinates of customer j
- d_{j,s}: demand of customer j in scenario s
- p_s: probability of scenario s
- beta_0, beta_1, beta_2, beta_3, beta_4: ML coefficients

### First-Stage Decision Variables
- y_i in {0,1}: 1 if facility i is opened, 0 otherwise

### Scenario-Dependent Second-Stage Quantities
For each scenario s and a chosen facility set y:
- total_demand_s = sum over j of d_{j,s}
- max_customer_demand_s = max over j of d_{j,s}
- average_distance_s = average over customers j of the distance from customer j to the nearest open facility

Let dist(j,i) be the Euclidean distance between customer j and facility i.
If no facility is open, the average distance is treated as 0.

The estimated routing cost in scenario s is:
- RC_s(y) = beta_0 + beta_1 * total_demand_s + beta_2 * average_distance_s + beta_3 * sum_i y_i + beta_4 * max_customer_demand_s

### Objective Function
Minimize total expected cost:
- sum_i f_i y_i + sum_s p_s RC_s(y)

### Constraints
- y_i in {0,1} for all i
- At least one facility must be open

### Expected Cost Calculation
For each feasible subset of facilities:
1. compute opening cost,
2. for each scenario, compute estimated routing cost using the ML model,
3. take the probability-weighted average over scenarios,
4. add opening cost.

## Input Format
The input is plain text with the following structure:

n_facilities n_customers n_scenarios
beta_0 beta_1 beta_2 beta_3 beta_4
f_1 x_1 y_1
...
f_n x_n y_n
u_1 v_1
...
u_m v_m
p_1 d_11 d_21 ... d_m1
...
p_s d_1s d_2s ... d_ms

Where:
- facilities are given by fixed cost and coordinates,
- customers are given by coordinates,
- each scenario begins with its probability followed by one demand value per customer.

## Output Format
Return two lines:
- first line: indices of opened facilities in increasing order, separated by spaces; if only one facility is opened, print that index; if multiple, print them separated by spaces
- second line: the minimum expected total cost as a decimal number

## Constraints
- 1 <= n_facilities <= 10
- 1 <= n_customers <= 20
- 1 <= n_scenarios <= 10
- 0 <= fixed costs, demands, and probabilities
- scenario probabilities sum to 1
- coordinates are real numbers with small magnitude
- brute force evaluation of all facility subsets is feasible

## Example Input
3 2 2
10 1 0 0 0
8 5 0
6 0 5
4 3 4
1 1
2 5
0.6 3 1
0.4 0 4

## Example Output
2
14.0