from __future__ import annotations

import json
import math
from itertools import combinations
from typing import Any


def _euclidean_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.hypot(x1 - x2, y1 - y2)


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
    num_customers = len(customers)
    num_facilities = len(facilities)

    best_cost = float("inf")
    best_subset: list[str] = []

    # Enumerate every non-empty subset of facilities.
    for mask in range(1, 1 << num_facilities):
        open_indices = [idx for idx in range(num_facilities) if (mask >> idx) & 1]
        num_open = len(open_indices)

        fixed_opening_cost = sum(facility_costs[idx] for idx in open_indices)
        expected_second_stage_cost = 0.0

        for scenario in scenarios:
            probability = float(scenario["probability"])
            demands = [float(x) for x in scenario["demands"]]

            total_demand = sum(demands)
            max_customer_demand = max(demands) if demands else 0.0

            # Average distance from each customer to the nearest open facility.
            distance_sum = 0.0
            for cx, cy in customer_coords:
                nearest_distance = min(
                    _euclidean_distance(cx, cy, facility_coords[idx][0], facility_coords[idx][1])
                    for idx in open_indices
                )
                distance_sum += nearest_distance
            average_distance_to_nearest_open_facility = distance_sum / num_customers if num_customers else 0.0

            routing_cost_estimate = (
                beta_0
                + beta_1 * total_demand
                + beta_2 * average_distance_to_nearest_open_facility
                + beta_3 * num_open
                + beta_4 * max_customer_demand
            )

            expected_second_stage_cost += probability * routing_cost_estimate

        total_expected_cost = fixed_opening_cost + expected_second_stage_cost

        if total_expected_cost < best_cost - 1e-12:
            best_cost = total_expected_cost
            best_subset = [facility_ids[idx] for idx in open_indices]
        elif abs(total_expected_cost - best_cost) <= 1e-12:
            # Deterministic tie-breaker: lexicographically smaller facility-id list.
            if [facility_ids[idx] for idx in open_indices] < best_subset:
                best_subset = [facility_ids[idx] for idx in open_indices]

    result = {
        "selected_facilities": best_subset,
        "minimum_expected_cost": round(best_cost, 6),
    }
    return json.dumps(result, separators=(",", ":"))
