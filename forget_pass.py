from tkinter import *
from tkinter import Label
from tkinter import messagebox
from PIL import Image,ImageTk
import customtkinter as ctk


class Forget_pass(ctk.CTkFrame):
   def __init__(self, parent, controller):
        super().__init__(parent)



        #----------------------IMAGE PART-------------------------------

        self.phone_image = ImageTk.PhotoImage(file="K:\\Code\\Project\\Advanced_intelligent assistant\\Forgetpass.png")
        self.lbl_img1=Label(self,image=self.phone_image,bg="Slate Gray1").place(x=0,y=160,width=520,height=500)

        self.phone_image2 = ImageTk.PhotoImage(file="K:\\Code\\Project\\Advanced_intelligent assistant\\Forgetpass2.png")
        self.lbl_img2 = Label(self, image=self.phone_image2, bg="Slate Gray1").place(x=800, y=160, width=450,height=500)


        #----------------------forget Frame1------------------------------

        forget_frame = Label(self,bd=0,relief=RIDGE,bg="Slate Gray1")
        forget_frame.place(x=500,y=215,width=300,height=300)

        mail= Label(forget_frame,text="Email Address", font=("Andalus,15"),bg="Slate Gray1",fg="black").place(x=0,y=10)
        self.mail = StringVar()
        Email = Entry(forget_frame,textvariable=self.mail,font=("times new roman",20),bg="#ECECEC").place(x=0,y=40)

        button = Button(forget_frame,  text="RESET", font=("Arial Rounded MT Bold", 15),
                        bg="black", activebackground="black", fg="white", activeforeground="white",
                        cursor="hand2",command=lambda: controller.show_frame("")).place(x=50, y=90, width=180, height=30)

        #--------------------Forget frame2-------------
        forget_frame2 = Label(self, bd=0, relief=RIDGE, bg="Slate Gray1")
        forget_frame2.place(x=350, y=80, width=400, height=150)

        titel = Label(forget_frame2, text="FORGOT", font=("Comic Sans MS", 30, "bold"), bg="Slate Gray1", fg="black").place(x=0, y=0,relwidth=1)
        titel = Label(forget_frame2, text="YOUR PASSWORD", font=("Comic Sans MS", 30, "bold"), bg="Slate Gray1", fg="black").place(x=0, y=50, relwidth=1)

