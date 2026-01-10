from tkinter import *
import tkinter as tk
from tkinter import Label
from tkinter import messagebox
from PIL import Image,ImageTk
import customtkinter as ctk

import sql_repo

class Signup(ctk.CTkFrame):
   def __init__(self, parent, controller):
      super().__init__(parent)
      self.check=tk.BooleanVar()
      self.username = tk.StringVar()
      self.email = tk.StringVar()
      self.gender = tk.StringVar()
      self.password = tk.StringVar()
      self.confirm_password = tk.StringVar()
      self.date_of_birth = tk.StringVar()
      #----------------------IMAGE PART-------------------------------

      self.phone_image = ImageTk.PhotoImage(file=r"E:\Code\Project\Advanced_intelligent assistant\A_I_S_H_A\images\pcpic.png")
      self.lbl_img1=Label(self,image=self.phone_image,bg='#333333').place(x=650,y=60,width=520,height=500)


      #----------------------Login Frame------------------------------

      signupFrame = Label(self,bd=2,relief=RIDGE,bg="black")
      signupFrame.place(x=95,y=60,width=600,height=500)

      titel = Label(signupFrame,text="CREATE AN ACCOUNT",font=("Comic Sans MS",20,"bold"),bg="black",fg="white").place(x=0,y=40,relwidth=1)

      username= Label(signupFrame,text="Username", font=("Andalus,15"),bg="black",fg="white").place(x=50,y=110)
      
      user = Entry(signupFrame,textvariable=self.username,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140)

      mail = Label(signupFrame, text="Email Address", font=("Andalus,15"), bg="black", fg="white").place(x=50, y=170)
      
      email = Entry(signupFrame, textvariable=self.email, font=("times new roman", 15), bg="#ECECEC").place(x=50,y=200)

      Birthday = Label(signupFrame, text="Date of birth", font=("Andalus,15"), bg="black", fg="white").place(x=50, y=230)

      birthday = Entry(signupFrame, textvariable=self.date_of_birth, font=("times new roman", 15), bg="#ECECEC").place(x=50,y=260)

      Gender = Label(signupFrame, text="Gender", font=("Andalus,15"), bg="black", fg="white").place(x=340, y=110)

      gen = Entry(signupFrame,textvariable=self.gender, font=("times new roman", 15), bg="#ECECEC").place(x=340, y=140)

      password = Label(signupFrame, text="Password", font=("Andalus,15"), bg="black", fg="white").place(x=340,y=170)

      pas = Entry(signupFrame, textvariable=self.password, font=("times new roman", 15),bg="#ECECEC").place(x=340, y=200)

      Comfirm_password = Label(signupFrame, text="Confirm Password", font=("Andalus,15"), bg="black", fg="white").place(x=340,y=230)
      
      Cpas = Entry(signupFrame, textvariable=self.confirm_password, font=("times new roman", 15),bg="#ECECEC").place(x=340, y=260)

      Checkbutton(
      signupFrame,
      text="I agree to the Terms & Conditions",
      variable=self.check,
      bg="black",
      fg="white",
      activebackground="black",
      activeforeground="white",
      selectcolor="gray20",   
      font=("Arial Rounded MT Bold",10)
      ).place(x=170, y=330)


      Button(
      signupFrame,
      command=lambda: self.signup_action(controller),
      font=("Arial Rounded MT Bold",15),
      bg="#00B0F0",
      fg="white",
      text="Sign Up",
      cursor="hand2"
      ).place(x=200,y=390,width=180,height=30)
   def signup_action(self, controller):
      if not self.check.get():
         messagebox.showerror(
               "Error",
               "You must agree to the Terms & Conditions"
         )
         return
      if not sql_repo.SQLRepository.fetch_data( self.email.get())is None:
         messagebox.showerror(
               "Error",
               "Email already exists"
         )
         return
      if self.password.get() != self.confirm_password.get():
         messagebox.showerror(
               "Error",
               "Passwords do not match"
         )
         return
      sql_repo.SQLRepository.insert_data( self.username.get(), self.email.get(), self.date_of_birth.get(), self.gender.get(), self.password.get())
      messagebox.showinfo(
               "Success",
               "Account created successfully"
         )
      controller.show_frame("Login")