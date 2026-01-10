from tkinter import *
from tkinter import Label
from tkinter import messagebox
from PIL import Image,ImageTk
import customtkinter as ctk
import tkinter as tk
import random
from email_store import email_store
import otp
import sql_repo

from sib_api_v3_sdk import ApiClient, Configuration
from sib_api_v3_sdk.api.transactional_emails_api import TransactionalEmailsApi
from sib_api_v3_sdk.models import SendSmtpEmail

SENDINBLUE_API_KEY = "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"




class Forget_pass(ctk.CTkFrame):
   def __init__(self, parent, controller):
      super().__init__(parent)
      self.email = tk.StringVar()
      self.otp = None

      #----------------------IMAGE PART-------------------------------

      self.phone_image = ImageTk.PhotoImage(file=r"E:\Code\Project\Advanced_intelligent assistant\A_I_S_H_A\images\Forgetpass1.png")
      self.lbl_img1=Label(self,image=self.phone_image,bg="Slate Gray1").place(x=0,y=160,width=520,height=500)

      self.phone_image2 = ImageTk.PhotoImage(file=r"E:\Code\Project\Advanced_intelligent assistant\A_I_S_H_A\images\Forgetpass2.png")
      self.lbl_img2 = Label(self, image=self.phone_image2, bg="Slate Gray1").place(x=800, y=160, width=450,height=500)


      #----------------------forget Frame1------------------------------

      forget_frame = Label(self,bd=0,relief=RIDGE,bg="Slate Gray1")
      forget_frame.place(x=500,y=215,width=300,height=300)

      mail= Label(forget_frame,text="Email Address", font=("Andalus,15"),bg="Slate Gray1",fg="black").place(x=0,y=10)
      Email = Entry(forget_frame,textvariable=self.email,font=("times new roman",20),bg="#ECECEC").place(x=0,y=40)

      button = Button(forget_frame,  text="RESET", font=("Arial Rounded MT Bold", 15),
                     bg="black", activebackground="black", fg="white", activeforeground="white",
                     cursor="hand2",command=lambda: self.check_email(controller)).place(x=50, y=90, width=180, height=30)

      #--------------------Forget frame2-------------
      forget_frame2 = Label(self, bd=0, relief=RIDGE, bg="Slate Gray1")
      forget_frame2.place(x=350, y=80, width=400, height=150)

      titel = Label(forget_frame2, text="FORGOT", font=("Comic Sans MS", 30, "bold"), bg="Slate Gray1", fg="black").place(x=0, y=0,relwidth=1)
      titel = Label(forget_frame2, text="YOUR PASSWORD", font=("Comic Sans MS", 30, "bold"), bg="Slate Gray1", fg="black").place(x=0, y=50, relwidth=1)

   def generate_otp(self, length=6):
      return str(random.randint(10**(length-1), 10**length - 1))

   def send_otp_email(self, to_email, otp):
      configuration = Configuration()
      configuration.api_key['api-key'] = SENDINBLUE_API_KEY
      api_instance = TransactionalEmailsApi(ApiClient(configuration))

      send_smtp_email = SendSmtpEmail(
         to=[{"email": to_email}],
         sender={"email": "squallenix12@gmail.com"},
         subject="Your OTP Code",
         html_content=f"<p>Your OTP code is <strong>{otp}</strong></p>"
      )
      try:
         api_response = api_instance.send_transac_email(send_smtp_email)
         print(api_response)
         return True
      except Exception as e:
         print("Error sending OTP:", e)
         return False

   def check_email(self, controller):
      user = sql_repo.SQLRepository.fetch_data(self.email.get())
      if user:
         # Generate new OTP
         otp = self.generate_otp()
         sent = self.send_otp_email(self.email.get(), otp)
         
         if sent:
               messagebox.showinfo("Email Found", "An OTP has been sent to your email.")
               state = email_store()
               state.sent_otp = otp
               state.verified_email = self.email.get()
               controller.show_frame("Otp")  
         else:
               messagebox.showerror("Error", "Failed to send OTP. Try again.")
      else:
         messagebox.showerror("Email Not Found", "The provided email does not exist.")


   