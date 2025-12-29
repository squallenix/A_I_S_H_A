import customtkinter as ctk
from paths import IMAGE_PATHS
from PIL import Image
from ollama import chat
from tkinter import filedialog
class Chatbox(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        IMAGES = {
            "icon": ctk.CTkImage(Image.open(IMAGE_PATHS["icon"]), size=(35, 35)),
            "add": ctk.CTkImage(Image.open(IMAGE_PATHS["add"]), size=(30, 29)),
            "back": ctk.CTkImage(Image.open(IMAGE_PATHS["back"]), size=(30, 29)),
            "enter": ctk.CTkImage(Image.open(IMAGE_PATHS["enter"]), size=(20, 20)),
            
        }
        icon=IMAGES["icon"]
        add=IMAGES["add"]
        back=IMAGES["back"]
        enter=IMAGES["enter"]
        self.image_added = None
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        #chat frame
        self.chatFrame = ctk.CTkFrame(self, fg_color="gray20",corner_radius=0)
        self.chatFrame.grid(row=0, column=0,rowspan=2,columnspan=3, sticky="nsew")
        self.chatFrame.grid_rowconfigure(0, weight=0)
        self.chatFrame.grid_rowconfigure(1, weight=1)

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
        

    
    

#app = Chatbox()
#app.mainloop()
