from __future__ import annotations

import json
import math
from itertools import combinations
from typing import Any


def solve(input_data: str) -> str:
    data = json.loads(input_data)

    facilities = data["facilities"]
    customers = data["customers"]
    scenarios = data["scenarios"]
    beta_0, beta_1, beta_2, beta_3, beta_4 = data["beta"]

    facility_ids = [f["id"] for f in facilities]
    facility_coords = [(float(f["x"]), float(f["y"])) for f in facilities]
    facility_costs = [float(f["fixed_cost"]) for f in facilities]
    customer_coords = [(float(c["x"]), float(c["y"])) for c in customers]

    num_facilities = len(facilities)
    num_customers = len(customers)

    def euclidean_distance(p: tuple[float, float], q: tuple[float, float]) -> float:
        return math.hypot(p[0] - q[0], p[1] - q[1])

    best_cost = float("inf")
    best_subset: list[str] | None = None

    # Enumerate all non-empty subsets of facilities.
    for mask in range(1, 1 << num_facilities):
        open_indices = [i for i in range(num_facilities) if (mask >> i) & 1]
        open_count = len(open_indices)
        fixed_opening_cost = sum(facility_costs[i] for i in open_indices)

        expected_routing_cost = 0.0
        feasible = True

        for scenario in scenarios:
            probability = float(scenario["probability"])
            demands = [float(x) for x in scenario["demands"]]

            if open_count == 0:
                feasible = False
                break

            total_demand = sum(demands)
            max_customer_demand = max(demands) if demands else 0.0

            total_nearest_distance = 0.0
            for customer_coord in customer_coords:
                nearest_distance = min(
                    euclidean_distance(customer_coord, facility_coords[idx])
                    for idx in open_indices
                )
                total_nearest_distance += nearest_distance
            average_distance = total_nearest_distance / num_customers if num_customers else 0.0

            routing_cost = (
                beta_0
                + beta_1 * total_demand
                + beta_2 * average_distance
                + beta_3 * open_count
                + beta_4 * max_customer_demand
            )
            expected_routing_cost += probability * routing_cost

        if not feasible:
            continue

        total_cost = fixed_opening_cost + expected_routing_cost

        if total_cost < best_cost - 1e-12:
            best_cost = total_cost
            best_subset = [facility_ids[i] for i in open_indices]
        elif abs(total_cost - best_cost) <= 1e-12 and best_subset is not None:
            candidate_subset = [facility_ids[i] for i in open_indices]
            if candidate_subset < best_subset:
                best_subset = candidate_subset

    if best_subset is None:
        best_subset = []
        best_cost = 0.0

    result = {
        "open_facilities": best_subset,
        "minimum_expected_cost": round(best_cost, 6),
    }
    return json.dumps(result, separators=(",", ":"))
