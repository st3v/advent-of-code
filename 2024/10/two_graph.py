"""
Optimized solution for counting trail paths in a topographic map.

The original solution used DFS with full path tracking (visited set), which required
deep copying the visited state for each recursive call. This was very expensive.

This optimized solution uses dynamic programming with topological sorting:
1. Build a directed graph of valid moves (from height h to h+1)
2. Use topological sort to process nodes in dependency order
3. Accumulate path counts from trailheads (0s) to peaks (9s)
4. Sum all paths that end at peaks

Time Complexity: O(H*W) where H and W are height and width of the map
Space Complexity: O(H*W) for the graph and path count storage
"""

from sys import argv
from collections import defaultdict, deque


def on_map(row: int, col: int, height: int, width: int) -> bool:
    """Check if the coordinates are within the map bounds."""
    return 0 <= row < height and 0 <= col < width


def solve():
    # Read the topographic map
    topo = []
    with open(argv[1], "r") as file:
        for line in file:
            row = list(map(int, line.strip()))
            topo.append(row)

    height, width = len(topo), len(topo[0])

    # Build adjacency graph: which cells can be reached from each cell?
    # Only valid moves are to adjacent cells with height + 1
    graph = defaultdict(list)  # from (x,y) to [(nx,ny), ...]
    in_degree = defaultdict(int)  # count of incoming edges to each node

    # Find all trailheads (0s) and peaks (9s)
    trailheads = []
    peaks = set()

    for x in range(height):
        for y in range(width):
            if topo[x][y] == 0:
                trailheads.append((x, y))
            elif topo[x][y] == 9:
                peaks.add((x, y))

            # Check all 4 directions for valid transitions (current_height -> current_height + 1)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if on_map(nx, ny, height, width) and topo[nx][ny] == topo[x][y] + 1:
                    # Can move from (x,y) to (nx,ny)
                    graph[(x, y)].append((nx, ny))
                    in_degree[(nx, ny)] += 1

    # Initialize path counts: each trailhead starts with 1 path
    path_counts = defaultdict(int)
    for start_x, start_y in trailheads:
        path_counts[(start_x, start_y)] = 1

    # Process nodes in topological order using Kahn's algorithm
    queue = deque()
    # Start with nodes that have no incoming edges (trailheads and nodes not reachable from anything)
    for x in range(height):
        for y in range(width):
            if in_degree[(x, y)] == 0:
                queue.append((x, y))

    # Process the graph in topological order
    while queue:
        x, y = queue.popleft()

        # Propagate path counts to all valid next positions
        for nx, ny in graph[(x, y)]:
            path_counts[(nx, ny)] += path_counts[(x, y)]
            in_degree[(nx, ny)] -= 1

            # If all dependencies for (nx, ny) are processed, add to queue
            if in_degree[(nx, ny)] == 0:
                queue.append((nx, ny))

    # Sum the path counts for all peaks (9s)
    total = sum(path_counts[peak_pos] for peak_pos in peaks)

    print(total)


if __name__ == "__main__":
    solve()
