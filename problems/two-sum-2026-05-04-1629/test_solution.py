import pytest

from solution import solve


def test_basic_case():
    assert solve([2, 7, 11, 15], 9) in ([0, 1], [1, 0])


def test_another_case():
    assert solve([3, 2, 4], 6) in ([1, 2], [2, 1])


def test_with_duplicates():
    assert solve([3, 3], 6) in ([0, 1], [1, 0])


def test_negative_numbers():
    assert solve([-1, -2, -3, -4, -5], -8) in ([2, 4], [4, 2])


def test_zero_target():
    assert solve([0, 4, 3, 0], 0) in ([0, 3], [3, 0])


def test_solution_exists_returns_two_indices():
    result = solve([1, 5, 1, 5], 10)
    assert len(result) == 2
    i, j = result
    assert i != j
    assert [1, 5, 1, 5][i] + [1, 5, 1, 5][j] == 10