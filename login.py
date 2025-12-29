from paths import IMAGE_PATHS
from tkinter import *
from tkinter import Label
from tkinter import messagebox
from PIL import Image,ImageTk
from customtkinter import *
import customtkinter as ctk

class Login(ctk.CTkFrame):
    def __init__(self,parent, controller):
        super().__init__(parent)

        
        IMAGES = {k: ImageTk.PhotoImage(Image.open(v)) for k, v in IMAGE_PATHS.items()}
        #----------------------IMAGE PART-------------------------------

        self.phone_image = IMAGES["bg"]
        self.lbl_img1=Label(self,image=self.phone_image,bg='#333333').place(x=50,width=600,height=700)


        #----------------------Login Frame------------------------------

        Login_frame = CTkFrame(self,fg_color="black",corner_radius=10,width=310,height=340)
        Login_frame.place(x=800,y=160)

        tittle = CTkLabel(Login_frame,text="Login",text_color='white',font=("Comic Sans MS",40,"bold"),fg_color="black")
        tittle.place(x=0,y=20,relwidth=1)

        username= CTkLabel(Login_frame,text="Username",text_color='white', font=("Andalus",15),fg_color="black")
        username.place(x=50,y=80)
        self.username = StringVar()

        user = CTkEntry(Login_frame,textvariable=self.username,font=("times new roman",15),width=200,corner_radius=15)
        user.place(x=50,y=110)

        password = CTkLabel(Login_frame, text="Password",text_color='white', font=("Andalus",15), fg_color="black")
        password.place(x=50, y=150)
        self.password = StringVar()

        pas = CTkEntry(Login_frame,show="*",textvariable=self.password, font=("times new roman", 15),width=200,corner_radius=15)
        pas.place(x=50, y=180)

        button = CTkButton(Login_frame,command=lambda :controller.show_frame("Menu"),text="Log In",text_color="white",font=("Arial Rounded MT Bold",20),cursor="hand2",corner_radius=15,width=150,height=30,hover_color="deepskyblue",fg_color="deepskyblue")
        button.place(x=75,y=230)

        hr = Label(Login_frame,bg="lightgray").place(x=50,y=280, width=200,height=3)
        rr = Label(Login_frame,text="OR",bg="black",fg="lightgray",font=("times new roman", 15,"bold"))
        rr.place(x=130,y=267)

        forgetpass = Button(Login_frame,text="Forget Password??",font=("times new roman", 13,"bold"),bg="black",fg="gold",bd=0,activebackground="black",activeforeground="gold",command=lambda: controller.show_frame("Forget_part"))
        forgetpass.place(x=75, y=290)

        # ----------------------Login Frame 2------------------------------

        Register_frame = CTkFrame(self, corner_radius=10,  fg_color="black", width=310, height=40)
        Register_frame.place(x=800, y=510)

        reg = Label(Register_frame,text="Don't have an account?",font=("times new roman", 13),bg="black",fg="white")
        reg.place(x=40,y=5)

        sign_up = Button(Register_frame, text="Sign Up",font=("times new roman", 13,"bold"), bg="black",fg="gold", bd=0, activebackground="black",activeforeground="gold",command=lambda: controller.show_frame("Signup"))
        sign_up.place(x=200,y=4)

        #---------------------Animation Image-----------------------

        # Inside __init__
        self.images = [IMAGES[f"ui{i}"] for i in range(1, 8)]
        self.img_index = 0

# Make sure this Label exists BEFORE starting animation
        self.lb1_animation = Label(self, bg="white")
        self.lb1_animation.place(x=70, y=50, width=550, height=600)

# Start animation
        self.animation()


# Outside __init__ (same indentation level as __init__)
    def animation(self):
        self.lb1_animation.config(image=self.images[self.img_index])
        self.img_index = (self.img_index + 1) % len(self.images)
        self.lb1_animation.after(4000, self.animation)



       #----------------------Login function part----------------------

    def login(self):
        uname = "Quaium"
        pw = "8541"

        if self.username.get() == uname and self.password.get() == pw:
            messagebox.showinfo(title="Login Success", message="You Successfully Logged in")
        else:
            messagebox.showinfo(title="Invalid Login", message="Please try again")



