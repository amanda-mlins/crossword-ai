# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from crossword_generator import create_crossword, grid_to_display
from ai_word_generator import get_words_by_theme
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
class GenerateRequest(BaseModel):
    theme: Optional[str] = None
    words: Optional[List[str]] = None
    grid_size: Optional[int] = 15


@app.post("/generate")
async def generate(req: GenerateRequest):
    # Prefer explicit words if provided
    if req.words and len(req.words) > 0:
        words = req.words
        clues =  ["Clue for " + w for w in words]
    elif req.theme:
        try:
            words, clues = get_words_by_theme(req.theme, num_words=12)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI word generation failed: {e}")
    else:
        # default seed words
        words = ["cat", "dog", "turtle", "bird"]
        clues = ["Likes milk","Likes bones","Very slow", "Can fly"]

    # Normalize
    # words = [w.strip() for w in words if w and len(w.strip()) > 1]

    grid_size = max(9, min(25, req.grid_size or 15))
    grid, placed_words = create_crossword(words, clues, grid_size=grid_size)
    display = grid_to_display(grid)
    for (word, start, end, position) in placed_words :
        clues[word]["position"] = position
        clues[word]["start"] = start
        clues[word]["end"] = end

    return {
        "grid": display,
        "placed_words": placed_words,
        "words_requested": words,
        "clues": clues,
        "grid_size": grid_size,
        "theme": req.theme,
    }

