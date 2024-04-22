from tkinter import *
from tkinter import messagebox
from tkinter_uix.Entry import Entry
import mysql.connector as sql
from modules.register import *
from modules.recruiter import *
from modules.client import *
from modules.creds import user_pwd
from tkinter_uix.Entry import Entry


def success(root, email1):
    global f
    f1.destroy()
    try:
        r1.destroy()
    except:
        pass

    s = f'select usertype from User where email="{email1}"'
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='jobmagnet')
    cur = mycon.cursor()
    cur.execute(s)
    q = cur.fetchall()
    mycon.close()
    print(q)

    if q[0][0] == "Emp":
        emp(root, email1)
    else:
        jobseeker(root, email1)


def submit(root):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='jobmagnet')
    cur = mycon.cursor()
    cur.execute('select Email,Password from User')
    total = cur.fetchall()
    mycon.close()
    email1 = email.get()
    password = pwd.get()
    if email1 and password:
        for i in total:
            if email1 == i[0] and password == i[1]:
                return success(root, email1)
            elif email1 == i[0] and password != i[1]:
                messagebox.showinfo('Alert!', 'Invalid Credentials')
                break
        else:
            messagebox.showinfo(
                'Alert!', 'Email is not registered, Please register')
    else:
        messagebox.showinfo(
            'Alert!', 'Please Enter both Email and Password')


def reg(root):
    try:
        f1.destroy()
    except:
        pass
    mai(root)


def log(root):
    global f1, email, pwd
    try:
        f2.destroy()
    except:
        pass
    f1 = Frame(root, width=1050, height=700, bg='#FFFFFF')
    f1.place(x=0, y=0)

    # Background
    f1.render = PhotoImage(file='elements\\bg.png')
    img = Label(f1, image=f1.render)
    img.place(x=0, y=0)

    # Email
    email_l = Label(f1, text="Email : ", bg='#333333',
                    font=('normal', 20, 'bold'), fg="#00B9ED")
    email_l.place(x=610, y=300)
    email = Entry(f1, width=24, placeholder="Enter your Email..")
    email.place(x=730, y=300)

    # Password
    pwd_l = Label(f1, text="Password : ", bg='#333333',
                  font=('normal', 20, 'bold'), fg="#00B9ED")
    pwd_l.place(x=555, y=350)
    pwd = Entry(f1, show="*", width=24, placeholder="Enter your Password..")
    pwd.place(x=730, y=350)

    # Buttons
    f1.bn = PhotoImage(file="elements\\login2.png")
    btn = Button(f1, image=f1.bn, bg="#333333", bd=0,
                 activebackground="#E0E0E0", command=lambda: submit(root))
    btn.place(x=820, y=420)

    f1.bn1 = PhotoImage(file="elements\\reg.png")
    btn1 = Button(f1, image=f1.bn1, bg="#333333", bd=0,
                  activebackground="#E0E0E0", command=lambda: reg(root))
    btn1.place(x=620, y=420)
