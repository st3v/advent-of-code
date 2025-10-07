from sys import argv
import heapq


def read(path):
    drops = []
    with open(path, "r") as file:
        for line in file:
            x, y = line.strip().split(",")
            drops.append((int(x), int(y)))
    return drops


def path_len(sp, end):
    res = -1
    while end in sp:
        res += 1
        nx, ny, _ = sp[end]
        end = (nx, ny)
    return res


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
            return path_len(sp, end)

        for dy, dx in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                if (nx, ny) not in sp or sp[(nx, ny)][2] > length + 1:
                    heapq.heappush(pq, (length + 1, nx, ny, x, y))

    return -1


drops = read(argv[1])
n = int(argv[2]) + 1
num_bytes = int(argv[3])
start, end = (0, 0), (n - 1, n - 1)

grid = [["."] * n for _ in range(n)]
for i in range(num_bytes):
    x, y = drops[i]
    grid[y][x] = "#"

print(find_path(grid, start, end))
