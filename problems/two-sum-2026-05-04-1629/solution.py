from typing import List


def solve(nums: List[int], target: int) -> List[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


if __name__ == "__main__":
    import sys

    data = sys.stdin.read().strip().split()
    if data:
        n = int(data[0])
        nums = list(map(int, data[1:1 + n]))
        target = int(data[1 + n])
        result = solve(nums, target)
        print(*result)