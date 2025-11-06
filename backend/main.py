# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crossword_generator import create_crossword
from ai_word_generator import get_words_by_theme

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/generate")
def generate_crossword(theme: str = None):
    if theme:
        words = get_words_by_theme(theme)
    else:
        words = ["python", "api", "crossword", "puzzle", "ai", "grid"]

    grid, placed_words = create_crossword(words)
    return {"grid": grid, "words": placed_words, "theme": theme}

