from sys import argv
import heapq


def read(path):
    drops = []
    with open(path, "r") as file:
        for line in file:
            x, y = line.strip().split(",")
            drops.append((int(x), int(y)))
    return drops


def build_path(sp, end):
    path = []
    while end in sp:
        path.append(end)
        nx, ny, _ = sp[end]
        end = (nx, ny)
    return path


def find_path(grid, start, end):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    pq = [(0, *start, -1, -1)]
    sp = {}

    while pq:
        length, x, y, px, py = heapq.heappop(pq)
        if grid[y][x] == "#" or (x, y) in sp:
            continue

        sp[(x, y)] = (px, py, length)
        if (x, y) == (end):
            return build_path(sp, end)

        for dy, dx in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                if (nx, ny) not in sp or sp[(nx, ny)][2] > length + 1:
                    heapq.heappush(pq, (length + 1, nx, ny, x, y))

    return None


drops = read(argv[1])
n = int(argv[2]) + 1
start, end = (0, 0), (n - 1, n - 1)
path = None
grid = [["."] * n for _ in range(n)]

for x, y in drops:
    grid[y][x] = "#"
    if not path or (x, y) in path:
        if not (path := find_path(grid, start, end)):
            print(f"{x},{y}")
            break
