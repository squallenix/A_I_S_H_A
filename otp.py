from tkinter import *
from tkinter import Label
from tkinter import messagebox
from PIL import Image,ImageTk
import customtkinter as ctk



class Otp(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)


        #----------------------IMAGE PART-------------------------------

        self.phone_image = ImageTk.PhotoImage(file=r"E:\Code\Project\Advanced_intelligent assistant\A_I_S_H_A\images\otp1.png")
        self.lbl_img1=Label(self,image=self.phone_image,bg="salmon").place(x=0,y=160,width=520,height=500)

        self.phone_image2 = ImageTk.PhotoImage(file=r"E:\Code\Project\Advanced_intelligent assistant\A_I_S_H_A\images\otp2.png")
        self.lbl_img2 = Label(self, image=self.phone_image2, bg="salmon").place(x=800, y=170, width=450,height=500)


        #----------------------forget Frame1------------------------------

        Otp_frame = Label(self,bd=0,relief=RIDGE,bg="salmon")
        Otp_frame.place(x=500,y=215,width=300,height=300)

        otp= Label(Otp_frame,text="Authentication Code", font=("Andalus,15"),bg="salmon",fg="black").place(x=0,y=10)
        self.otp = StringVar()
        otpp = Entry(Otp_frame,textvariable=self.otp,font=("times new roman",20),bg="#ECECEC",justify='center').place(x=0,y=40)

        button = Button(Otp_frame,  text="VERIFY", font=("Arial Rounded MT Bold", 15),
                        bg="black", activebackground="black", fg="white", activeforeground="white",
                        cursor="hand2",command=lambda: controller.show_frame("Change_pass")).place(x=50, y=90, width=180, height=30)

        reg = Label(Otp_frame, text="Didn't receive code?", font=("times new roman", 10), bg="salmon",
                    fg="black").place(x=40, y=150)
        request_code = Button(Otp_frame, text="Request again", font=("times new roman", 11), bg="salmon", fg="white",
                         bd=0, activebackground="salmon", activeforeground="white").place(x=150, y=150)

        #--------------------Forget frame2-------------
        Otp_frame2 = Label(self, bd=0, relief=RIDGE, bg="salmon")
        Otp_frame2.place(x=350, y=80, width=400, height=150)

        titel = Label(Otp_frame2, text="ACCOUNT", font=("Comic Sans MS", 30, "bold"), bg="salmon", fg="black").place(x=0, y=0,relwidth=1)
        titel = Label(Otp_frame2, text="VERIFICATION", font=("Comic Sans MS", 30, "bold"), bg="salmon", fg="black").place(x=0, y=50, relwidth=1)

