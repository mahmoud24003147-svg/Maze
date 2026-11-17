from collections import deque


def bfs_search(grid, src, dest):
    rows, cols = len(grid), len(grid[0])
    src, dest = tuple(src), tuple(dest)

    if grid[src[0]][src[1]] == 0 or grid[dest[0]][dest[1]] == 0:
        return [], [], None
    if src == dest:
        return [src], [src], 0

    queue = deque([src])
    parent = {src: None}
    visited = []

    while queue:
        r, c = queue.popleft()
        visited.append((r, c))

        if (r, c) == dest:
            path = []
            curr = dest
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            cost = sum(grid[pr][pc] for pr, pc in path[1:])
            return visited, path, cost

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 0:
                if (nr, nc) not in parent:
                    parent[(nr, nc)] = (r, c)
                    queue.append((nr, nc))

    return visited, [], None