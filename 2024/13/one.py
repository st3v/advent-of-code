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
    ax, ay = a
    bx, by = b
    px, py = p

    f = px / py
    g = (ay * f - ax) / (bx - by * f)

    num_a = round(px / (ax + bx * g))
    num_b = round(py * g / (ay + by * g))

    if num_a * ax + num_b * bx == px and num_a * ay + num_b * by == py:
        total += 3 * num_a + num_b

print(total)
