from sys import argv
from itertools import combinations


def read(path):
    grid = []
    with open(path) as file:
        for line in file:
            grid.append(list(line.strip()))
    return grid


def get_offsets(grid):
    empty_row_count = 0
    row_offsets = []
    empty_cols = [True for _ in range(len(grid[0]))]
    for r in range(len(grid)):
        row_offsets.append(empty_row_count)
        empty = True
        for c in range(len(grid[r])):
            empty &= grid[r][c] == "."
            empty_cols[c] &= grid[r][c] == "."
        empty_row_count += 1 if empty else 0

    empty_col_count = 0
    col_offsets = []
    for empty in empty_cols:
        col_offsets.append(empty_col_count)
        empty_col_count += 1 if empty else 0

    return [
        [(row_offsets[r], col_offsets[c]) for c in range(len(grid[r]))]
        for r in range(len(grid))
    ]


def find_galaxies(grid):
    res = []
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == "#":
                res.append((r, c))
    return res


def distance(a, b, offsets, factor=2):
    ax, ay = a
    bx, by = b
    off = zip(offsets[ax][ay], offsets[bx][by])
    ox, oy = (abs(a - b) * (factor - 1) for a, b in off)
    return abs(ax - bx) + abs(ay - by) + ox + oy


grid = read(argv[1])
offsets = get_offsets(grid)
galaxies = find_galaxies(grid)
expand_by = int(argv[2]) if len(argv) > 2 else 10**6
total = 0
for a, b in combinations(galaxies, 2):
    total += distance(a, b, offsets, expand_by)
print(total)
