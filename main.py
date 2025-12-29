from tkinter import *
import customtkinter as ctk
from customtkinter import *
from login import Login
from chatbox import Chatbox
from menu import Menu
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login System")
        self.geometry("1350x700+0+0")
        self.configure(bg="white")

        # container that holds all frames (pages)
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Login,Chatbox,Menu):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "Menu":
            self.geometry("800x500+0+0")
        else:
            self.geometry("1350x700+0+0")


 


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()