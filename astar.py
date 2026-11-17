import heapq


class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0


def calculate_h_value(row, col, dest):
    return abs(row - dest[0]) + abs(col - dest[1])


def trace_path(cell_details, dest):
    path = []
    row, col = dest
    while not (cell_details[row][col].parent_i == row
               and cell_details[row][col].parent_j == col):
        path.append((row, col))
        row, col = cell_details[row][col].parent_i, cell_details[row][col].parent_j
    path.append((row, col))
    path.reverse()
    return path


def a_star_search(grid, src, dest):
    ROW, COL = len(grid), len(grid[0])
    src, dest = tuple(src), tuple(dest)

    def is_valid(r, c):
        return 0 <= r < ROW and 0 <= c < COL

    if grid[src[0]][src[1]] == 0 or grid[dest[0]][dest[1]] == 0:
        return [], [], None
    if src == dest:
        return [src], [src], 0

    closed_list = [[False] * COL for _ in range(ROW)]
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    i, j = src
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    open_list = [(0.0, i, j)]
    visited = []

    while open_list:
        _, i, j = heapq.heappop(open_list)

        if closed_list[i][j]:      
            continue
        closed_list[i][j] = True
        visited.append((i, j))

        if (i, j) == dest:
            return visited, trace_path(cell_details, dest), cell_details[i][j].g

        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + di, j + dj
            if is_valid(ni, nj) and grid[ni][nj] != 0 and not closed_list[ni][nj]:
                g_new = cell_details[i][j].g + grid[ni][nj]
                if g_new < cell_details[ni][nj].g:
                    h_new = calculate_h_value(ni, nj, dest)
                    f_new = g_new + h_new
                    heapq.heappush(open_list, (f_new, ni, nj))
                    cell_details[ni][nj].f = f_new
                    cell_details[ni][nj].g = g_new
                    cell_details[ni][nj].h = h_new
                    cell_details[ni][nj].parent_i = i
                    cell_details[ni][nj].parent_j = j

    return visited, [], None      


# if __name__ == "__main__":
#     grid = [
#         [1, 1, 9],
#         [1, 0, 1],
#         [1, 1, 1],
#     ]
    visited, path, cost = a_star_search(grid, (0, 0), (0, 2))
    print(visited)
    print(path, cost)