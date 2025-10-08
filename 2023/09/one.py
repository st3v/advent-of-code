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
    last = []
    while not all_equal(h):
        last.append(h[-1])
        h = diffs(h)

    prev = h[-1]
    for l in reversed(last):
        prev += l

    total += prev

print(total)
