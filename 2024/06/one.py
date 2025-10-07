from sys import argv


def find_guard(map: list[list[str]]) -> tuple[int, int]:
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] in ("^", ">", "v", "<"):
                return (y, x)

    return (-1, -1)


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


def turn(guard: str) -> str:
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
    return map[y][x] == "#"


map: list[list[str]] = []
with open(argv[1], "r") as file:
    for line in file:
        map.append(list(line.strip()))

total = 0
VISITED = "X"
y, x = find_guard(map)
guard = map[y][x]

while on_map(map, y, x):
    if map[y][x] != VISITED:
        total += 1
        map[y][x] = VISITED

    if is_obstacle(map, *next_pos(guard, y, x)):
        guard = turn(guard)

    y, x = next_pos(guard, y, x)

print(total)
