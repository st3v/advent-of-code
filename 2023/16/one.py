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


grid = []
with open(argv[1]) as file:
    for line in file:
        grid.append(list(line.strip()))

q = [(0, 0, RIGHT)]
seen = set()
energized = set()
while q:
    current = q.pop()
    seen.add(current)
    energized.add((current[0], current[1]))
    for n in next_steps(current, grid):
        if n not in seen:
            q.append(n)

print(len(energized))
