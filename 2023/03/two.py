from sys import argv
from collections import defaultdict


def read(path):
    grid = []
    with open(path) as file:
        for line in file:
            grid.append(list(line.strip()))
    return grid


def is_digit(s):
    return s in "0123456789"


def neighbor_gear(r, c, grid):
    for dr, dc in [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
        (1, 1),
        (1, -1),
        (-1, -1),
        (-1, 1),
    ]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]):
            if grid[nr][nc] not in ".0123456789":
                return (nr, nc)

    return None


def find_gears(grid):
    gears = defaultdict(list)
    for r in range(len(grid)):
        curr = 0
        gear_positions = set()
        for c in range(len(grid[r])):
            if is_digit(grid[r][c]):
                curr = curr * 10 + int(grid[r][c])
                gear_pos = neighbor_gear(r, c, grid)
                if gear_pos is not None:
                    gear_positions.add(gear_pos)
            elif curr > 0:
                for pos in gear_positions:
                    gears[pos].append(curr)
                curr = 0
                gear_positions = set()

        if curr > 0:
            for pos in gear_positions:
                gears[pos].append(curr)

    return gears


grid = read(argv[1])
gears = find_gears(grid)
print(sum(nums[0] * nums[1] for nums in gears.values() if len(nums) == 2))
