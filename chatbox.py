import threading
import customtkinter as ctk
import numpy as np
from paths import IMAGE_PATHS
from PIL import Image
from ollama import chat
from tkinter import filedialog
import speech_recognition as sr
import pyaudio
class Chatbox(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        IMAGES = {
            "icon": ctk.CTkImage(Image.open(IMAGE_PATHS["icon"]), size=(35, 35)),
            "add": ctk.CTkImage(Image.open(IMAGE_PATHS["add"]), size=(30, 29)),
            "back": ctk.CTkImage(Image.open(IMAGE_PATHS["back"]), size=(30, 29)),
            "enter": ctk.CTkImage(Image.open(IMAGE_PATHS["enter"]), size=(20, 20)),
            "record": ctk.CTkImage(Image.open(IMAGE_PATHS["record"]), size=(35, 35)),
            "stop": ctk.CTkImage(Image.open(IMAGE_PATHS["stop"]), size=(30, 29)),
            "back": ctk.CTkImage(Image.open(IMAGE_PATHS["back"]), size=(30, 29)),
        }
        icon=IMAGES["icon"]
        add=IMAGES["add"]
        back=IMAGES["back"]
        enter=IMAGES["enter"]
        record=IMAGES["record"]
        stop=IMAGES["stop"]
        back=IMAGES["back"]
        self.image_added = None

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.recording = False
        self.audio_data = None
        self.listening = None
        self.running = False
        self.stream = None
        self.p = pyaudio.PyAudio()
        self.waveform_running = False
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        #chat frame
        self.chatFrame = ctk.CTkFrame(self, fg_color="gray20",corner_radius=0)
        self.chatFrame.grid(row=0, column=0,rowspan=2,columnspan=3, sticky="nsew")
        self.chatFrame.grid_rowconfigure(0, weight=0)
        self.chatFrame.grid_rowconfigure(1, weight=1)
        self.chatFrame.grid_rowconfigure(2, weight=1)
        self.chatFrame.grid_columnconfigure(0, weight=0)
        self.chatFrame.grid_columnconfigure(1, weight=1)
        self.chatFrame.grid_columnconfigure(2, weight=1)
        self.back_button = ctk.CTkButton(
            self.chatFrame, image= back, text="", corner_radius=0, fg_color="gray20",hover_color="gray30",width=50,height=30,command=lambda: controller.show_frame("Menu"))
        self.back_button.grid(row=0, column=2, sticky="ne",padx=10,pady=10)
        #chat frame
        #sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="gray10",corner_radius=0)
        self.frame_visible = False
        self.sidebar_frame.grid_rowconfigure(0, weight=0)
        self.sidebar_frame.grid_rowconfigure(1, weight=0)
        self.sidebar_frame.grid_columnconfigure(0, weight=0)
        self.settings_button1 = ctk.CTkButton(
            self.sidebar_frame, text="New Chat", corner_radius=0, fg_color="gray10",hover_color="gray20"
        )
        self.settings_button1.grid(row=0, column=0, sticky="n",pady=3)
        self.settings_button2 = ctk.CTkButton(
            self.sidebar_frame, text="Settings", corner_radius=0, fg_color="gray10",hover_color="gray20"
        )
        self.settings_button2.grid(row=1, column=0, sticky="n",pady=3)
        #sidebar frame
        self.waveform_canvas = ctk.CTkCanvas(self.chatFrame, width=400, height=1, bg="gray30")
        #sidebar button
        self.sidebar_button = ctk.CTkButton(
            self.chatFrame,image=icon, text="", command=self.toggle_sidebar,corner_radius=0, fg_color="gray20",hover_color="gray30",width=30,height=30,bg_color="gray20"
        )
        self.sidebar_button.grid(row=0, column=0)
        #sidebar button
        
        #text boxes
        self.text_box1 = ctk.CTkTextbox(self.chatFrame, fg_color="gray20", text_color="white",corner_radius=15,height=300,state="disabled")
        self.text_box1.grid(row=1, column=0,sticky="wse",rowspan=1,columnspan=3, padx=60, pady=10)
        self.text_box2 = ctk.CTkTextbox(self.chatFrame, fg_color="gray50", text_color="black",corner_radius=15,height=90,)
        self.text_box2.grid(row=2, column=0,sticky="wse",rowspan=1,columnspan=3, padx=60, pady=20)
        self.text_box2.grid_columnconfigure(0, weight=1)
        self.text_box2.grid_rowconfigure(0, weight=1)
        self.add_button = ctk.CTkButton(
            self.chatFrame,image=add, text="",corner_radius=0, fg_color="gray20",hover_color="gray30",width=30,height=30,command=self.pick_image
        )
        self.add_button.grid(row=2, column=0, sticky="w",padx=10)
        self.record_button = ctk.CTkButton(
            self.chatFrame,image=record, text="",corner_radius=0, fg_color="gray20",hover_color="gray30",width=35,height=35,command=self.mic_button
        )
        self.record_button.grid(row=2, column=2, sticky="e",padx=10)
        self.send_button = ctk.CTkButton(
            self.text_box2,image=enter, text="",corner_radius=20, fg_color="gray10",hover_color="gray30",width=50,height=30,command=self.send_prompt
        )
        self.send_button.grid(row=0,column=0, sticky="se")
        #text boxes
        
    def toggle_sidebar(self):
        if self.frame_visible:
            self.sidebar_frame.grid_remove()
            self.grid_columnconfigure(0, weight=0)
            self.grid_columnconfigure(1, weight=1)
            self.chatFrame.grid(row=0, column=0, sticky="nsew")
            self.frame_visible = False

        else:
            self.grid_columnconfigure(0, weight=0)
            self.grid_columnconfigure(1, weight=1)
            self.sidebar_frame.grid(row=1, column=0,rowspan=2, sticky="nsew")
            self.chatFrame.grid(row=0, column=1, sticky="nsew")
            self.frame_visible = True
    def pick_image(self):
        filepath = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp"),
                ("All Files", "*.*")
            ]
        )

        if filepath:
            self.image_added = filepath
    def send_prompt(self):
        if not self.image_added:
            user_prompt = self.text_box2.get("1.0", "end").strip()
            self.ai(user_prompt, self.image_added,model="gpt-oss:120b-cloud")
            self.text_box2.delete("1.0", "end")

            return
        else:
            user_prompt = self.text_box2.get("1.0", "end").strip()
            self.ai(user_prompt, self.image_added,model="qwen3-vl:235b-cloud")
            self.text_box2.delete("1.0", "end")

            return
        
    def ai(self, promt,image_path, model, max_tokens=512):
        stream = chat(
        model=model,
        messages=[
            {"role": "user",
            "content": promt,
            "images": [image_path] if image_path else None
            }
        ],
        stream=True
        )
        full_response = ""
        for chunk in stream:
            token = chunk["message"]["content"]
            full_response += token
            self.text_box1.configure(state="normal")
            self.text_box1.insert("end", token)
            self.text_box1.see("end")
            self.text_box1.configure(state="disabled")
            
        self.text_box1.configure(state="normal")
        self.text_box1.insert("end", "\n\n")
        self.text_box1.configure(state="disabled")
        self.image_added = None
        return 
    def _callback(self, recognizer,audio):
        self.audio_data = audio

    def start_waveform(self):
        if self.waveform_running:
            return

        self.waveform_running = True

        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024
        )
        threading.Thread(target=self.start_waveform, daemon=True).start()
        threading.Thread(target=self._update_waveform, daemon=True).start()

    def stop_waveform(self):
        self.waveform_running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.waveform_canvas.delete("all")

    def _update_waveform(self):
        while self.waveform_running:
            try:
                data = self.stream.read(1024, exception_on_overflow=False)
                samples = np.frombuffer(data, dtype=np.int16)

                self.waveform_canvas.delete("all")
                mid = 50
                width = 400
                step = len(samples) // width

                for x in range(width):
                    y = int(samples[x * step] / 32768 * mid)
                    self.waveform_canvas.create_line(
                        x, mid - y,
                        x, mid + y,
                        fill="lime"
                    )
            except Exception as e:
                pass

    def start(self):
        if self.recording:
            return

        print("Recording started")
        self.recording = True

        # reset buffer
        self.audio_bytes = bytearray()

        # start waveform safely
        self.running = True
        self.start_waveform()

        # open mic stream ONCE
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,              
            input=True,
            frames_per_buffer=1024
        )

        def record_thread():
            try:
                while self.recording:
                    data = self.stream.read(
                        1024,
                        exception_on_overflow=False  #  prevents crashes
                    )
                    self.audio_bytes.extend(data)
            except Exception as e:
                print("Recording error:", e)

        
        self.record_thread = threading.Thread(
            target=record_thread,
            daemon=True
        )
        self.record_thread.start()


    def stop(self):
        if not self.recording:
            return

        print("Recording stopped")
        self.recording = False


        self.stop_waveform()


        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        if not self.audio_bytes:
            print("⚠ No audio captured")
            return

        self.audio_data = sr.AudioData(
        bytes(self.audio_bytes),
        sample_rate=44100,
        sample_width=self.p.get_sample_size(pyaudio.paInt16)
        )   

        try:
            text = self.recognizer.recognize_google(self.audio_data)
            self.after(0, lambda: self.text_box2.insert("end", text + "\n"))
            print("Recognized text:", text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("API error:", e)
        finally:
            print("Ready for next recording")
        
        self.audio_bytes = bytearray()

    def mic_button(self):
        if self.recording:
            self.stop()
        else:
            self.start()
    

#app = Chatbox()
#app.mainloop()
