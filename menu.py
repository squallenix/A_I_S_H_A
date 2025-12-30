from tkinter import *
from PIL import Image, ImageTk
from customtkinter import *

class Menu(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="black")
        self.controller = controller

        # Configure grid for main frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # main content

        # === Sidebar Frame ===
        sidebar = CTkFrame(self, fg_color="black", width=300)
        sidebar.grid(row=0, column=0, sticky="nsw", padx=(50, 20), pady=50)
        sidebar.grid_propagate(False)  # prevent auto-resize

        # Sidebar buttons (use grid instead of place)
        button_opts = {
            "fg_color": "cyan2",
            "font": ("Arial", 20),
            "width": 200,
            "bg_color": "black",
            "text_color": "black",
            "hover_color": "cyan4",
            "corner_radius": 30,
            "cursor": "hand2",
            "border_width": 2,
            "border_color": "gray77"
        }

        
        button1 = CTkButton(sidebar, text="Chat_Box",command=lambda: controller.show_frame("Chatbox"), **button_opts)
        button2 = CTkButton(sidebar, text="Voice Assistance",command=lambda: controller.show_frame("Voice"), **button_opts)

        sidebar.grid_rowconfigure((0,1,2), weight=1)
        button1.grid(row=0, column=0, pady=10)
        button2.grid(row=1, column=0, pady=10)

        # === Main content frame ===
        frame2 = CTkFrame(
            self,
            fg_color="gray5",
            border_width=1,
            corner_radius=15
        )
        frame2.grid(row=0, column=1, padx=(30,70), pady=50, sticky="nsew")

        frame2.grid_rowconfigure((0,1,2), weight=1)
        frame2.grid_columnconfigure(0, weight=1)

        text_sample = (
            "But Moore netted three times in the space\n"
            "of 23 minutes in the second half to take\n"
            "his goal tally to nine for the season and\n"
            "inspire Wrexham to their most impressive\n"
            "result of the campaign."
        )

        # Labels inside frame2
        l1 = CTkLabel(frame2, text=text_sample, text_color="white", font=("Helvetica", 12))
        l2 = CTkLabel(frame2, text=text_sample, text_color="white", font=("Helvetica", 12))
        l3 = CTkLabel(frame2, text=text_sample, text_color="white", font=("Helvetica", 12))

        l1.grid(row=0, column=0, sticky="n", pady=(20, 10))
        l2.grid(row=1, column=0, sticky="n", pady=(10, 10))
        l3.grid(row=2, column=0, sticky="n", pady=(10, 20))

        # === Top-right settings ===
        topbar = CTkFrame(self, fg_color="black")
        topbar.grid(row=0, column=1, sticky="ne", padx=(0, 20), pady=(10, 0))

        settings_button = CTkButton(
            topbar,
            bg_color="black",
            fg_color="black",
            text="⚙️",
            font=("Arial", 22),
            width=0,
            cursor="hand2",
            text_color="white",
            hover_color="gray15",
            corner_radius=30,
            
        )
        settings_button.grid(row=0, column=0, sticky="e")

        # === Logout (bottom-right) ===
        logout_button = CTkButton(
            self,
            bg_color="black",
            fg_color="cyan2",
            text="LogOut",
            font=("Arial", 15),
            width=0,
            cursor="hand2",
            text_color="black",
            hover_color="cyan3",
            corner_radius=30,
            border_width=2,
            border_color="gray77",
            command=lambda: controller.show_frame("Login")
        )
        logout_button.grid(row=0, column=1, sticky="se", padx=20, pady=10)
