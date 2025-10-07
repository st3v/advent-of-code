from sys import argv
from collections import deque, Counter


def step(num):
    num = (num ^ (num * 64)) % 16777216
    num = (num ^ (num // 32)) % 16777216
    return (num ^ (num * 2048)) % 16777216


def solve(num, steps):
    diffs = deque()
    price_changes = {}
    prev = num % 10
    for _ in range(steps):
        num = step(num)
        price = num % 10
        diff = price - prev
        prev = price

        if len(diffs) == 3:
            if (seq := (*diffs, diff)) not in price_changes:
                price_changes[seq] = price
            diffs.popleft()

        diffs.append(diff)

    return price_changes


totals = Counter()
for n in map(int, open(argv[1]).readlines()):
    for seq, price in solve(n, 2000).items():
        totals[seq] += price

print(max(totals.values()))
