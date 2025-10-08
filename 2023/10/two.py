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

# which tile connects to a given set of directions?
TILE_BY_CONNECTION = {c: t for t, c in CONNECTIONS_BY_TILE.items()}

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
            positions.append((nr, nc, [start]))

    visited = {}
    while True:
        nxt = []
        for r, c, path in positions:
            origin = ORIGIN[(r - path[-1][0], c - path[-1][1])]
            path.append((r, c))
            for dr, dc, new_origin in next_moves(grid[r][c], origin):
                nr, nc = r + dr, c + dc
                if on_grid(nr, nc, grid) and valid_move(grid[nr][nc], new_origin):
                    if (nr, nc) in visited:
                        # loop is current path plus the position of the next tile,
                        # plus the reversed path that has seen the next tile before,
                        # minus the duplicated starting position
                        return path + [(nr, nc)] + list(reversed(visited[(nr, nc)][1:]))
                    visited[(nr, nc)] = path
                    nxt.append((nr, nc, path))
        positions = nxt


def set_starting_tile(grid, loop):
    first = loop[0]
    second = loop[1]
    last = loop[-1]

    out_dir = (first[0] - second[0], first[1] - second[1])
    in_dir = (first[0] - last[0], first[1] - last[1])

    tile = TILE_BY_CONNECTION[ORIGIN[out_dir] | ORIGIN[in_dir]]
    grid[first[0]][first[1]] = tile


def remove_non_loop_tiles(grid, loop):
    loop_positions = set(loop)
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if (r, c) not in loop_positions:
                grid[r][c] = EMPTY


def find_inside_tiles(grid):
    total = 0
    for r in range(len(grid)):
        border = 0
        inside = False
        for c in range(len(grid[r])):
            border ^= CONNECTIONS_BY_TILE[grid[r][c]] & CONNECTIONS_BY_TILE[VERTICAL]
            if border == CONNECTIONS_BY_TILE[VERTICAL]:
                inside = not inside
                border = 0
            if inside and grid[r][c] == EMPTY:
                total += 1
    return total


grid = []
with open(argv[1]) as file:
    for line in file:
        grid.append(list(line.strip()))

loop = find_loop(grid)
set_starting_tile(grid, loop)
remove_non_loop_tiles(grid, loop)
print(find_inside_tiles(grid))
