import customtkinter
from tkinter import *
from tkinter import messagebox
from datetime import date
import database

app = customtkinter.CTk()
app.title('Clinic Management System')
app.geometry('900x350')
app.config(bg='#0A0B0C')
app.iconbitmap('clinic_icon.ico')  # You would need a clinic-themed icon
app.resizable(False, False)

font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 24, 'bold')


app.mainloop()