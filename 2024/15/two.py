from sys import argv
import re

WALL = "#"
EMPTY = "."
ROBOT = "@"
BOX = "["

delta = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1),
}


def gps_coord(x: int, y: int) -> int:
    return 100 * y + x


def print_map(map: list[list[str]]):
    valid = True
    for row in map:
        line = "".join(row)
        if re.findall("\\[[\\.\\@O#\\[]", line):
            valid = False
        print(line)
    return valid


def can_move_to(
    sym: str, prev_x: int, x: int, y: int, dir: str, map: list[list[str]]
) -> bool:
    if map[y][x] == WALL:
        return False

    if map[y][x] == EMPTY:
        return True

    dx, dy = delta[dir]

    if dir in ["^", "v"]:
        if map[y][x] == "[" and prev_x != x + 1:
            left = can_move_to(map[y][x], x, x + dx, y + dy, dir, map)
            right = can_move_to(map[y][x + 1], x + 1, x + 1 + dx, y + dy, dir, map)
            return left and right
        elif map[y][x] == "]" and prev_x != x - 1:
            right = can_move_to(map[y][x], x, x + dx, y + dy, dir, map)
            left = can_move_to(map[y][x - 1], x - 1, x - 1 + dx, y + dy, dir, map)
            return left and right

    return can_move_to(map[y][x], x, x + dx, y + dy, dir, map)


def do_move_to(sym: str, x: int, y: int, dir: str, map: list[list[str]]) -> bool:
    if not can_move_to(sym, x, x, y, dir, map):
        return False

    if map[y][x] == EMPTY:
        map[y][x] = sym
        return True

    dx, dy = delta[dir]

    if dir in ["^", "v"]:
        if map[y][x] == "[":
            do_move_to(map[y][x], x + dx, y + dy, dir, map)
            do_move_to(map[y][x + 1], x + 1 + dx, y + dy, dir, map)
            map[y][x + 1] = EMPTY
            map[y][x] = sym
            return True
        elif map[y][x] == "]":
            do_move_to(map[y][x], x + dx, y + dy, dir, map)
            do_move_to(map[y][x - 1], x - 1 + dx, y + dy, dir, map)
            map[y][x - 1] = EMPTY
            map[y][x] = sym
            return True

    do_move_to(map[y][x], x + dx, y + dy, dir, map)
    map[y][x] = sym
    return True


moves: list[str] = []
map: list[list[str]] = []
robot: tuple[int, int] = (-1, -1)

with open(argv[1], "r") as file:
    for line in file:
        line = line.strip()
        if line == "":
            continue

        if WALL in line:
            line = line.replace("#", "##")
            line = line.replace("O", "[]")
            line = line.replace(".", "..")
            line = line.replace("@", "@.")
            map.append(list(line))

            x = line.find(ROBOT)
            if x >= 0:
                robot = (x, len(map) - 1)

        else:
            moves.extend(list(line))

for dir in moves:
    dx, dy = delta[dir]
    x, y = robot
    if do_move_to(ROBOT, x + dx, y + dy, dir, map):
        map[y][x] = EMPTY
        robot = (x + dx, y + dy)

total = 0
for y in range(len(map)):
    for x in range(len(map[0])):
        if map[y][x] == BOX:
            total += gps_coord(x, y)


print(total)
