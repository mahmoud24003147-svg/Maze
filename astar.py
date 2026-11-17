
import heapq

def a_star_search(grid, start, goal):

    rows = len(grid)
    cols = len(grid[0])

    def heuristic(pos):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    pq = [(heuristic(start), 0, start)]

    g_score = {start: 0}
    parent = {}    
    visited = []

    while pq:

        f, g, current = heapq.heappop(pq)
  
        if g != g_score.get(current):
            continue

        visited.append(current)

        if current == goal:
            path = [goal]

            while path[-1] != start:
                path.append(parent[path[-1]])

            path.reverse()

            return visited, path, g

        row, col = current

        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0)
        ]

        for dr, dc in directions:

            nr = row + dr
            nc = col + dc

            if 0 <= nr < rows and 0 <= nc < cols:

                if grid[nr][nc] != 0:

                    neighbor = (nr, nc)

                    new_g = g + grid[nr][nc]

                    if new_g < g_score.get(neighbor, float('inf')):

                        g_score[neighbor] = new_g
                        parent[neighbor] = current

                        new_f = new_g + heuristic(neighbor)

                        heapq.heappush(
                            pq,
                            (new_f, new_g, neighbor)
                        )

    return visited, [], None
