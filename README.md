# 🎓 Teach with Pod

**Teach with Pod** is an AI-powered classroom companion that helps educators flip their classroom using podcast episodes from Cabrera Lab.

Teachers describe their course and topic of interest, and the app suggests a podcast episode — along with a student question and a model answer key.

---

## ✨ Features

- 🔍 Accepts natural-language prompts about the course, topic, and grade level
- 🎧 Suggests a relevant podcast episode from your indexed library
- ❓ Generates a student-facing question based on the episode
- 🧠 Provides a teacher-facing model answer to support grading
- 🔁 Offers multiple alternative suggestions — including forcing a different episode
- 🎨 Clean and responsive UI with embedded video and rich formatting

---

## 🗈️ Example Use Case

> **Teacher Prompt**:  
> _“Public policy, masters level, focusing on complex problem solving”_

> **App Output**:  
> ✅ Suggestion 1  
> 🎧 Watch this episode: *All About Identity-Other Distinctions*  
> ❓ *How can developing cognitive skills and technical know-how contribute to solving complex public policy problems?*  
> 🧠 *(Model answer follows...)*

---

## 🛠️ How It Works

- Transcripts and metadata are loaded from `.docx` and Excel files.
- LangChain + FAISS is used to embed and search transcript chunks.
- A GPT model generates the teaching content dynamically using RAG.

---