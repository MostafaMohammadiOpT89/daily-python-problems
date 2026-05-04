from __future__ import annotations

import math
from itertools import combinations
from typing import List, Tuple


def solve(input_data: str) -> str:
    tokens = input_data.split()
    if not tokens:
        return "\n0.0"

    idx = 0
    n_facilities = int(tokens[idx]); idx += 1
    n_customers = int(tokens[idx]); idx += 1
    n_scenarios = int(tokens[idx]); idx += 1

    beta = [float(tokens[idx + k]) for k in range(5)]
    idx += 5

    facility_costs: List[float] = []
    facility_coords: List[Tuple[float, float]] = []
    for _ in range(n_facilities):
        facility_costs.append(float(tokens[idx])); idx += 1
        x = float(tokens[idx]); idx += 1
        y = float(tokens[idx]); idx += 1
        facility_coords.append((x, y))

    customer_coords: List[Tuple[float, float]] = []
    for _ in range(n_customers):
        x = float(tokens[idx]); idx += 1
        y = float(tokens[idx]); idx += 1
        customer_coords.append((x, y))

    scenario_probabilities: List[float] = []
    scenario_demands: List[List[float]] = []
    for _ in range(n_scenarios):
        p = float(tokens[idx]); idx += 1
        scenario_probabilities.append(p)
        demands = [float(tokens[idx + j]) for j in range(n_customers)]
        idx += n_customers
        scenario_demands.append(demands)

    # Precompute distances from each customer to each facility.
    distances = []
    for cx, cy in customer_coords:
        row = []
        for fx, fy in facility_coords:
            row.append(math.hypot(cx - fx, cy - fy))
        distances.append(row)

    def expected_cost_for_open_set(open_mask: int) -> float:
        opened_indices = [i for i in range(n_facilities) if (open_mask >> i) & 1]
        opening_cost = sum(facility_costs[i] for i in opened_indices)

        total_expected_routing_cost = 0.0
        for scenario_index in range(n_scenarios):
            demands = scenario_demands[scenario_index]
            total_demand = sum(demands)
            max_customer_demand = max(demands) if demands else 0.0

            if opened_indices:
                total_distance = 0.0
                for customer_index in range(n_customers):
                    best_distance = min(distances[customer_index][i] for i in opened_indices)
                    total_distance += best_distance
                average_distance = total_distance / n_customers if n_customers else 0.0
            else:
                average_distance = 0.0

            routing_cost_estimate = (
                beta[0]
                + beta[1] * total_demand
                + beta[2] * average_distance
                + beta[3] * len(opened_indices)
                + beta[4] * max_customer_demand
            )
            total_expected_routing_cost += scenario_probabilities[scenario_index] * routing_cost_estimate

        return opening_cost + total_expected_routing_cost

    best_cost = float("inf")
    best_mask = None

    for mask in range(1, 1 << n_facilities):
        cost = expected_cost_for_open_set(mask)
        if cost < best_cost - 1e-12:
            best_cost = cost
            best_mask = mask
        elif abs(cost - best_cost) <= 1e-12 and best_mask is not None:
            current_indices = [i for i in range(n_facilities) if (mask >> i) & 1]
            best_indices = [i for i in range(n_facilities) if (best_mask >> i) & 1]
            if current_indices < best_indices:
                best_mask = mask

    if best_mask is None:
        return "\n0.0"

    best_indices = [str(i + 1) for i in range(n_facilities) if (best_mask >> i) & 1]
    return " ".join(best_indices) + "\n" + f"{best_cost:.10g}"


if __name__ == "__main__":
    import sys
    print(solve(sys.stdin.read()))
