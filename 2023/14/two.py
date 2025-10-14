from sys import argv


def tilt_right(grid):
    res = []
    for row in grid:
        tilted = []
        empty, stones = 0, 0
        for c in row:
            if c == "O":
                stones += 1
            elif c == ".":
                empty += 1
            else:
                tilted.extend(["."] * empty)
                tilted.extend(["O"] * stones)
                tilted.append("#")
                empty, stones = 0, 0
        tilted.extend(["."] * empty)
        tilted.extend(["O"] * stones)
        res.append(tilted)
    return res


def tilt_horizontally(grid, direction):
    if direction < 0:
        reversed_grid = [list(reversed(row)) for row in grid]
        reversed_tilted = tilt_right(reversed_grid)
        return [list(reversed(row)) for row in reversed_tilted]
    return tilt_right(grid)


def tilt(grid, direction):
    if direction[0] != 0:
        transposed = list(map(list, zip(*grid)))
        transposed_tilted = tilt_horizontally(transposed, direction[0])
        return list(map(list, zip(*transposed_tilted)))
    else:
        return tilt_horizontally(grid, direction[1])


def tilt_cycle(grid):
    res = grid
    for dir in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        res = tilt(res, dir)
    return res


def key(grid):
    return hash("".join("".join(row) for row in grid))


def get_load(grid):
    load = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == "O":
                load += len(grid) - r
    return load


def read(path):
    grid = []
    with open(path) as file:
        for line in file:
            grid.append(list(line.strip()))
    return grid


grid = read(argv[1])
step = 0
configurations = {}
while (k := key(grid)) not in configurations:
    configurations[k] = (step, grid)
    grid = tilt_cycle(grid)
    step += 1

initial_steps = configurations[key(grid)][0]
repetition_frequency = step - initial_steps
final_step = ((10**9 - initial_steps) % repetition_frequency) + initial_steps
final_configuration = next(c for s, c in configurations.values() if s == final_step)

print(get_load(final_configuration))
