import random
from typing import List, Tuple, Optional

class Crossword:
    def __init__(self, size: int = 15):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.placed_words = []  # List of dicts with word, row, col, dir

    def place_words(self, words: List[str]):
        words = [w.upper() for w in words]
        words.sort(key=lambda w: -len(w))  # longest first

        # Place first word in center horizontally
        first = words[0]
        start_row = self.size // 2
        start_col = (self.size - len(first)) // 2
        self._place_word(first, start_row, start_col, "H")
        self.placed_words.append({"word": first, "row": start_row, "col": start_col, "dir": "H"})

        # Place the rest
        for word in words[1:]:
            best = self._find_best_position(word)
            if best:
                row, col, direction = best
                self._place_word(word, row, col, direction)
                self.placed_words.append({"word": word, "row": row, "col": col, "dir": direction})
            else:
                # fallback random placement if nothing fits
                self._try_random_place(word)

        return self.grid, self.placed_words

    # ----------------------------------------------------------------
    # Core placement logic
    # ----------------------------------------------------------------
    def _find_best_position(self, word: str) -> Optional[Tuple[int, int, str]]:
        best_score = 0
        best_pos = None
        for placed in self.placed_words:
            w2, row2, col2, dir2 = placed["word"], placed["row"], placed["col"], placed["dir"]
            # Try intersecting every matching letter
            for i, ch1 in enumerate(word):
                for j, ch2 in enumerate(w2):
                    if ch1 == ch2:
                        # propose intersection
                        if dir2 == "H":  # then new word is vertical
                            new_row = row2 - i
                            new_col = col2 + j
                            pos = (new_row, new_col, "V")
                        else:  # existing is vertical → new is horizontal
                            new_row = row2 + j
                            new_col = col2 - i
                            pos = (new_row, new_col, "H")

                        if self._can_place(word, pos[0], pos[1], pos[2]):
                            score = self._score_position(word, pos[0], pos[1], pos[2])
                            if score > best_score:
                                best_score = score
                                best_pos = pos
        return best_pos

    def _score_position(self, word: str, row: int, col: int, direction: str) -> int:
        """Score based on number of intersections created."""
        score = 0
        for i, ch in enumerate(word):
            r, c = (row + i, col) if direction == "V" else (row, col + i)
            if 0 <= r < self.size and 0 <= c < self.size:
                if self.grid[r][c] == ch:
                    score += 1
        return score

    def _can_place(self, word: str, row: int, col: int, direction: str) -> bool:
        """Check if a word can be placed without conflicts or adjacency errors."""
        for i, ch in enumerate(word):
            r, c = (row + i, col) if direction == "V" else (row, col + i)
            # Out of bounds
            if not (0 <= r < self.size and 0 <= c < self.size):
                return False
            # Conflict
            cell = self.grid[r][c]
            if cell != ' ' and cell != ch:
                return False

            # Optional: Check adjacency to avoid touching sides
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                rr, cc = r + dr, c + dc
                if 0 <= rr < self.size and 0 <= cc < self.size:
                    neighbor = self.grid[rr][cc]
                    if neighbor != ' ' and neighbor != ch:
                        # Allow vertical adjacency if it's the intersection itself
                        if not (cell == ch):
                            return False
        return True

    def _place_word(self, word: str, row: int, col: int, direction: str):
        for i, ch in enumerate(word):
            r, c = (row + i, col) if direction == "V" else (row, col + i)
            self.grid[r][c] = ch

    def _try_random_place(self, word: str):
        for _ in range(200):
            direction = random.choice(["H", "V"])
            row = random.randint(0, self.size - (len(word) if direction == "V" else 1))
            col = random.randint(0, self.size - (len(word) if direction == "H" else 1))
            if self._can_place(word, row, col, direction):
                self._place_word(word, row, col, direction)
                self.placed_words.append({"word": word, "row": row, "col": col, "dir": direction})
                return True
        return False

def create_crossword(words: List[str], grid_size: int = 15):
    c = Crossword(grid_size)
    return c.place_words(words)

def grid_to_display(grid):
    return [[cell if cell != ' ' else '' for cell in row] for row in grid]

