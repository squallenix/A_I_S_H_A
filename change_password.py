from tkinter import *
from tkinter import Label
from tkinter import messagebox
from PIL import Image,ImageTk
import customtkinter as ctk
import tkinter as tk
from email_store import email_store
import sql_repo
class Change_pass(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.New_password = tk.StringVar()
        self.Confirm_password = tk.StringVar()
        #----------------------IMAGE PART-------------------------------

        self.phone_image = ImageTk.PhotoImage(file=r"E:\Code\Project\Advanced_intelligent assistant\A_I_S_H_A\images\change_pass.png")
        self.lbl_img1=Label(self,image=self.phone_image,bg='#333333',bd=0).place(x=90,y=60,width=750,height=500)


        #----------------------Login Frame------------------------------

        Cnpass_frame = Label(self,bd=0,relief=RIDGE,bg="black")
        Cnpass_frame.place(x=820,y=60,width=360,height=500)

        titel = Label(Cnpass_frame,text="CREATE A \n NEW PASSWORD",font=("Comic Sans MS",20,"bold"),bg="black",fg="white").place(x=0,y=25,relwidth=1)



        New_password = Label(Cnpass_frame, text="New Password", font=("Andalus,15"), bg="black", fg="white").place(x=80,y=120)
        
        New_pas = Entry(Cnpass_frame, textvariable=self.New_password, font=("times new roman", 15),bg="#ECECEC").place(x=80, y=160)

        Comfirm_password = Label(Cnpass_frame, text="Confirm Password", font=("Andalus,15"), bg="black", fg="white").place(x=80,y=200)
        
        Cpas = Entry(Cnpass_frame, textvariable=self.Confirm_password, font=("times new roman", 15),bg="#ECECEC").place(x=80, y=240)

        button = Button(Cnpass_frame,command=lambda: self.change_password_action(controller),text="CONFIRM",font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground="#00B0F0",fg="white",activeforeground="white",cursor="hand2").place(x=95,y=300,width=180,height=30)

        reg = Label(Cnpass_frame, text="Didn't receive code?", font=("times new roman", 10), bg="black",
                    fg="white").place(x=105, y=360)
        login = Button(Cnpass_frame, text="Enter Email again", font=("times new roman", 11), bg="black", fg="#00B0F0",
                              bd=0, activebackground="black", activeforeground="#00B0F0",command=lambda: controller.show_frame("Forget_pass")).place(x=215, y=360)


    def change_password_action(self, controller):
        if self.New_password.get() == "" or self.Confirm_password.get() == "":
            messagebox.showerror(
                "Error",
                "All fields are required"
            )
            return
        if self.New_password.get() != self.Confirm_password.get():
            messagebox.showerror(
                "Error",
                "Passwords do not match"
            )
            return
        
        state = email_store()
        user_email = state.verified_email
        print("DEBUG: Changing password for email:", user_email)  # <-- check this

        if not user_email:
            messagebox.showerror("Error", "No email found. Go back and request OTP again.")
            return
        sql_repo.SQLRepository.update_password(user_email, self.New_password.get())

        messagebox.showinfo("Success", "Password changed successfully")

        # Clear the temporary session
        state.reset()

        controller.show_frame("Login")

