# AI-voice-Assistant
<img width="1893" height="925" alt="image" src="https://github.com/user-attachments/assets/99f44287-2689-4431-9c74-b1378f5bfe2a" />

---
# 🎙️ AI Voice Assistant with FastAPI

An intelligent voice-activated desktop assistant built using **FastAPI**, **speech recognition**, **text-to-speech**, and various automation utilities. This assistant can perform system tasks, interact with APIs, browse the web, and respond intelligently using ChatGPT integration.

---

## 🧠 Features

- ✅ Voice & Text-based assistant (uses `speech_recognition` & FastAPI)
- ✅ Open websites like YouTube, Google
- ✅ Take screenshots with timestamp
- ✅ Check system battery status
- ✅ Get current location via IP
- ✅ Calculate distance between places (Google Maps)
- ✅ Perform actions in browser (new tab, incognito, history)
- ✅ Tell jokes (via `pyjokes`)
- ✅ Perform speed tests (via `speedtest`)
- ✅ Reminder/Note functionality
- ✅ Open/Close Notepad, Command Prompt, Camera
- ✅ Take photos using Windows Camera app
- ✅ Wikipedia-like help via `pywikihow`
- ✅ Speak AI answers using ChatGPT backend

---

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Voice I/O**: SpeechRecognition, pyttsx3
- **Web Automation**: pyautogui, webbrowser, keyboard
- **NLP**: OpenAI / ChatGPT
- **Other Tools**: pyjokes, speedtest, pywikihow

---

## 📁 Folder Structure

openAI-project/
├── .venv/ # Python virtual environment
├── devil_voice_assistant.py # Core command and action functions
├── main.py # FastAPI server (voice/text chat routes)
├── data.txt # Stores remembered notes
├── static/ # Frontend files (HTML, CSS, JS)
└── requirements.txt # Python dependencies

---
How Run Project:

Step 1: Create and activate virtual environment

       python -m venv .venv
      .venv\Scripts\activate
      
Step 2: Install dependencies

    pip install -r requirements.txt

Step 3: Run the application

    uvicorn main:app --reload


