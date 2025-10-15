from sys import argv

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def next_steps(current, grid):
    x, y, dir = current
    tile = grid[x][y]

    if tile == "|" and dir in [LEFT, RIGHT]:
        nxt = [UP, DOWN]
    elif tile == "-" and dir in [UP, DOWN]:
        nxt = [LEFT, RIGHT]
    elif tile == "/":
        nxt = [(-dir[1], -dir[0])]
    elif tile == "\\":
        nxt = [(dir[1], dir[0])]
    else:
        nxt = [dir]

    res = []
    for dx, dy in nxt:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[nx]):
            res.append((nx, ny, (dx, dy)))
    return res


def read(path):
    grid = []
    with open(path) as file:
        for line in file:
            grid.append(list(line.strip()))
    return grid


def energize(start, grid):
    q = [start]
    seen = set()
    energized = set()
    while q:
        current = q.pop()
        seen.add(current)
        energized.add((current[0], current[1]))
        for n in next_steps(current, grid):
            if n not in seen:
                q.append(n)
    return len(energized)


grid = read(argv[1])
max_energized = 0

for x in range(len(grid)):
    if (e := energize((x, 0, RIGHT), grid)) > max_energized:
        max_energized = e

    if (e := energize((x, len(grid[x]) - 1, LEFT), grid)) > max_energized:
        max_energized = e

for y in range(len(grid[0])):
    if (e := energize((0, y, DOWN), grid)) > max_energized:
        max_energized = e

    if (e := energize((len(grid) - 1, y, UP), grid)) > max_energized:
        max_energized = e

print(max_energized)
