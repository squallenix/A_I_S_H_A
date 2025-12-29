import json
from tkinter import *
from PIL import Image, ImageTk
from customtkinter import *
from tkinter import filedialog, messagebox, simpledialog
import threading
import speech_recognition as sr
import pyttsx3
import subprocess
import psutil
import keyboard
from rapidfuzz import fuzz
import os
import re
import difflib
import textdistance


class voice_Assistant(CTkFrame):
    JSON_FILE = "apps.json"  # 🗂️ File to store added apps

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="black")
        self.controller = controller
        self.voice_enabled = BooleanVar(value=False)
        self.listening_thread = None
        self.hotkey_thread = None

        # ========================== GRID SETUP ==========================
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        bg_frame = CTkFrame(self, fg_color="black")
        bg_frame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew")

        container = CTkFrame(self, fg_color="black")
        container.grid(row=1, column=1, sticky="n")

        container.grid_rowconfigure((0, 1, 2), weight=0)
        container.grid_columnconfigure(0, weight=0)
        container.grid_columnconfigure(1, weight=1)

        # ========================== LABELS ==========================
        label1 = CTkLabel(container, text="Keyboard Shortcut", text_color="white", font=("Helvetica", 20))
        label1.grid(row=0, column=0, sticky="w", padx=(20, 10), pady=(10, 5))

        label2 = CTkLabel(container, text="Executable Path", text_color="white", font=("Helvetica", 20))
        label2.grid(row=1, column=0, sticky="w", padx=(20, 10), pady=(10, 5))

        # ========================== TEXTBOXES ==========================
        frame2 = CTkFrame(container, fg_color="black")
        frame2.grid(row=0, column=1, sticky="ew", padx=(0, 20), pady=(10, 5))
        frame3 = CTkFrame(container, fg_color="black")
        frame3.grid(row=1, column=1, sticky="ew", padx=(0, 20), pady=(10, 5))

        self.input_text_field = CTkTextbox(
            frame2, wrap='word', font=("Helvetica", 15),
            border_width=2, border_color="gray90",
            text_color="white", fg_color="gray15",
            corner_radius=15, state='disabled', height=40
        )
        self.input_text_field.pack(fill='both', expand=True, padx=5, pady=5)

        self.input_text_field2 = CTkTextbox(
            frame3, wrap='word', font=("Helvetica", 15),
            border_width=2, border_color="gray90",
            text_color="white", fg_color="gray15",
            corner_radius=15, state='disabled', height=40
        )
        self.input_text_field2.pack(fill='both', expand=True, padx=5, pady=5)

        # ========================== BUTTONS ==========================
        frame4 = CTkFrame(container, fg_color="black")
        frame4.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=(10, 5))

        button = CTkButton(
            frame4,
            fg_color="black",
            text="📂",
            font=("Arial", 40),
            width=0,
            text_color="orange",
            hover_color="gray25",
            corner_radius=30,
            command=self.insert_file,
        )
        button.pack(side="left", padx=(5, 0))

        back_btn = CTkButton(
            self,
            text="← Back",
            fg_color="cyan2",
            text_color="black",
            hover_color="cyan4",
            font=("Arial", 15),
            corner_radius=20,
            cursor="hand2",
            command=lambda: controller.show_frame("Menu") if controller else None
        )
        back_btn.grid(row=2, column=1, sticky="se", padx=20, pady=20)

        # ========================== VOICE SUPPORT TOGGLE ==========================
        voice_frame = CTkFrame(self, fg_color="black")
        voice_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))

        voice_label = CTkLabel(voice_frame, text="Enable Voice Support:", text_color="white", font=("Helvetica", 16))
        voice_label.pack(side="left", padx=(0, 10))

        voice_checkbox = CTkCheckBox(
            voice_frame,
            text="",
            variable=self.voice_enabled,
            onvalue=True,
            offvalue=False,
            checkbox_height=24,
            checkbox_width=24,
            border_width=2,
            corner_radius=5,
            fg_color="orange",
            hover_color="gray25",
            command=self.toggle_voice_support
        )
        voice_checkbox.pack(side="left")

        # ============ SPEECH ENGINE ============
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 175)

        # ============ LOAD APPS ============
        self.apps = self.load_apps()

    # =============================================================
    # 🧠 JSON HANDLERS
    # =============================================================
    def load_apps(self):
        default_apps = {
            "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe"
        }
        if os.path.exists(self.JSON_FILE):
            try:
                with open(self.JSON_FILE, "r") as f:
                    user_apps = json.load(f)
                default_apps.update(user_apps)
            except Exception as e:
                print("⚠️ Failed to load apps.json:", e)
        return default_apps

    def save_apps(self):
        try:
            # Save only user-added apps (excluding built-ins)
            with open(self.JSON_FILE, "w") as f:
                json.dump(self.apps, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save apps: {e}")

    # =============================================================
    # 📂 Insert .exe Path Function + Alias
    # =============================================================
    def insert_file(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select an Executable File",
                filetypes=[("Executable files", "*.exe")],
            )
            if not file_path:
                return

            alias = simpledialog.askstring("App Alias", "Enter a short name (alias) to open/close this app:")
            if not alias:
                messagebox.showwarning("No Alias", "You must enter an alias to register the app.")
                return

            alias = alias.strip().lower()
            self.apps[alias] = file_path
            self.save_apps()

            self.input_text_field.configure(state='normal')
            self.input_text_field.delete("1.0", "end")
            self.input_text_field.insert("1.0", alias)
            self.input_text_field.configure(state='disabled')

            self.input_text_field2.configure(state='normal')
            self.input_text_field2.delete("1.0", "end")
            self.input_text_field2.insert("1.0", file_path)
            self.input_text_field2.configure(state='disabled')

            messagebox.showinfo("App Added", f"Added alias '{alias}' for:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert file:\n{e}")

    # =============================================================
    # 🎙️ Toggle Voice Support
    # =============================================================
    def toggle_voice_support(self):
        if self.voice_enabled.get():
            print("🎙️ Voice Support Enabled")
            self.speak("Voice support enabled. Press Control plus Space to speak.")
            self.hotkey_thread = threading.Thread(target=self.start_hotkey_listener, daemon=True)
            self.hotkey_thread.start()
        else:
            print("🔇 Voice Support Disabled")
            self.speak("Voice support disabled.")
            keyboard.unhook_all_hotkeys()

    # =============================================================
    # 🔊 Speech Output
    # =============================================================
    def speak(self, text):
        print("A.I.S.H.A:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    # =============================================================
    # 🎧 Voice Recognition
    # =============================================================
    def voice_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            self.process_command(command.lower())
        except Exception as e:
            print("Error:", e)
            self.speak("Sorry, I couldn't understand that.")

    # =============================================================
    # ⚙️ Command Processing
    # =============================================================
    def match_app(self, user_text):
        def normalize(text):
            # Lowercase and remove punctuation/spaces
            text = text.lower().strip()
            text = re.sub(r"[^a-z0-9]+", "", text)
            return text

        def phonetic_code(text):
            """Return Soundex-like phonetic code"""
            try:
                return textdistance.soundex(text)
            except Exception:
                return text  # fallback if not convertible

        user_text_norm = normalize(user_text)
        user_sound = phonetic_code(user_text_norm)

        best_app = None
        best_score = 0

        for app_name in self.apps:
            app_norm = normalize(app_name)
            app_sound = phonetic_code(app_norm)

            # Fuzzy scores (text similarity)
            score1 = fuzz.ratio(user_text_norm, app_norm)
            score2 = fuzz.partial_ratio(user_text_norm, app_norm)
            score3 = fuzz.token_sort_ratio(user_text_norm, app_norm)
            seq_match = difflib.SequenceMatcher(None, user_text_norm, app_norm).ratio() * 100

            # Phonetic score (sound similarity)
            phonetic_match = difflib.SequenceMatcher(None, user_sound, app_sound).ratio() * 100

            # Weighted average (60% text, 40% phonetic)
            final_score = (0.6 * ((score1 + score2 + score3 + seq_match) / 4)) + (0.4 * phonetic_match)

            if final_score > best_score:
                best_score = final_score
                best_app = app_name

        # Match threshold lowered for accent tolerance
        if best_score > 45:
            print(f"🧩 Matched '{user_text}' → '{best_app}' ({best_score:.1f}%)")
            return best_app
        else:
            print(f"❌ No match for '{user_text}' (best={best_score:.1f}%)")
            return None
        # =============================================================
    # 🧩 Process recognized voice command
    # =============================================================
    def process_command(self, text):
        text = text.lower().strip()
        print(f"🎧 Recognized command: {text}")

        if any(word in text for word in ["open", "start", "launch", "activate"]):
            # Extract app name
            for word in ["open", "start", "launch", "activate"]:
                text = text.replace(word, "")
            app_name = text.strip()

            app = self.match_app(app_name)
            if app:
                try:
                    os.startfile(self.apps[app])

                    self.speak(f"Opening {app}")
                except Exception as e:
                    print(f"⚠️ Failed to open {app}: {e}")
                    self.speak(f"Sorry, I couldn't open {app}.")
            else:
                self.speak("I couldn't find that app.")

        elif any(word in text for word in ["close", "exit", "stop", "terminate", "kill"]):
            for word in ["close", "exit", "stop", "terminate", "kill"]:
                text = text.replace(word, "")
            app_name = text.strip()

            app = self.match_app(app_name)
            if app:
                closed = False
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if app.lower() in proc.info['name'].lower():
                            psutil.Process(proc.info['pid']).terminate()
                            closed = True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                if closed:
                    self.speak(f"Closed {app}")
                else:
                    self.speak(f"{app} is not currently running.")
            else:
                self.speak("I couldn't identify which app to close.")

        else:
            self.speak("Command not recognized. Please say open or close followed by app name.")

    
    
    
    # =============================================================
    # ⌨️ Hotkey Listener
    # =============================================================
    def start_hotkey_listener(self):
        keyboard.add_hotkey("ctrl+space", lambda: threading.Thread(target=self.voice_command, daemon=True).start())
        keyboard.wait()


# ========================== RUN STANDALONE ==========================
# if __name__ == "__main__":
#     app = CTk()
#     frame = voice_Assistant(app, controller=None)
#     frame.pack(fill="both", expand=True)
#     app.mainloop()
