from sys import argv


def read(path):
    with open(path, "r") as file:
        return [list(l.strip()) for l in file.readlines()]


def find_start(grid):
    return next(
        (r, c)
        for r in range(len(grid))
        for c in range(len(grid[0]))
        if grid[r][c] == "S"
    )


grid = read(argv[1])
min_saving = int(argv[2])


start = find_start(grid)
path = set()
walls = {}
cheats = {}

x, y = start
steps = 0
while True:
    visit_next = None
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        n = grid[nx][ny]
        if n == "#":
            if (nx, ny) not in walls:
                walls[(nx, ny)] = steps + 1
            else:
                cheats[(nx, ny)] = steps - walls[(nx, ny)] - 1
            continue

        if (nx, ny) not in path:
            visit_next = (nx, ny)

    if grid[x][y] == "E":
        break

    assert visit_next is not None
    path.add(visit_next)
    x, y = visit_next
    steps += 1

total = 0
for _, saving in cheats.items():
    if saving >= min_saving:
        total += 1

print(total)
