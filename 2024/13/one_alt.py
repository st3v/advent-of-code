from sys import argv
import re

machines: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]] = []
with open(argv[1], "r") as file:
    button_a = (-1, -1)
    button_b = (-1, -1)
    prize = (-1, -1)
    for line in file:
        res = re.findall("Button A: X\\+([0-9]*), Y\\+([0-9]*)", line)
        if res:
            button_a = tuple(map(int, res[0]))
            continue

        res = re.findall("Button B: X\\+([0-9]*), Y\\+([0-9]*)", line)
        if res:
            button_b = tuple(map(int, res[0]))
            continue

        res = re.findall("Prize: X=([0-9]*), Y=([0-9]*)", line)
        if res:
            prize = tuple(map(int, res[0]))
            machines.append((button_a, button_b, prize))

total = 0
for a, b, p in machines:
    memo_a: dict[tuple[int, int], int] = {}
    memo_b: dict[tuple[int, int], int] = {}

    ax, ay = a
    bx, by = b
    px, py = p

    x, y = 0, 0
    memo_a[(x, y)] = 0
    while 0 <= x < px and 0 <= y < py:
        n = memo_a[(x, y)]
        x, y = x + ax, y + ay
        memo_a[(x, y)] = n + 1

    candidates: list[tuple[int, int]] = []
    x, y = 0, 0
    memo_b[(x, y)] = 0
    while 0 <= x < px and 0 <= y < py:
        n = memo_b[(x, y)]
        dx, dy = px - x, py - y
        if (dx, dy) in memo_a:
            candidates.append((memo_a[(dx, dy)], n))
        x, y = x + bx, y + by
        memo_b[(x, y)] = n + 1

    if candidates:
        a, b, max = 0, 0, 0
        for n, m in candidates:
            if m > max:
                a, b, max = n, m, m
        total += a * 3 + b

print(total)
