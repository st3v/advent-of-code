from sys import argv, exit
import heapq


def read(path):
    with open(path, "r") as file:
        return [list(l.strip()) for l in file.readlines()]


def find(sym, grid):
    return next(
        (
            (r, c)
            for r in range(len(grid))
            for c in range(len(grid[0]))
            if grid[r][c] == sym
        ),
        None,
    )


def get_path(sp, end):
    path = []
    while end in sp:
        steps, (px, py) = sp[end]
        path.append(end)
        end = px, py
    return list(reversed(path))


def find_path(start, end, grid):
    sp = {}
    pq = [(0, *start, -1, -1)]
    steps = 0
    while pq:
        steps, x, y, px, py = heapq.heappop(pq)

        if (x, y) in sp and sp[(x, y)][0] < steps:
            continue

        sp[(x, y)] = (steps, (px, py))
        if (x, y) == end:
            return get_path(sp, end)

        steps += 1

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy

            if grid[x][y] == "#":
                continue

            if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
                continue

            if (nx, ny) not in sp or sp[(nx, ny)][0] > steps:
                heapq.heappush(pq, (steps, nx, ny, x, y))

    return []


def solve_brute(path, min_saving, radius):
    total = 0
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            steps = j - i
            sx, sy = path[i]
            ex, ey = path[j]
            dist = abs(ex - sx) + abs(ey - sy)
            saving = steps - dist
            if dist <= radius and saving >= min_saving:
                total += 1

    print(total)


def solve_better(path, min_saving, radius):
    offsets = []
    for dx in range(-radius, radius + 1):
        max = radius - abs(dx)
        for dy in range(-max, max + 1):
            offsets.append((dx, dy))

    path_positions = {p: i for i, p in enumerate(path)}
    total = 0
    for i in range(len(path)):
        sx, sy = path[i]
        for dx, dy in offsets:
            ex, ey = sx + dx, sy + dy
            if (ex, ey) not in path_positions:
                continue

            j = path_positions[(ex, ey)]
            if j <= i:
                continue

            dist = abs(dx) + abs(dy)
            steps = j - i
            if steps - dist >= min_saving:
                total += 1

    print(total)


"""
This script can be used to solve both Part Two and One:

    Part Two: `python two.py input.txt 100`
    Part One: `python two.py input.txt 100 2`

    Example for Part Tow: `python two.py example.txt 50`
    Example for Part One: `python two.py example.txt 2 2`

The script contains my original brute-force solution for Part
Two and an optimized version of that which limits the elements
we iterate over when searching for cheats.
"""

try:
    grid = read(argv[1])
    min_saving = int(argv[2])
    radius = 20 if len(argv) < 4 else int(argv[3])
except IndexError:
    print(
        f"Missing arguments: python {argv[0]} <path-to-data> <min-saving> [<max-cheat-time>]"
    )
    exit(-1)

start = find("S", grid)
end = find("E", grid)
path = find_path(start, end, grid)

# import timeit
# time = timeit.timeit(lambda: solve_brute(path, min_saving, radius), number=1)
# print(f"Brute-force: {time:.2f} seconds")
# time = timeit.timeit(lambda: solve_better(path, min_saving, radius), number=1)
# print(f"Better: {time:.2f} seconds")

solve_better(path, min_saving, radius)
