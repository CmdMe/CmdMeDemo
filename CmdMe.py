import customtkinter as ctk
from tkinter import scrolledtext
import webbrowser
import threading
import pyttsx3
import speech_recognition as sr
import subprocess
import datetime
import os

# ======= Voice Engine Setup ========
engine = pyttsx3.init()
voices = engine.getProperty('voices')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def update_voice_settings(rate, gender):
    engine.setProperty('rate', rate)
    engine.setProperty('voice', voices[0].id if gender == 'male' else voices[1].id)

# ======= Command Handlers =========
def handle_app_opening_commands(command):
    command = command.lower()
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "command prompt": "cmd.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "chrome": "chrome.exe",
        "vs code": "code",
        "spotify": "spotify.exe"
    }
    for app_name, exe in apps.items():
        if f"open {app_name}" in command:
            try:
                subprocess.Popen(exe)
                return f"Opening {app_name.title()}."
            except FileNotFoundError:
                return f"Sorry, {app_name} is not installed."
    return None

def handle_website_command(command):
    if "open" in command and ".com" in command:
        words = command.split()
        for word in words:
            if ".com" in word:
                webbrowser.open(f"https://{word}")
                return f"Opening {word}."
    return None

def handle_time_date_commands(command):
    now = datetime.datetime.now()
    if "time" in command:
        return f"The time is {now.strftime('%I:%M %p')}."
    elif "date" in command:
        return f"Today's date is {now.strftime('%B %d, %Y')}."
    return None

def handle_system_commands(command):
    if "shutdown" in command:
        os.system("shutdown /s /t 1")
        return "Shutting down the system."
    elif "restart" in command:
        os.system("shutdown /r /t 1")
        return "Restarting the system."
    return None

# ======= Command Processing =======
def process_command(command, chat_display):
    command = command.lower()
    handlers = [
        handle_app_opening_commands,
        handle_website_command,
        handle_time_date_commands,
        handle_system_commands
    ]

    for handler in handlers:
        response = handler(command)
        if response:
            chat_display.insert('end', f"Assistant: {response}\n\n")
            chat_display.see('end')
            speak(response)
            return

    fallback = "Sorry, I didn’t understand that command."
    chat_display.insert('end', f"Assistant: {fallback}\n\n")
    chat_display.see('end')
    speak(fallback)

# ======= Voice Input Thread =======
recognizer = sr.Recognizer()
def listen_voice(chat_display):
    def listen():
        chat_display.insert('end', "Listening...\n")
        chat_display.see('end')
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                chat_display.insert('end', f"You: {command}\n")
                chat_display.see('end')
                process_command(command, chat_display)
        except sr.UnknownValueError:
            error_msg = "Sorry, I could not understand your speech."
            chat_display.insert('end', f"Assistant: {error_msg}\n")
            speak(error_msg)
        except sr.RequestError:
            error_msg = "Speech recognition service error."
            chat_display.insert('end', f"Assistant: {error_msg}\n")
            speak(error_msg)
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            chat_display.insert('end', f"Assistant: {error_msg}\n")
            speak("An error occurred.")
    threading.Thread(target=listen, daemon=True).start()

# ======= UI Themes ==========
LIGHT_THEME = {
    "bg_color": "#f0f8ff",
    "frame_color": "#ffffff",
    "widget_color": "#e6f2ff",
    "text_color": "#1a1a1a",
    "chat_bg": "#ffffff",
    "chat_fg": "#1a1a1a",
    "button_fg": "#0041AB",
    "button_hover": "#03358c"
}
DARK_THEME = {
    "bg_color": "#121b2e",
    "frame_color": "#1c2a4a",
    "widget_color": "#2a3a5f",
    "text_color": "#f0f4ff",
    "chat_bg": "#2a3a5f",
    "chat_fg": "#ffffff",
    "button_fg": "#0041AB",
    "button_hover": "#03358c"
}

