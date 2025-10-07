from sys import argv


def is_valid(res: int, nums: list[int]) -> bool:
    if len(nums) == 2:
        return res == nums[0] * nums[1] or res == nums[0] + nums[1]

    return is_valid(res, [nums[0] * nums[1]] + nums[2:]) or is_valid(
        res, [nums[0] + nums[1]] + nums[2:]
    )


total = 0
with open(argv[1], "r") as file:
    for line in file:
        res, nums = line.strip().split(":")
        res, nums = int(res), list(map(int, nums.strip().split(" ")))
        if is_valid(res, nums):
            total += res

print(total)
