from sys import argv
from itertools import combinations


def read(path):
    grid = []
    with open(path) as file:
        for line in file:
            grid.append(list(line.strip()))
    return grid


def find_empty_rows_and_cols(grid):
    empty_rows = set()
    empty_cols = [True for _ in range(len(grid[0]))]
    for r in range(len(grid)):
        row_empty = True
        for c in range(len(grid[r])):
            empty_cols[c] &= grid[r][c] == "."
            row_empty &= grid[r][c] == "."
        if row_empty:
            empty_rows.add(r)

    empty_cols = set([i for i, c in enumerate(empty_cols) if c])
    return empty_rows, empty_cols


def expand(grid):
    empty_rows, empty_cols = find_empty_rows_and_cols(grid)
    num_cols = len(grid[0]) + len(empty_cols)
    expanded = []
    for r in range(0, len(grid)):
        if r - 1 in empty_rows:
            expanded.append(["." for _ in range(num_cols)])
        row = []
        for c in range(0, len(grid[r])):
            if c - 1 in empty_cols:
                row.append(".")
            row.append(grid[r][c])
        expanded.append(row)
    return expanded


def find_galaxies(grid):
    res = []
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == "#":
                res.append((r, c))
    return res


def distance(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)


total = 0
for a, b in combinations(find_galaxies(expand(read(argv[1]))), 2):
    total += distance(a, b)
print(total)
