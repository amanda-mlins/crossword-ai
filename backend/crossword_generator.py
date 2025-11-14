import itertools,random

class CrosswordSolver:
    def __init__(self, words, clues, size=15):
        self.words = [w.upper() for w in words]
        self.clues = clues
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.best_grid = None
        self.best_score = -1
        self.best_positions = []

        # Precompute all intersections
        self.intersections = self._compute_intersections()

    def _compute_intersections(self):
        """Find all letter overlaps between any two words."""
        inter = {}
        for w1, w2 in itertools.permutations(self.words, 2):
            key = (w1, w2)
            inter[key] = []
            for i, c1 in enumerate(w1):
                for j, c2 in enumerate(w2):
                    if c1 == c2:
                        inter[key].append((i, j))
        return inter

    def _can_place(self, word, row, col, direction):
        """Validate a word placement."""
        n = len(word)
        for i, ch in enumerate(word):
            r = row + (i if direction == "V" else 0)
            c = col + (i if direction == "H" else 0)
            if not (0 <= r < self.size and 0 <= c < self.size):
                return False
            cur = self.grid[r][c]
            if cur != ' ' and cur != ch:
                return False
        return True

    def _place(self, word, row, col, direction):
        """Place word on grid."""
        for i, ch in enumerate(word):
            r = row + (i if direction == "V" else 0)
            c = col + (i if direction == "H" else 0)
            self.grid[r][c] = ch

    def _remove(self, word, row, col, direction):
        """Remove word from grid (for backtracking)."""
        for i, ch in enumerate(word):
            r = row + (i if direction == "V" else 0)
            c = col + (i if direction == "H" else 0)
            # Recompute cell if another word overlaps here
            self.grid[r][c] = ' '
            for w, rr, cc, d in self.placed:
                for k, ch2 in enumerate(w):
                    rr2 = rr + (k if d == "V" else 0)
                    cc2 = cc + (k if d == "H" else 0)
                    if rr2 == r and cc2 == c:
                        self.grid[r][c] = ch2

    def _score_grid(self):
        """Count intersections in current grid."""
        score = 0
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != ' ':
                    count = 0
                    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                        rr, cc = r+dr, c+dc
                        if 0 <= rr < self.size and 0 <= cc < self.size and self.grid[rr][cc] != ' ':
                            count += 1
                    if count >= 2:  # intersection point
                        score += 1
        return score

    def solve(self):
        """Main recursive solver."""
        self.placed = []
        first = self.words[0]
        start_row = self.size // 2
        start_col = (self.size - len(first)) // 2
        self._place(first, start_row, start_col, "H")
        self.placed.append((first, start_row, start_col, "H"))
        self._search(self.words[1:])
        return self.best_grid, self.best_positions, self.best_score

    def _search(self, remaining):
        if not remaining:
            score = self._score_grid()
            if score > self.best_score:
                self.best_score = score
                self.best_grid = [row[:] for row in self.grid]
                self.best_positions = self.placed[:]
            return

        word = remaining[0]
        best_local_score = 0
        placed_any = False

        for existing in self.placed:
            w2, r2, c2, d2 = existing
            for (i1, i2) in self.intersections.get((word, w2), []):
                if d2 == "H":
                    # new word vertical
                    row = r2 - i1
                    col = c2 + i2
                    direction = "V"
                else:
                    # new word horizontal
                    row = r2 + i2
                    col = c2 - i1
                    direction = "H"

                if self._can_place(word, row, col, direction):
                    self._place(word, row, col, direction)
                    self.placed.append((word, row, col, direction))
                    self._search(remaining[1:])
                    self.placed.pop()
                    self._remove(word, row, col, direction)
                    placed_any = True

        # fallback random placement if no intersection possible
        if not placed_any:
            for _ in range(100):
                d = random.choice(["H","V"])
                row = random.randint(0, self.size - (len(word) if d == "V" else 1))
                col = random.randint(0, self.size - (len(word) if d == "H" else 1))
                if self._can_place(word, row, col, d):
                    self._place(word, row, col, d)
                    self.placed.append((word, row, col, d))
                    self._search(remaining[1:])
                    self.placed.pop()
                    self._remove(word, row, col, d)
                    break

def create_crossword(words, clues, grid_size=15):
    solver = CrosswordSolver(words, clues, size=grid_size)
    grid, positions, score = solver.solve()
    return grid, positions

def grid_to_display(grid):
    return [[cell if cell != ' ' else '' for cell in row] for row in grid]

