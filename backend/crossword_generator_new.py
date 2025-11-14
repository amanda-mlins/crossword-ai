import random

class CrosswordSolver:
    """
    Crossword solver using a heuristic approach:
    - Places longest words first
    - First word in the center
    - Uses letter-to-position map for intersections
    - Scores candidate positions based on intersections
    """

    def __init__(self, words, clues, size=15):
        """
        Initialize the crossword solver.

        Args:
            words (list[str]): List of words to place
            clues (dict): Dictionary of clues (used for later reference)
            size (int): Size of the grid (size x size)
        """
        self.words = [w.upper() for w in words]
        self.clues = clues
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.placed = []  # Stores tuples (word, row, col, direction)
        self.letter_positions = {}  # Map letters to grid positions for fast intersection lookup

        # Sort words longest first for better placement
        self.words.sort(key=len, reverse=True)

    def _can_place(self, word, row, col, direction):
        """
        Check if a word can be placed at a given position.

        Args:
            word (str): Word to place
            row (int): Starting row
            col (int): Starting column
            direction (str): 'H' for horizontal, 'V' for vertical

        Returns:
            bool: True if placement is valid
        """
        for i, ch in enumerate(word):
            r = row + (i if direction == 'V' else 0)
            c = col + (i if direction == 'H' else 0)
            if not (0 <= r < self.size and 0 <= c < self.size):
                return False
            cur = self.grid[r][c]
            if cur != ' ' and cur != ch:
                return False
        return True

    def _place_word(self, word, row, col, direction):
        """
        Place a word on the grid and update the letter positions map.

        Args:
            word (str): Word to place
            row (int): Starting row
            col (int): Starting column
            direction (str): 'H' or 'V'
        """
        for i, ch in enumerate(word):
            r = row + (i if direction == 'V' else 0)
            c = col + (i if direction == 'H' else 0)
            self.grid[r][c] = ch
            self.letter_positions.setdefault(ch, []).append((r, c))
        self.placed.append((word, row, col, direction))

    def _score_position(self, word, row, col, direction):
        """
        Compute score for a candidate placement based on intersections.

        Args:
            word (str): Word to score
            row (int): Starting row
            col (int): Starting column
            direction (str): 'H' or 'V'

        Returns:
            int: Number of intersecting letters
        """
        score = 0
        for i, ch in enumerate(word):
            r = row + (i if direction == 'V' else 0)
            c = col + (i if direction == 'H' else 0)
            if self.grid[r][c] == ch:
                score += 1
        return score

    def solve(self):
        """
        Solve the crossword by placing all words.

        Returns:
            grid (list[list[str]]): Completed grid
            placed (list[tuple]): List of placed words with positions and directions
        """
        if not self.words:
            return self.grid, self.placed

        # Place the first word in the center horizontally
        first_word = self.words[0]
        start_row = self.size // 2
        start_col = (self.size - len(first_word)) // 2
        self._place_word(first_word, start_row, start_col, "H")

        # Place remaining words
        for word in self.words[1:]:
            candidates = []

            # Find potential intersections based on letters
            for i, ch in enumerate(word):
                for r, c in self.letter_positions.get(ch, []):
                    for direction in ['H', 'V']:
                        row = r - i if direction == 'V' else r
                        col = c - i if direction == 'H' else c
                        if self._can_place(word, row, col, direction):
                            score = self._score_position(word, row, col, direction)
                            candidates.append((score, row, col, direction))

            # Sort by score descending (max intersections first)
            candidates.sort(key=lambda x: x[0], reverse=True)

            placed = False
            for score, row, col, direction in candidates[:5]:  # try top 5
                self._place_word(word, row, col, direction)
                placed = True
                break

            # Fallback random placement if no intersections found
            if not placed:
                for _ in range(50):
                    direction = random.choice(['H', 'V'])
                    row = random.randint(0, self.size - (len(word) if direction == 'V' else 1))
                    col = random.randint(0, self.size - (len(word) if direction == 'H' else 1))
                    if self._can_place(word, row, col, direction):
                        self._place_word(word, row, col, direction)
                        break

        return self.grid, self.placed


def create_crossword(words, clues, grid_size=15):
    """
    Helper function to generate a crossword grid and positions.

    Args:
        words (list[str]): List of words
        clues (dict): Dictionary of clues
        grid_size (int): Grid size

    Returns:
        grid (list[list[str]]), positions (list[tuple])
    """
    solver = CrosswordSolver(words, clues, size=grid_size)
    grid, positions = solver.solve()
    return grid, positions


def grid_to_display(grid):
    """
    Convert internal grid to display-friendly format.

    Empty spaces become ''.
    """
    return [[cell if cell != ' ' else '' for cell in row] for row in grid]