# ======= Main App Class ==========
class AssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CmdMe")
        self.geometry("1000x700")
        self.iconbitmap("icon.ico")
        self.settings = {
            "appearance_mode": "system",
            "voice_rate": 150,
            "voice_gender": "female"
        }

        ctk.set_appearance_mode(self.settings["appearance_mode"])
        self._apply_theme()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()

        update_voice_settings(self.settings["voice_rate"], self.settings["voice_gender"])

    def _apply_theme(self):
        mode = self.settings.get("appearance_mode", "system")
        self.theme = DARK_THEME if (mode == "dark" or ctk.get_appearance_mode() == "Dark") else LIGHT_THEME
        self.configure(fg_color=self.theme["bg_color"])

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=180, corner_radius=20, fg_color=self.theme["frame_color"])
        sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        sidebar.grid_propagate(False)

        ctk.CTkLabel(sidebar, text="CmdMe", font=("Segoe UI", 26, "bold"),
                     text_color=self.theme["text_color"]).pack(pady=(30, 15))

        ctk.CTkButton(sidebar, text="🗑️ Clear Chat", fg_color=self.theme["button_fg"],
                      hover_color=self.theme["button_hover"], corner_radius=10,
                      command=self.clear_chat).pack(pady=(0, 20), fill='x', padx=15)

        ctk.CTkLabel(sidebar, text="⚙️ Settings", font=("Segoe UI", 18, "bold"),
                     text_color=self.theme["text_color"]).pack(pady=(0, 10))

        self.setting_widgets = {}
        self._create_dropdown(sidebar, "Appearance Mode", "appearance_mode", ["light", "dark", "system"])
        self._create_slider(sidebar, "Voice Speed", "voice_rate", 100, 250)
        self._create_dropdown(sidebar, "Voice Gender", "voice_gender", ["male", "female"])

        ctk.CTkButton(sidebar, text="✅ Apply", command=self._apply_app_settings,
                      fg_color=self.theme["button_fg"], hover_color=self.theme["button_hover"], corner_radius=10).pack(pady=(20, 5), fill='x', padx=15)

        ctk.CTkButton(sidebar, text="🔁 Reset", command=self._reset_app_settings,
                      fg_color=self.theme["button_fg"], hover_color=self.theme["button_hover"], corner_radius=10).pack(pady=(0, 10), fill='x', padx=15)

    def _build_main(self):
        main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color=self.theme["frame_color"])
        main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="Hello 👋, how can I assist you today?",
                     font=("Segoe UI", 20, "bold"), text_color=self.theme["text_color"]).pack(pady=(25, 15))

        chat_frame = ctk.CTkFrame(main_frame, corner_radius=20, fg_color=self.theme["widget_color"])
        chat_frame.pack(expand=True, fill='both', padx=20, pady=(5, 15))

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap='word', font=("Segoe UI", 12),
            bg=self.theme["chat_bg"], fg=self.theme["chat_fg"],
            relief='flat', bd=0, insertbackground=self.theme["chat_fg"]
        )
        self.chat_display.pack(expand=True, fill='both', padx=12, pady=12)
        self.chat_display.insert("end", "Assistant: Welcome! Type or speak a command below.\n\n")

        input_frame = ctk.CTkFrame(main_frame, height=60, corner_radius=20, fg_color=self.theme["widget_color"])
        input_frame.pack(fill='x', padx=20, pady=(0, 20))

        self.entry = ctk.CTkEntry(input_frame, placeholder_text="Type your command here...",
                                  font=("Segoe UI", 12), corner_radius=10)
        self.entry.pack(side='left', fill='x', expand=True, padx=(10, 10), pady=10)
        self.entry.bind("<Return>", lambda e: self._handle_send())

        ctk.CTkButton(input_frame, text="📩 Send", fg_color=self.theme["button_fg"],
                      hover_color=self.theme["button_hover"], corner_radius=10,
                      command=self._handle_send).pack(side='left', padx=(0, 10))

        ctk.CTkButton(input_frame, text="🎤 Speak", fg_color=self.theme["button_fg"],
                      hover_color=self.theme["button_hover"], corner_radius=10,
                      command=self._handle_speak).pack(side='left')

    def _create_dropdown(self, parent, label, key, options):
        ctk.CTkLabel(parent, text=label, text_color=self.theme["text_color"]).pack(pady=(10, 0))
        dropdown = ctk.CTkOptionMenu(parent, values=options, command=lambda val: self._update_setting(key, val))
        dropdown.set(self.settings[key])
        dropdown.pack(pady=5, fill='x', padx=10)
        self.setting_widgets[key] = dropdown

    def _create_slider(self, parent, label, key, min_val, max_val):
        ctk.CTkLabel(parent, text=label, text_color=self.theme["text_color"]).pack(pady=(10, 0))
        slider = ctk.CTkSlider(parent, from_=min_val, to=max_val, number_of_steps=15,
                               command=lambda val: self._update_setting(key, int(val)))
        slider.set(self.settings[key])
        slider.pack(pady=5, fill='x', padx=10)
        self.setting_widgets[key] = slider

    def _update_setting(self, key, value):
        self.settings[key] = value

    def _apply_app_settings(self):
        ctk.set_appearance_mode(self.settings["appearance_mode"])
        self._apply_theme()
        self._refresh_colors()
        update_voice_settings(self.settings["voice_rate"], self.settings["voice_gender"])
        speak("Settings applied.")

    def _reset_app_settings(self):
        self.settings = {"appearance_mode": "system", "voice_rate": 150, "voice_gender": "female"}
        for key, widget in self.setting_widgets.items():
            if isinstance(widget, ctk.CTkOptionMenu):
                widget.set(self.settings[key])
            elif isinstance(widget, ctk.CTkSlider):
                widget.set(self.settings[key])
        self._apply_app_settings()
        speak("Settings reset to default.")

    def _refresh_colors(self):
        self.chat_display.config(bg=self.theme["chat_bg"], fg=self.theme["chat_fg"], insertbackground=self.theme["chat_fg"])
        self.configure(fg_color=self.theme["bg_color"])

    def clear_chat(self):
        self.chat_display.delete("1.0", "end")

    def _handle_send(self):
        text = self.entry.get()
        if text.strip():
            self.chat_display.insert("end", f"You: {text}\n")
            self.chat_display.see("end")
            self.entry.delete(0, 'end')
            process_command(text, self.chat_display)

    def _handle_speak(self):
        self.chat_display.insert("end", "Listening for voice command...\n")
        self.chat_display.see("end")
        listen_voice(self.chat_display)

# ======== Launch App ==========
if __name__ == "__main__":
    app = AssistantApp()
    app.mainloop()
