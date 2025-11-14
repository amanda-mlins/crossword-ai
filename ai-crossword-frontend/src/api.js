import axios from "axios";

const API_BASE = "http://127.0.0.1:8000"; // Change if backend URL differs

export async function generateCrossword(words, theme = "") {
  try {
    const res = await axios.post(`${API_BASE}/generate`, {
      words,
      theme
    });
    return res.data;
  } catch (err) {
    console.error("API Error:", err);
    throw err;
  }
}

