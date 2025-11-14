# backend/ai_word_generator.py
from openai import OpenAI
import json
client = OpenAI()

def get_words_by_theme(theme, num_words=10):
    prompt = f"In order to help me build a crossword puzzle, generate {num_words} simple Dutch words related to the theme '{theme}'. Return only a plain json array (no line breaks, nothing besides the values asked) with words and a short clue (in Dutch) for them, the keys used in each object should be 'word' and 'clue'."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    #print(response.choices[0].message.content.strip())
    json_string = response.choices[0].message.content.strip()
    print(json_string)
    json_result = json.loads(json_string)
    result = {
        item["word"].upper(): {
            "clue": item["clue"],
        }
        for item in json_result
    }

    # print(result)
    #words = response.choices[0].message.content.strip()
    # words = "snow,ice,cold,freeze,chill,frost"
    words = list(result.keys())
    clues = []
    return words, result