# backend/ai_word_generator.py
from openai import OpenAI
client = OpenAI()

def get_words_by_theme(theme, num_words=10):
    prompt = f"Generate {num_words} simple English words related to the theme '{theme}'. Return only a comma-separated list."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    words = response.choices[0].message.content.strip()
    return [w.strip() for w in words.split(",")]

