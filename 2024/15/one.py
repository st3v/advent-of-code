from shutil import move
from sys import argv

WALL = "#"
EMPTY = "."
ROBOT = "@"
BOX = "O"

delta = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1),
}


def gps_coord(x: int, y: int) -> int:
    return 100 * y + x


def print_map(map: list[list[str]]):
    for row in map:
        print("".join(row))


def move_to(sym: str, x: int, y: int, dir: str, map: list[list[str]]) -> bool:
    if map[y][x] == WALL:
        return False

    if map[y][x] == EMPTY:
        map[y][x] = sym
        return True

    dx, dy = delta[dir]
    if move_to(map[y][x], x + dx, y + dy, dir, map):
        map[y][x] = sym
        return True

    return False


moves: list[str] = []
map: list[list[str]] = []
robot: tuple[int, int] = (-1, -1)

with open(argv[1], "r") as file:
    for line in file:
        line = line.strip()
        if line == "":
            continue

        if WALL in line:
            map.append(list(line))
            x = line.find(ROBOT)
            if x >= 0:
                robot = (x, len(map) - 1)

        else:
            moves.extend(list(line))

for dir in moves:
    dx, dy = delta[dir]
    x, y = robot
    if move_to(ROBOT, x + dx, y + dy, dir, map):
        map[y][x] = EMPTY
        robot = (x + dx, y + dy)

total = 0
for y in range(len(map)):
    for x in range(len(map[0])):
        if map[y][x] == BOX:
            total += gps_coord(x, y)

print(total)
