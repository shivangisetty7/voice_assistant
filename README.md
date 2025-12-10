# 🎙 Simple Voice Assistant (Python)
A simple Python voice assistant that uses speech recognition and text-to-speech to perform basic tasks like telling time, opening websites and answering simple commands.

A beginner-friendly **voice assistant** built using Python.  
It listens to your voice through the microphone, understands basic commands, and responds using text-to-speech.

This project helped me understand how speech recognition and text-to-speech work in real applications.

---

## ✨ Features

- 🎧 Listens to voice input via microphone  
- 🗣 Converts speech to text using Google Speech Recognition  
- 🔊 Speaks responses using `pyttsx3`  
- ⏰ Tells the current time  
- 🌐 Opens common websites:
  - Google
  - YouTube
  - GitHub  
- ℹ️ Answers basic questions like:
  - "What is your name?"
  - "Who are you?"
- 🛑 Can be stopped with commands like:
  - "stop"
  - "exit"
  - "quit"

---

## 🧠 Tech Stack

| Component      | Used                      |
|---------------|---------------------------|
| Language      | Python 3                  |
| Speech-to-Text| `speech_recognition`      |
| Text-to-Speech| `pyttsx3`                 |
| Audio Input   | Microphone (via `PyAudio`)|
| Browser       | `webbrowser` module       |

---

## ▶️ How to Run

### 1️⃣ Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate    # Linux / Mac
venv\Scripts\activate       # Windows
