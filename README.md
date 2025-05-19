# 🎙️ CmdMe - Voice Assistant using Python

CmdMe is a desktop-based voice assistant that lets you control your system using typed or spoken commands. Built using `customtkinter`, it features a modern GUI, voice interaction, and basic system control.

---

## 📦 Features

- Open apps (Notepad, Calculator, Chrome, etc.)
- Browse websites (e.g., "open google.com")
- Get date and time
- Control system (shutdown, restart)
- Voice and text input
- Light/Dark/System themes
- Adjustable voice speed and gender

---

## 🛠 Tech Stack

- `customtkinter`
- `pyttsx3` (text-to-speech)
- `SpeechRecognition` + `pyaudio` (speech-to-text)
- `tkinter` (GUI components)
- `subprocess`, `os`, `datetime`, etc.

---

## 🔧 Installation

### Step 1: Download or Clone the Repository

```bash
https://github.com/IamSomnathDas/CmdMe.git
cd cmdme

Or download the ZIP and extract it.


---

#Step 2: Create and Activate a Virtual Environment (recommended)

On Windows:

python -m venv venv
venv\Scripts\activate

On macOS/Linux:

python3 -m venv venv
source venv/bin/activate


---

Step 3: Install Required Python Packages

pip install -r requirements.txt

If you encounter issues installing pyaudio, try:

Windows:


pip install pipwin
pipwin install pyaudio

macOS (with Homebrew):


brew install portaudio
pip install pyaudio

Linux (Debian/Ubuntu):


sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio


---

#Step 4: Run the Application

python main.py


---

#Usage

Type commands into the input box and press Send or hit Enter.

Click Speak and say a command to use voice control.

Use the sidebar to clear chat, adjust appearance, or voice settings.

Example commands:

"Open notepad"

"Open google.com"

"What is the time?"

"Shutdown the system"




---

#File Structure

cmdme/
├── main.py          # Main application script
├── requirements.txt # Python dependencies
├── icon.ico         # App icon file
└── README.md        # This file


---

#Dependencies

customtkinter

pyttsx3

SpeechRecognition

pyaudio

tkinter (builtin)

Other standard libraries: threading, subprocess, datetime, os, webbrowser



---

#License

This project is for educational purposes.


---

#Author

Somnath Das
GitHub Profile:
https://github.com/IamSomnathDas


---

If you want me to generate requirements.txt or help with anything else, just ask!
