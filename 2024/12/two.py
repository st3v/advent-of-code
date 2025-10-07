from sys import argv
from collections import deque, defaultdict


def on_map(x: int, y: int, h: int, w: int) -> bool:
    return 0 <= x < h and 0 <= y < w


def val_or_none(x: int, y: int, cells: list[list[str]]) -> str | None:
    if not on_map(x, y, len(cells), len(cells[0])):
        return None
    return cells[x][y]


def count_corners(x: int, y: int, cells: list[list[str]]) -> int:
    this = cells[x][y]
    corners = 0

    for dx1, dy1, dx2, dy2 in [
        (-1, 0, 0, -1),  # top-left
        (-1, 0, 0, 1),  # top-right
        (1, 0, 0, -1),  # bottom-left
        (1, 0, 0, 1),  # bottom-right
    ]:
        n1 = (x + dx1, y + dy1)
        n2 = (x + dx2, y + dy2)
        n3 = (x + dx1 + dx2, y + dy1 + dy2)

        # outer corner
        if this != val_or_none(*n1, cells) and this != val_or_none(*n2, cells):
            corners += 1

        # inner corner
        if (
            this == val_or_none(*n1, cells)
            and this == val_or_none(*n2, cells)
            and this != val_or_none(*n3, cells)
        ):
            corners += 1

    return corners


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
    corners = count_corners(x, y, cells)
    h, w = len(cells), len(cells[0])

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if on_map(nx, ny, h, w):
            if cells[nx][ny] != cells[x][y]:
                queue.append((nx, ny))
            else:
                a, s = visit((nx, ny), cells, queue, visited)
                area += a
                corners += s

    return (area, corners)


cells: list[list[str]] = []
with open(argv[1], "r") as file:
    for line in file:
        cells.append(list(line.strip()))

visited: dict[tuple[int, int], bool] = defaultdict(bool)
queue = deque([(0, 0)])

total = 0
while queue:
    pos = queue.popleft()
    area, corners = visit(pos, cells, queue, visited)
    total += area * corners

print(total)
