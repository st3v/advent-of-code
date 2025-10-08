from sys import argv


def all_equal(nums):
    for a, b in zip(nums, nums[1:]):
        if a != b:
            return False
    return True


def diffs(nums):
    res = []
    for a, b in zip(nums, nums[1:]):
        res.append(b - a)
    return res


histories = []
with open(argv[1]) as file:
    for line in file:
        histories.append(list(map(int, line.strip().split())))

total = 0
for h in histories:
    first = []
    while not all_equal(h):
        first.append(h[0])
        h = diffs(h)

    prev = h[0]
    for f in reversed(first):
        prev = f - prev

    total += prev

print(total)
