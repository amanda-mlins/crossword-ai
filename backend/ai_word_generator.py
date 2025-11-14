# backend/ai_word_generator.py
from openai import OpenAI
import json
client = OpenAI()

def get_words_by_theme(theme, num_words=10, test=0):
   if test :
        result = {
            "ZON" : {"word":"ZON","clue":"De ster in ons zonnestelsel."},
            "STRAND" : {"word":"STRAND","clue":"Plaats waar je zand en zee vindt."},
            "VAKANTIE" : {"word":"VAKANTIE","clue":"Tijd om te ontspannen en te reizen."}
        }
        words = list(result.keys())
        return words, result
   else :
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
            "word": item["word"].upper()
        }
        for item in json_result
    }

    # print(result)

    words = list(result.keys())
    return words, result