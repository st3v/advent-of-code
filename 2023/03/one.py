from sys import argv


def read(path):
    grid = []
    with open(path) as file:
        for line in file:
            grid.append(list(line.strip()))
    return grid


def is_digit(s):
    return s in "0123456789"


def is_valid(r, c, grid):
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
                return True

    return False


def sumup(grid):
    total = 0
    valid = False
    for r in range(len(grid)):
        curr = 0
        for c in range(len(grid[r])):
            if is_digit(grid[r][c]):
                curr = curr * 10 + int(grid[r][c])
                valid = valid or is_valid(r, c, grid)
            else:
                if valid:
                    total += curr
                curr = 0
                valid = False

        if valid:
            total += curr

    return total


grid = read(argv[1])
print(sumup(grid))
