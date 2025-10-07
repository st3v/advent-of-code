from sys import argv
from collections import deque, defaultdict


def on_map(x: int, y: int, h: int, w: int) -> bool:
    return 0 <= x < h and 0 <= y < w


def visit(
    pos: tuple[int, int],
    cells: list[list[str]],
    queue: deque[tuple[int, int]],
    visited: dict[tuple[int, int], bool],
) -> tuple[int, int]:
    if visited[pos]:
        return (0, 0)

    visited[pos] = True
    x, y = pos
    area = 1
    perimeter = 0
    perimeter += 1 if x == 0 else 0
    perimeter += 1 if y == 0 else 0
    perimeter += 1 if x == len(cells) - 1 else 0
    perimeter += 1 if y == len(cells[0]) - 1 else 0

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if on_map(nx, ny, len(cells), len(cells[0])):
            if cells[nx][ny] != cells[x][y]:
                queue.append((nx, ny))
                perimeter += 1
            else:
                a, p = visit((nx, ny), cells, queue, visited)
                area += a
                perimeter += p

    return (area, perimeter)


cells: list[list[str]] = []
with open(argv[1], "r") as file:
    for line in file:
        cells.append(list(line.strip()))

visited: dict[tuple[int, int], bool] = defaultdict(bool)
queue = deque([(0, 0)])

total = 0
while queue:
    pos = queue.popleft()
    area, perimeter = visit(pos, cells, queue, visited)
    total += area * perimeter

print(total)
