from sys import argv


def find_guard(map: list[list[str]]) -> tuple[str, int, int]:
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] in ("^", ">", "v", "<"):
                return (map[y][x], y, x)

    return ("", -1, -1)


def on_map(map: list[list[str]], y: int, x: int) -> bool:
    return 0 <= x < len(map[0]) and 0 <= y < len(map)


def next_pos(guard: str, y: int, x: int) -> tuple[int, int]:
    match guard:
        case "^":
            return (y - 1, x)
        case ">":
            return (y, x + 1)
        case "v":
            return (y + 1, x)
        case "<":
            return (y, x - 1)
        case _:
            return (y, x)


def turn_right(guard: str) -> str:
    match guard:
        case "^":
            return ">"
        case ">":
            return "v"
        case "v":
            return "<"
        case "<":
            return "^"
        case _:
            return guard


def is_obstacle(map: list[list[str]], y: int, x: int) -> bool:
    if not on_map(map, y, x):
        return False
    return map[y][x] in ["#", "O"]


def turn_if_needed(
    map: list[list[str]], guard: str, y: int, x: int
) -> tuple[str, bool]:
    tries = 0
    while is_obstacle(map, *next_pos(guard, y, x)):
        guard = turn_right(guard)
        tries += 1
        if tries == 4:
            return (guard, True)
    return (guard, False)


def walk_map(
    map: list[list[str]], guard: str, y: int, x: int
) -> set[tuple[str, int, int]]:
    path: set[tuple[str, int, int]] = set()
    while on_map(map, y, x):
        path.add((guard, y, x))

        guard, blocked = turn_if_needed(map, guard, y, x)
        if blocked:
            return path

        y, x = next_pos(guard, y, x)

    return path


def print_map(map: list[list[str]]):
    for row in map:
        print("".join(row))
    print("")


map: list[list[str]] = []
with open(argv[1], "r") as file:
    for line in file:
        map.append(list(line.strip()))

start = find_guard(map)
path = walk_map(map, *start)
visited: set[tuple[int, int]] = set()

loops = 0
for pos in path:
    _, y, x = pos
    if pos == start or (y, x) in visited:
        continue

    visited.add((y, x))
    prev = map[y][x]
    map[y][x] = "O"
    checked_path: set[tuple[str, int, int]] = set()

    guard, y, x = start
    while on_map(map, y, x):
        if (guard, y, x) in checked_path:
            loops += 1
            break

        checked_path.add((guard, y, x))

        guard, blocked = turn_if_needed(map, guard, y, x)
        if blocked:
            loops += 1
            break

        y, x = next_pos(guard, y, x)

    map[pos[1]][pos[2]] = prev


print(loops)
