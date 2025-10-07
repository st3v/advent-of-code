from sys import argv
import re
import sys
import termios
import tty
import time
import os


def wait_for_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def print_map(
    robots: list[tuple[tuple[int, int], tuple[int, int]]], width: int, height: int
) -> bool:
    map = [[" "] * width for _ in range(height)]
    for (x, y), _ in robots:
        map[y][x] = "+"

    bottom = False
    for i, row in enumerate(map):
        line = "".join(row)
        if "+" * 10 in line:
            bottom = True
        print(line)

    return bottom


def move(
    pos: tuple[int, int],
    steps_per_second: tuple[int, int],
    seconds: int,
    height: int,
    width: int,
) -> tuple[int, int]:
    x, y = pos
    dx, dy = steps_per_second
    ty = (y + dy * seconds) % height
    tx = (x + dx * seconds) % width
    return (tx, ty)


robots: list[tuple[tuple[int, int], tuple[int, int]]] = []
with open(argv[1], "r") as file:
    for line in file:
        parts = re.findall(
            "p=([0-9]*)\\,([0-9]*)\\sv=([\\-{0,1}0-9]*)\\,([\\-{0,1}0-9]*)",
            line.strip(),
        )

        if not parts or len(parts[0]) != 4:
            continue

        robots.append(
            ((int(parts[0][0]), int(parts[0][1])), (int(parts[0][2]), int(parts[0][3])))
        )

h, w = 103, 101
seconds = 100000

step = 0
for _ in range(seconds):
    step += 1
    for i, (pos, steps) in enumerate(robots):
        x, y = move(pos, steps, 1, h, w)
        robots[i] = ((x, y), steps)
    os.system("cls" if os.name == "nt" else "clear")
    print("-" * 101)
    wait = print_map(robots, w, h)
    print("-" * 101)
    print(f"Step {step}")
    # time.sleep(1)
    if wait:
        print("Press any key to continue...")
        key = wait_for_key()
        if key == "q":
            sys.exit()
