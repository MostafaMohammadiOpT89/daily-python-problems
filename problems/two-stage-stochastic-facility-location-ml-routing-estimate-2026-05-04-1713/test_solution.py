import json

from solution import solve


def parse_output(output):
    return json.loads(output)


def test_only_one_facility():
    input_data = json.dumps({
        "facilities": [{"id": "A", "x": 0, "y": 0, "fixed_cost": 7}],
        "customers": [{"id": "C1", "x": 1, "y": 0}],
        "scenarios": [{"probability": 1.0, "demands": [2]}],
        "beta": [1, 2, 3, 4, 5],
    })
    out = parse_output(solve(input_data))
    assert out["selected_facilities"] == ["A"]
    assert abs(out["minimum_expected_cost"] - 22.0) < 1e-6


def test_one_scenario():
    input_data = json.dumps({
        "facilities": [
            {"id": "A", "x": 0, "y": 0, "fixed_cost": 1},
            {"id": "B", "x": 10, "y": 0, "fixed_cost": 1},
        ],
        "customers": [{"id": "C1", "x": 1, "y": 0}, {"id": "C2", "x": 9, "y": 0}],
        "scenarios": [{"probability": 1.0, "demands": [1, 1]}],
        "beta": [0, 0, 10, 0, 0],
    })
    out = parse_output(solve(input_data))
    assert out["selected_facilities"] in (["A"], ["B"])
    assert abs(out["minimum_expected_cost"] - 11.0) < 1e-6


def test_equal_cost_alternatives_tie_break():
    input_data = json.dumps({
        "facilities": [
            {"id": "A", "x": 0, "y": 0, "fixed_cost": 5},
            {"id": "B", "x": 10, "y": 0, "fixed_cost": 5},
        ],
        "customers": [{"id": "C1", "x": 5, "y": 0}],
        "scenarios": [{"probability": 1.0, "demands": [0]}],
        "beta": [0, 0, 0, 0, 0],
    })
    out = parse_output(solve(input_data))
    assert out["selected_facilities"] == ["A"]
    assert abs(out["minimum_expected_cost"] - 5.0) < 1e-6


def test_high_fixed_cost_vs_low_routing_cost_tradeoff():
    input_data = json.dumps({
        "facilities": [
            {"id": "Near", "x": 0, "y": 0, "fixed_cost": 20},
            {"id": "Far", "x": 100, "y": 0, "fixed_cost": 1},
        ],
        "customers": [{"id": "C1", "x": 1, "y": 0}],
        "scenarios": [{"probability": 1.0, "demands": [1]}],
        "beta": [0, 0, 10, 0, 0],
    })
    out = parse_output(solve(input_data))
    assert out["selected_facilities"] == ["Near"]
    assert abs(out["minimum_expected_cost"] - 30.0) < 1e-6


def test_zero_demand_scenario():
    input_data = json.dumps({
        "facilities": [
            {"id": "A", "x": 0, "y": 0, "fixed_cost": 2},
            {"id": "B", "x": 2, "y": 0, "fixed_cost": 2},
        ],
        "customers": [{"id": "C1", "x": 1, "y": 0}, {"id": "C2", "x": 2, "y": 0}],
        "scenarios": [{"probability": 1.0, "demands": [0, 0]}],
        "beta": [3, 4, 5, 6, 7],
    })
    out = parse_output(solve(input_data))
    assert out["selected_facilities"] == ["A"]
    assert abs(out["minimum_expected_cost"] - 11.5) < 1e-6


def test_multiple_scenarios_expected_value():
    input_data = json.dumps({
        "facilities": [
            {"id": "A", "x": 0, "y": 0, "fixed_cost": 1},
            {"id": "B", "x": 4, "y": 0, "fixed_cost": 3},
        ],
        "customers": [{"id": "C1", "x": 1, "y": 0}],
        "scenarios": [
            {"probability": 0.25, "demands": [0]},
            {"probability": 0.75, "demands": [4]},
        ],
        "beta": [1, 1, 0, 0, 0],
    })
    out = parse_output(solve(input_data))
    assert out["selected_facilities"] == ["A"]
    assert abs(out["minimum_expected_cost"] - 3.25) < 1e-6
