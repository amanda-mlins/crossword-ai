# backend/crossword_generator.py
import random

def create_crossword(words, grid_size=15):
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    placed_words = []

    for word in words:
        word = word.upper()
        placed = False
        for _ in range(100):  # Try up to 100 times to place a word
            direction = random.choice(['H', 'V'])
            if direction == 'H':
                row = random.randint(0, grid_size - 1)
                col = random.randint(0, grid_size - len(word))
                if all(grid[row][col + i] in (' ', word[i]) for i in range(len(word))):
                    for i in range(len(word)):
                        grid[row][col + i] = word[i]
                    placed_words.append((word, row, col, direction))
                    placed = True
                    break
            else:
                row = random.randint(0, grid_size - len(word))
                col = random.randint(0, grid_size - 1)
                if all(grid[row + i][col] in (' ', word[i]) for i in range(len(word))):
                    for i in range(len(word)):
                        grid[row + i][col] = word[i]
                    placed_words.append((word, row, col, direction))
                    placed = True
                    break
        if not placed:
            print(f"Couldn't place {word}")
    return grid, placed_words


def display_crossword(grid):
    return "\n".join(" ".join(row) for row in grid)

