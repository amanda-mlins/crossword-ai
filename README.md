# AI based crossword puzzle
A simple project to learn more about:
- AI prompting and integrating it to an application: 
  - ChatGPT helped me generate the base code and a lot of hints and debugging since I was not that familiar with Python and Vue.js
  - The application asks AI (Open API) for words and the clues
- Python backend: Fast API
- Vue.js as the frontend framework
- Dutch (crossword puzzle is generated in Dutch, a language I am learning :) )

![image](screenshot.png)

### How to run the Python backend
Make sure you have the correct OPENAI_API_KEY in your environment
```
cd backend
```
```

uvicorn main:app --reload
```

### How to run the Vue.js frontend
```
cd ai-crossword-frontend
```
```
npm run dev
```
