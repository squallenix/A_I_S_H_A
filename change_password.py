from tkinter import *
from tkinter import Label
from tkinter import messagebox
from PIL import Image,ImageTk
import customtkinter as ctk

class Change_pass(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        #----------------------IMAGE PART-------------------------------

        self.phone_image = ImageTk.PhotoImage(file="K:\\Code\\Project\\Advanced_intelligent assistant\\change_pass2.png")
        self.lbl_img1=Label(self,image=self.phone_image,bg='#333333',bd=0).place(x=90,y=60,width=750,height=500)


        #----------------------Login Frame------------------------------

        Cnpass_frame = Label(self,bd=0,relief=RIDGE,bg="black")
        Cnpass_frame.place(x=820,y=60,width=360,height=500)

        titel = Label(Cnpass_frame,text="CREATE A \n NEW PASSWORD",font=("Comic Sans MS",20,"bold"),bg="black",fg="white").place(x=0,y=25,relwidth=1)



        New_password = Label(Cnpass_frame, text="New Password", font=("Andalus,15"), bg="black", fg="white").place(x=80,y=120)
        self.New_password = StringVar()
        New_pas = Entry(Cnpass_frame, textvariable=self.New_password, font=("times new roman", 15),bg="#ECECEC").place(x=80, y=160)

        Comfirm_password = Label(Cnpass_frame, text="Confirm Password", font=("Andalus,15"), bg="black", fg="white").place(x=80,y=200)
        self.Confirm_password = StringVar()
        Cpas = Entry(Cnpass_frame, textvariable=self.Confirm_password, font=("times new roman", 15),bg="#ECECEC").place(x=80, y=240)

        button = Button(Cnpass_frame,command=lambda: controller.show_frame("Login"),text="CONFIRM",font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground="#00B0F0",fg="white",activeforeground="white",cursor="hand2").place(x=95,y=300,width=180,height=30)

        reg = Label(Cnpass_frame, text="Didn't receive code?", font=("times new roman", 10), bg="black",
                    fg="white").place(x=105, y=360)
        login = Button(Cnpass_frame, text="SingIn", font=("times new roman", 11), bg="black", fg="#00B0F0",
                              bd=0, activebackground="black", activeforeground="#00B0F0",command=lambda: controller.show_frame("Login")).place(x=215, y=360)



