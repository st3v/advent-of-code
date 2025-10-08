from sys import argv

# tiles
VERTICAL = "|"
HORIZONTAL = "-"
NE = "L"
NW = "J"
SW = "7"
SE = "F"
EMPTY = "."
ANIMAL = "S"

# primary directions, each represented as a single bit
WEST = 1
SOUTH = 2
EAST = 4
NORTH = 8

# what directions does a given tile connect to?
CONNECTIONS_BY_TILE = {
    VERTICAL: NORTH | SOUTH,
    HORIZONTAL: WEST | EAST,
    NE: NORTH | EAST,
    NW: NORTH | WEST,
    SE: SOUTH | EAST,
    SW: SOUTH | WEST,
    ANIMAL: NORTH | SOUTH | EAST | WEST,
    EMPTY: 0,
}

# where are we going to?
DIRECTION = {EAST: (0, 1), WEST: (0, -1), NORTH: (-1, 0), SOUTH: (1, 0)}

# where are we coming from?
ORIGIN = {
    (0, 1): WEST,
    (0, -1): EAST,
    (-1, 0): SOUTH,
    (1, 0): NORTH,
}


def find_start(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == ANIMAL:
                return (r, c)
    return None


def valid_move(tile, origin):
    return tile != EMPTY and CONNECTIONS_BY_TILE[tile] & origin > 0


def next_moves(tile, origin):
    connections = CONNECTIONS_BY_TILE[tile]
    res = []
    for c in [NORTH, EAST, SOUTH, WEST]:
        if c & connections > 0 and c ^ origin > 0:
            res.append((*DIRECTION[c], ORIGIN[DIRECTION[c]]))
    return res


def on_grid(r, c, grid):
    return 0 <= r < len(grid) and 0 <= c < len(grid[r])


def find_loop(grid):
    start = find_start(grid)
    assert start is not None

    positions = []
    for (dr, dc), origin in ORIGIN.items():
        nr, nc = start[0] + dr, start[1] + dc
        if on_grid(nr, nc, grid) and valid_move(grid[nr][nc], origin):
            positions.append((nr, nc, origin))

    steps = 0
    visited = set()
    while True:
        steps += 1
        nxt = []
        for r, c, origin in positions:
            for dr, dc, new_origin in next_moves(grid[r][c], origin):
                nr, nc = r + dr, c + dc
                if on_grid(nr, nc, grid) and valid_move(grid[nr][nc], new_origin):
                    if (nr, nc) in visited:
                        return steps + 1
                    visited.add((nr, nc))
                    nxt.append((nr, nc, new_origin))
        positions = nxt


grid = []
with open(argv[1]) as file:
    for line in file:
        grid.append(list(line.strip()))

print(find_loop(grid))
