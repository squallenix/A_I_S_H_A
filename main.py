from tkinter import *
import customtkinter as ctk
from customtkinter import *
from login import Login
from chatbox import Chatbox
from menu import Menu
from voice import Voice
from signup import Signup
from forget_pass import Forget_pass
from otp import Otp
from change_password import Change_pass
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Advanced Intelligent Special Home Assistant - A.I.S.H.A")
        
        self.configure(bg="white")

        # container that holds all frames (pages)
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (Login,Chatbox,Menu,Voice,Signup):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "Menu" or page_name == "Voice" or page_name == "Chatbox":
            self.geometry("800x500+0+0")
        else:
            self.geometry("1350x670+0+0")

 


if __name__ == "__main__":
    app = MainApp()
    app.resizable(False, False)
    app.mainloop()