from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from customtkinter import *
from tkinter import ttk


Frame = Tk()
Frame.geometry("400x500+0+0")
Frame.resizable(False, False)
Frame.configure(bg="white")


setting = CTkLabel(Frame, text="Setting", font=("Helvetica", 25))
setting.place(x=140, y=13)


phone_image = ImageTk.PhotoImage(file=r"E:\Code\Project\Advanced_intelligent assistant\A_I_S_H_A\images\rsz_setting.png")

lbl_img1 = Label(Frame, image=phone_image,bg='white')
lbl_img1.image = phone_image
lbl_img1.place(x=218, y=10,height=50,width=50)

theme_mode  = CTkLabel(Frame, text="⚫Theme Mode", font=("Helvetica", 15))
theme_mode.place(x=25, y=90)

list1 = ['Dark Mode','Default']

theme_mode_listbox = ttk.Combobox(Frame,values=list1,state="readonly")
theme_mode_listbox.place(x=140, y=140)
theme_mode_listbox.set("Select Mode")

theme_mode_listbox.place(x=140, y=95)

list2 = ['English','Bengali','Japanese',
        'Hindi','Urdu','Nepali','Mandarin Chinese','Indonesian ']
translate  = CTkLabel(Frame, text="⚫Translate", font=("Helvetica", 15))
translate.place(x=25, y=135)

translate_Combobox = ttk.Combobox(Frame,values=list2,state="readonly")
translate_Combobox.place(x=140, y=140)
translate_Combobox.set("Select Language")

change_pass  = CTkLabel(Frame, text="⚫ ", font=("Helvetica", 15))
change_pass.place(x=25, y=175)
change_pass_button=Button(Frame, text="Change Password", font=("Helvetica", 11),bg="white", fg="cyan3", bd=0,
                          activebackground="white",activeforeground="cyan3",cursor="hand2").place(x=50,y=175)

about  = CTkLabel(Frame, text="⚫ ", font=("Helvetica", 15))
about.place(x=25, y=255)
about_button=Button(Frame, text="About", font=("Helvetica", 11),bg="white", fg="cyan3", bd=0,
                          activebackground="white",activeforeground="cyan3",cursor="hand2").place(x=50,y=255)


shortcut  = CTkLabel(Frame, text="⚫ Shortcuts", font=("Helvetica", 15))
shortcut.place(x=25, y=300)
shortcut_astn  = CTkLabel(Frame, text="Open assistant                        ctrl+space", font=("Helvetica", 12))
shortcut_astn.place(x=75, y=330)
shortcut_chatnewline  = CTkLabel(Frame, text="Chat new line                           shift+enter", font=("Helvetica", 12))
shortcut_chatnewline.place(x=75, y=355)
Frame.mainloop()
