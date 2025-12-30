import threading
import numpy as np
import speech_recognition as sr
from paths import IMAGE_PATHS
from tkinter import *
from PIL import Image
from customtkinter import *
import customtkinter as ctk
import pyaudio

class Voice(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        IMAGES = {
            "record": ctk.CTkImage(Image.open(IMAGE_PATHS["record"]), size=(35, 35)),
            "stop": ctk.CTkImage(Image.open(IMAGE_PATHS["stop"]), size=(30, 29)),
            "back": ctk.CTkImage(Image.open(IMAGE_PATHS["back"]), size=(30, 29)),
        }
        record=IMAGES["record"]
        stop=IMAGES["stop"]
        back=IMAGES["back"]
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.recording = False
        self.audio_data = None
        self.listening = None
        self.running = False
        self.stream = None
        self.p = pyaudio.PyAudio()


        #self.geometry("800x500")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.chatFrame = ctk.CTkFrame(self, fg_color="gray20",corner_radius=0)
        self.chatFrame.grid(row=0,column=0,sticky="nsew")

        self.chatFrame.grid_rowconfigure(0, weight=0)
        self.chatFrame.grid_rowconfigure(1, weight=0)
        self.chatFrame.grid_rowconfigure(2, weight=1)
        self.chatFrame.grid_columnconfigure(0, weight=1)
        self.chatFrame.grid_columnconfigure(1, weight=1)
        self.chatFrame.grid_columnconfigure(2, weight=1)

        self.label=ctk.CTkLabel(self.chatFrame, text="Voice Recognition Demo", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0,column=0, pady=10,padx=10, columnspan=3)

        self.button1=ctk.CTkButton(self.chatFrame,image=record, text="Start Listening", command=self.start, corner_radius=0, fg_color="gray20",hover_color="gray30")
        self.button1.grid(row=1,column=0,stick="w",padx=10,pady=0)
        self.button2=ctk.CTkButton(self.chatFrame,image=stop, text="Stop Listening", command=self.stop, corner_radius=0, fg_color="gray20",hover_color="gray30")
        self.button2.grid(row=1,column=2,stick="w",padx=10,pady=0)
        self.back_button = ctk.CTkButton(
        self.chatFrame, image= back, text="", corner_radius=0, fg_color="gray20",hover_color="gray30",width=50,height=30,command=lambda: controller.show_frame("Menu"))
        self.back_button.grid(row=0, column=2, sticky="ne",padx=10,pady=10)

        self.textfield=ctk.CTkTextbox(self.chatFrame, width=600, height=400)
        self.textfield.grid(row=2,column=0,sticky="nsew",columnspan=3, padx=50, pady=20)
        
        self.waveform_canvas = ctk.CTkCanvas(self.chatFrame, width=400, height=1, bg="gray30")
        self.waveform_canvas.grid(row=1, column=1, sticky="w",ipady=30)
        self.waveform_running = False
        self.stream = None
        self.p = pyaudio.PyAudio()
        self.data=None

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

        
        self.start_waveform()

        
        self.audio_bytes = bytearray()
        
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024
        )

        
        def record_thread():
            while self.recording:
                try:
                    data = self.stream.read(1024, exception_on_overflow=False)
                    self.audio_bytes.extend(data)
                except Exception as e:
                    pass

        threading.Thread(target=record_thread, daemon=True).start()

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
            self.textfield.insert("end", text + "\n")
            print("Recognized text:", text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("API error:", e)
        finally:
            print("Ready for next recording")
        
        self.audio_bytes = bytearray()



#app = Voice()
#app.mainloop()

