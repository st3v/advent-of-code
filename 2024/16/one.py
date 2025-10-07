from sys import argv
import heapq


def read_maze(path: str) -> tuple[list[list[str]], tuple[int, int], tuple[int, int]]:
    maze: list[list[str]] = []
    start: tuple[int, int] = (-1, -1)
    end: tuple[int, int] = (-1, -1)

    with open(path, "r") as file:
        for i, line in enumerate(file):
            line = line.strip()

            if (s := line.find("S")) >= 0:
                start = (i, s)

            if (e := line.find("E")) >= 0:
                end = (i, e)

            maze.append(list(line))

    assert start != (-1, -1) and end != (-1, -1)

    return (maze, start, end)


def turn_cost(current: str, next: str) -> int:
    dirs = [">", "v", "<", "^"]
    c, n = dirs.index(current), dirs.index(next)
    return min((c - n) % 4, (n - c) % 4) * 1000


DIRECTIONS = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}

maze, start, end = read_maze(argv[1])
visited: dict[tuple[int, int], int] = {}
to_visit: list[tuple[int, int, int, str]] = [(0, *start, ">")]

while to_visit:
    cost, x, y, dir = heapq.heappop(to_visit)
    visited[(x, y)] = cost

    if maze[x][y] == "#":
        continue

    if (x, y) == end:
        continue

    for ndir, (dx, dy) in DIRECTIONS.items():
        nx, ny = x + dx, y + dy
        ncost = cost + turn_cost(dir, ndir) + 1
        if (nx, ny) not in visited or visited[(nx, ny)] > ncost:
            heapq.heappush(to_visit, (ncost, nx, ny, ndir))

print(visited[end])
