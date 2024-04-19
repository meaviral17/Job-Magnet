from tkinter import *
from tkinter import messagebox
from modules.login import *

root = Tk()
root.geometry("1050x700")
root.title("Job-Magnet")
root.resizable(0, 0)
root.iconbitmap(r'elements\\favicon.ico')
root.config(bg="black") 
log(root)
root.mainloop()
