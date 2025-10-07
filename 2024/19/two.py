from sys import argv
from collections import Counter


def read(path):
    with open(path, "r") as file:
        towels, patterns = file.read().strip().split("\n\n")

    towels = [t.strip() for t in towels.strip().split(",")]
    patterns = [p.strip() for p in patterns.strip().split("\n")]

    return towels, patterns


def valid(pattern, towels, memo):
    if pattern in memo:
        return memo[pattern]

    count = 0
    for t in towels:
        l = len(t)
        if l > len(pattern):
            continue

        if l == len(pattern) and pattern == t:
            count += 1
            continue

        if pattern[:l] == t:
            count += valid(pattern[l:], towels, memo)

    memo[pattern] = count
    return count


towels, patterns = read(argv[1])
towels.sort(key=lambda x: -len(x))

total = 0
memo = {}
for p in patterns:
    total += valid(p, towels, memo)

print(total)
