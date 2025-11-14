import random
from typing import List, Tuple, Dict

class Crossword:
    def __init__(self, size: int = 15):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.placed_words = []

    def create_crossword(self, words: List[str]) -> Tuple[List[List[str]], List[Dict]]:
        words = [w.upper() for w in sorted(words, key=lambda x: -len(x))]  # longest first

        # Place first word in the center
        first_word = words[0]
        start_row = self.size // 2
        start_col = (self.size - len(first_word)) // 2
        self._place_word(first_word, start_row, start_col, "H")
        self.placed_words.append({"word": first_word, "row": start_row, "col": start_col, "dir": "H"})

        open_slots = self._get_open_slots(first_word, start_row, start_col, "H")

        for word in words[1:]:
            candidates = self._find_candidates(word, open_slots)
            if candidates:
                # Pick the candidate with maximum overlap
                candidates.sort(key=lambda x: -x["overlaps"])
                best = candidates[0]
                self._place_word(word, best["row"], best["col"], best["dir"])
                self.placed_words.append({"word": word, "row": best["row"], "col": best["col"], "dir": best["dir"]})
                open_slots = self._update_open_slots(open_slots, word, best)
            else:
                # Fallback: place randomly near center
                placed = False
                for _ in range(50):
                    direction = random.choice(["H", "V"])
                    row = random.randint(0, self.size - (len(word) if direction == "V" else 1))
                    col = random.randint(0, self.size - (len(word) if direction == "H" else 1))
                    if self._can_place(word, row, col, direction):
                        self._place_word(word, row, col, direction)
                        self.placed_words.append({"word": word, "row": row, "col": col, "dir": direction})
                        open_slots = self._update_open_slots(open_slots, word,
                                                             {"row": row, "col": col, "dir": direction})
                        placed = True
                        break
                if not placed:
                    print(f"Could not place word: {word}")

        return self.grid, self.placed_words

    # -------------------------- Core Logic --------------------------
    def _get_open_slots(self, word, row, col, direction):
        slots = []
        for i, ch in enumerate(word):
            r = row + (i if direction == "V" else 0)
            c = col + (i if direction == "H" else 0)
            slots.append({"row": r, "col": c, "char": ch})
        return slots

    def _update_open_slots(self, open_slots, word, placement):
        new_slots = self._get_open_slots(word, placement["row"], placement["col"], placement["dir"])
        # Avoid duplicates
        for slot in new_slots:
            if slot not in open_slots:
                open_slots.append(slot)
        return open_slots

    def _find_candidates(self, word, open_slots):
        candidates = []
        for i, ch1 in enumerate(word):
            for slot in open_slots:
                if ch1 == slot["char"]:
                    # Determine placement
                    if slot.get("dir") == "H":  # existing horizontal → new vertical
                        row = slot["row"] - i
                        col = slot["col"]
                        direction = "V"
                    else:  # default: vertical or unknown → horizontal
                        row = slot["row"]
                        col = slot["col"] - i
                        direction = "H"

                    if self._can_place(word, row, col, direction):
                        overlaps = self._count_overlaps(word, row, col, direction)
                        candidates.append({"row": row, "col": col, "dir": direction, "overlaps": overlaps})
        return candidates

    def _can_place(self, word, row, col, direction):
        for i, ch in enumerate(word):
            r = row + (i if direction == "V" else 0)
            c = col + (i if direction == "H" else 0)

            if not (0 <= r < self.size and 0 <= c < self.size):
                return False

            cell = self.grid[r][c]
            if cell != ' ' and cell != ch:
                return False

            # adjacency check (side neighbors)
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                rr, cc = r+dr, c+dc
                if 0 <= rr < self.size and 0 <= cc < self.size:
                    neighbor = self.grid[rr][cc]
                    if neighbor != ' ' and neighbor != ch:
                        return False
        return True

    def _place_word(self, word, row, col, direction):
        for i, ch in enumerate(word):
            r = row + (i if direction == "V" else 0)
            c = col + (i if direction == "H" else 0)
            self.grid[r][c] = ch

    def _count_overlaps(self, word, row, col, direction):
        count = 0
        for i, ch in enumerate(word):
            r = row + (i if direction == "V" else 0)
            c = col + (i if direction == "H" else 0)
            if 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == ch:
                count += 1
        return count

# -------------------- External Interface --------------------
def create_crossword(words: List[str], grid_size: int = 15):
    solver = Crossword(grid_size)
    return solver.create_crossword(words)

def grid_to_display(grid):
    return [[cell if cell != ' ' else '' for cell in row] for row in grid]

# -------------------- Test --------------------
if __name__ == "__main__":
    words = ["cat", "back", "stack", "attack", "track", "dog", "fish", "rat"]
    grid, positions = create_crossword(words, grid_size=15)
    for row in grid:
        print(' '.join(cell if cell != ' ' else '.' for cell in row))
