import sys
from collections import deque

import pygame

from astar import a_star_search
from bfs import bfs_search

ROWS, COLS, SIZE, TOP = 15, 25, 32, 50
W, H = 800, 500
STEPS_PER_FRAME = 2


BG, GRID_LINE = (0, 0, 0), (160, 160, 160)
WALL = (70, 70, 70)                    
START, GOAL = (46, 158, 68), (217, 48, 37)
VISITED, PATH = (143, 208, 245), (255, 193, 7)
BTN, BTN_TEXT = (255, 255, 255), (20, 20, 20)
GREEN, WHITE = (46, 158, 68), (255, 255, 255)


ALGORITHMS = {"astar": a_star_search, "bfs": bfs_search}

BUTTONS = [
    ("wall", "Wall"), ("weight", "Weight"), ("start", "Start"), ("goal", "Goal"),
    ("astar", "A*"), ("bfs", "BFS"),
    ("clear", "Clear"),
]


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("Maze Solver")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 16)
        self.small = pygame.font.SysFont("arial", 12)

       
        self.grid = [[1] * COLS for _ in range(ROWS)]
        self.start, self.goal = (1, 1), (13, 23)
        self.tool = "wall"
        self.algo = None         
        self.paint = None

        self.visited = set()
        self.queue = deque()
        self.pending_path = []
        self.path = []

        self.buttons = {}
        x = 8
        for key, _ in BUTTONS:
            self.buttons[key] = pygame.Rect(x, 8, 80, 34)
            x += 88

    def cell_at(self, pos):
        x, y = pos
        y -= TOP
        if y < 0:
            return None
        r, c = y // SIZE, x // SIZE
        return (r, c) if 0 <= r < ROWS and 0 <= c < COLS else None

    def apply(self, cell, first):
        r, c = cell
        if cell in (self.start, self.goal):
            return
        if self.tool == "wall":
            if first:
                self.paint = 1 if self.grid[r][c] == 0 else 0
            self.grid[r][c] = self.paint
        elif first and self.grid[r][c] != 0:
            if self.tool == "weight":
                self.grid[r][c] = {1: 3, 3: 5, 5: 9, 9: 1}.get(self.grid[r][c], 1)
            elif self.tool == "start":
                self.start = cell
            elif self.tool == "goal":
                self.goal = cell

    def animate(self, visited, path):
        self.clear_result()
        self.queue = deque(visited)
        self.pending_path = list(path)

    def run_algorithm(self, name):
        self.algo = name
        visited, path, cost = ALGORITHMS[name](self.grid, self.start, self.goal)
        self.animate(visited, path)

    def clear_result(self):
        self.visited.clear()
        self.queue.clear()
        self.pending_path = []
        self.path = []

    def update(self):
        for _ in range(STEPS_PER_FRAME):
            if self.queue:
                self.visited.add(self.queue.popleft())
            elif self.pending_path:
                self.path, self.pending_path = self.pending_path, []

    def color_of(self, r, c):
        cell = (r, c)
        if cell == self.start:
            return START
        if cell == self.goal:
            return GOAL
        if self.grid[r][c] == 0:
            return WALL
        if cell in self.path:
            return PATH
        if cell in self.visited:
            return VISITED
        w = self.grid[r][c]
        if w == 1:
            return WHITE
        t = min(w, 9) / 9             
        return (255, int(255 - 90 * t), int(255 - 180 * t))

    def draw(self):
        self.screen.fill(BG)

        for key, label in BUTTONS:
            rect = self.buttons[key]
            active = key == self.tool or key == self.algo
            pygame.draw.rect(self.screen, GREEN if active else BTN, rect, border_radius=12)
            text = self.font.render(label, True, WHITE if active else BTN_TEXT)
            self.screen.blit(text, text.get_rect(center=rect.center))

        for r in range(ROWS):
            for c in range(COLS):
                rect = pygame.Rect(c * SIZE, TOP + r * SIZE, SIZE, SIZE)
                pygame.draw.rect(self.screen, self.color_of(r, c), rect)
                pygame.draw.rect(self.screen, GRID_LINE, rect, 1)
                if self.grid[r][c] > 1:
                    t = self.small.render(str(self.grid[r][c]), True, (0, 0, 0))
                    self.screen.blit(t, t.get_rect(center=rect.center))
        pygame.display.flip()

    def on_click(self, pos):
        for key, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if key in ALGORITHMS:
                    self.run_algorithm(key)
                elif key == "clear":
                    self.clear_result()
                    self.algo = None
                else:
                    self.tool = key
                return False          
        cell = self.cell_at(pos)
        if cell:
            self.apply(cell, first=True)
            return True
        return False

    def run(self):
        dragging = False
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    dragging = self.on_click(e.pos)
                elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                    dragging = False
                elif e.type == pygame.MOUSEMOTION and dragging and self.tool == "wall":
                    cell = self.cell_at(e.pos)
                    if cell:
                        self.apply(cell, first=False)
            self.update()
            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    App().run()