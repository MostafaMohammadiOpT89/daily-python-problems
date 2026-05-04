import json

from solution import solve


def parse_output(output: str):
    return json.loads(output)


def test_single_facility():
    input_data = json.dumps({
        "facilities": [{"id": "A", "x": 0, "y": 0, "fixed_cost": 10}],
        "customers": [{"id": "C1", "x": 1, "y": 0}],
        "scenarios": [{"probability": 1.0, "demands": [5]}],
        "beta": [0, 0, 1, 0, 0],
    })
    out = parse_output(solve(input_data))
    assert out["open_facilities"] == ["A"]
    assert out["minimum_expected_cost"] == 11.0


def test_one_scenario():
    input_data = json.dumps({
        "facilities": [
            {"id": "A", "x": 0, "y": 0, "fixed_cost": 3},
            {"id": "B", "x": 10, "y": 0, "fixed_cost": 3},
        ],
        "customers": [
            {"id": "C1", "x": 1, "y": 0},
            {"id": "C2", "x": 9, "y": 0},
        ],
        "scenarios": [{"probability": 1.0, "demands": [2, 2]}],
        "beta": [0, 0, 10, 0, 0],
    })
    out = parse_output(solve(input_data))
    assert out["open_facilities"] in (["A"], ["B"])
    assert out["minimum_expected_cost"] == 23.0


def test_equal_cost_alternatives_choose_lexicographically_smallest():
    input_data = json.dumps({
        "facilities": [
            {"id": "A", "x": 0, "y": 0, "fixed_cost": 5},
            {"id": "B", "x": 10, "y": 0, "fixed_cost": 5},
        ],
        "customers": [{"id": "C1", "x": 5, "y": 0}],
        "scenarios": [{"probability": 1.0, "demands": [1]}],
        "beta": [0, 0, 0, 0, 0],
    })
    out = parse_output(solve(input_data))
    assert out["minimum_expected_cost"] == 5.0
    assert out["open_facilities"] == ["A"]


def test_high_fixed_cost_vs_low_routing_cost_tradeoff():
    input_data = json.dumps({
        "facilities": [
            {"id": "Near", "x": 0, "y": 0, "fixed_cost": 100},
            {"id": "Far", "x": 100, "y": 0, "fixed_cost": 1},
        ],
        "customers": [{"id": "C1", "x": 1, "y": 0}],
        "scenarios": [{"probability": 1.0, "demands": [1]}],
        "beta": [0, 0, 5, 0, 0],
    })
    out = parse_output(solve(input_data))
    assert out["open_facilities"] == ["Far"]
    assert out["minimum_expected_cost"] == 6.0


def test_zero_demand_scenario():
    input_data = json.dumps({
        "facilities": [
            {"id": "A", "x": 0, "y": 0, "fixed_cost": 2},
            {"id": "B", "x": 2, "y": 0, "fixed_cost": 2},
        ],
        "customers": [{"id": "C1", "x": 1, "y": 0}],
        "scenarios": [
            {"probability": 0.5, "demands": [0]},
            {"probability": 0.5, "demands": [4]},
        ],
        "beta": [1, 2, 0, 0, 3],
    })
    out = parse_output(solve(input_data))
    assert out["open_facilities"] in (["A"], ["B"])
    assert out["minimum_expected_cost"] == 7.0
