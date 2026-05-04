import pytest

from solution import solve


def test_only_one_facility():
    input_data = """1 2 1
0 0 0 0 0
5 0 0
2 1
3 2
1.0 4 1
"""
    output = solve(input_data).splitlines()
    assert output[0].strip() == "1"
    assert float(output[1]) == pytest.approx(9.0)


def test_one_scenario():
    input_data = """2 1 1
1 2 0 0 0
3 0 0
2 10 0
1 0
1.0 5
"""
    output = solve(input_data).splitlines()
    assert output[0].strip() == "1"
    assert float(output[1]) == pytest.approx(9.0)


def test_equal_cost_alternatives_choose_lexicographically_smallest():
    input_data = """2 1 1
0 0 0 0 0
1 0 0
1 2 0
0 0
1.0 0
"""
    output = solve(input_data).splitlines()
    assert output[0].strip() == "1"
    assert float(output[1]) == pytest.approx(0.0)


def test_high_fixed_cost_vs_low_routing_cost_tradeoff():
    input_data = """2 2 1
0 0 10 0 0
100 0 0
1 0 0
1 10 0
10 0
1.0 1 1
"""
    output = solve(input_data).splitlines()
    assert output[0].strip() == "1"
    assert float(output[1]) == pytest.approx(20.0)


def test_zero_demand_scenario():
    input_data = """2 2 2
5 1 1 0 0
4 0 0
4 10 0
0 0
0 10
0.5 0 0
0.5 2 3
"""
    output = solve(input_data).splitlines()
    assert output[0].strip() == "1"
    assert float(output[1]) == pytest.approx(11.5)
