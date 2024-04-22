from tkinter import *
from tkinter import ttk
from tkinter import messagebox, Label
from tkinter_uix.Entry import Entry
import mysql.connector as sql
import modules.login as l
from modules.creds import user_pwd
def logi(root):
    try:
        r2.destroy()
        r3.destroy()
    except:
        pass
    l.log(root)

def mai(root):
    global r1
    r1 = Frame(root, height=700, width=1050)
    r1.place(x=0, y=0)
    r1.render = PhotoImage(file="elements/Registration_bg.png")
    img = Label(r1, image=r1.render)
    img.place(x=0, y=0)
    
    r1.Img1 = PhotoImage(file="elements/recruiter_element.png")
    recruit = Button(r1, image=r1.Img1, border=0, bg="#333333", highlightbackground="#333333",
                     relief="raised", activebackground="#03EAFD", command=lambda: recruiter_regis(root),highlightthickness=0)
    recruit.place(x=100, y=300)
    
    r1.Img2 = PhotoImage(file="elements/client_element.png")
    client_reg = Button(r1, image=r1.Img2, border=0, bg="#333333",highlightthickness=0,highlightbackground="#333333",
                     relief="raised", activebackground="#03EAFD", command=lambda: client_regis(root))
    client_reg.place(x=400, y=300)
    
    r1.bn = PhotoImage(file="elements\\backlogin.png")
    btn = Button(r1, image=r1.bn, bg='#333333',highlightthickness=0, highlightbackground="#333333",
                 bd=0, activebackground="#05e4f6", command=lambda: logi(root))
    btn.place(x=200, y=550)



def recruiter_regis(root):
    global name, email, pwd, cpwd
    print("hello recruiter")
    r1.destroy()
    r2 = Frame(root, height=700, width=1050)
    r2.place(x=0, y=0)
    r2.render = PhotoImage(file="elements/reg_bg.png")
    img = Label(r2, image=r2.render)
    img.place(x=0, y=0)
    name_l = Label(r2, text="Name : ", bg='#FFFFFF', fg="#00B9ED",
                   font=('normal', 20, 'bold'))
    name_l.place(x=100, y=250)
    name = Entry(r2, placeholder='Enter Your Full Name...', width=20)
    name.place(x=290, y=250)

    email_l = Label(r2, text="Email : ", bg='#FFFFFF', fg="#00B9ED",
                    font=('normal', 20, 'bold'))
    email_l.place(x=100, y=300)
    email = Entry(r2, placeholder='Email', width=20)
    email.place(x=290, y=300)

    pwd_l = Label(r2, text="Password : ", bg='#FFFFFF', fg="#00B9ED",
                  font=('normal', 20, 'bold'))
    pwd_l.place(x=100, y=350)
    pwd = Entry(r2, placeholder='Password', show="*", width=20)
    pwd.place(x=290, y=350)

    con_pwd_l = Label(r2, text="Confirm : ", bg='#FFFFFF', fg="#00B9ED",
                      font=('normal', 20, 'bold'))
    con_pwd_l.place(x=100, y=400)
    cpwd = Entry(r2, placeholder='Confirm Password', show="*", width=20)
    cpwd.place(x=290, y=400)

    r2.bn = PhotoImage(file="elements\\next1.png")
    btn = Button(r2, image=r2.bn, bg='#FFFFFF', bd=0, highlightthickness=0, highlightbackground="#333333",
                 activebackground="#ffffff", command=lambda: recruiter_check(root))
    btn.place(x=320, y=500)

    r2.back = PhotoImage(file="elements\\back.png")
    btn2 = Button(r2, image=r2.back, bg='#FFFFFF', bd=0, highlightthickness=0, highlightbackground="#333333",
                  activebackground="#ffffff", command=lambda: mai(root))
    btn2.place(x=120, y=500)


def recruiter_check(root):
    global name1, email1, pwd1, cpwd1
    name1 = name.get()
    email1 = email.get()
    pwd1 = pwd.get()
    cpwd1 = cpwd.get()
    print(name1, email1, pwd1, cpwd1)
    if name1 and email1 and pwd1 and cpwd1:
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='jobmagnet')
        cur = mycon.cursor()
        cur.execute('select Email from User')
        total = cur.fetchall()
        mycon.close()
        exist_email = []
        for i in total:
            exist_email.append(i[0])
        print("existing users:", exist_email)

        if email1 in exist_email:
            messagebox.showinfo('ALERT!', 'EMAIL ALREADY REGISTERED')
            email.delete(0, END)

        else:
            if pwd1 == cpwd1:
                recruit_complete(root)
            else:
                messagebox.showinfo('ALERT!', 'PASSWORDS DO NOT MATCH')

    else:
        messagebox.showinfo('ALERT!', 'ALL FIELDS ARE MUST BE FILLED')

def recruit_complete(root):
    print("hello ", name1, ", Let's complete your profile")
    r3 = Frame(root, height=700, width=1050)
    r3.place(x=0, y=0)
    r3.render = PhotoImage(file="elements/reg_bg.png")
    img = Label(r3, image=r3.render)
    img.place(x=0, y=0)

    global company, loc, company_size, industry, website_url
    company_l = Label(r3, text="Company : ", bg='#FFFFFF', fg="#00B9ED",
                      font=('normal', 20, 'bold'))
    company_l.place(x=100, y=250)
    company = Entry(r3, placeholder='Company', width=20)
    company.place(x=290, y=250)

    loc_l = Label(r3, text="Location : ", bg='#FFFFFF', fg="#00B9ED",
                  font=('normal', 20, 'bold'))
    loc_l.place(x=100, y=300)
    loc = Entry(r3, placeholder='Location', width=20)
    loc.place(x=290, y=300)

    company_size_l = Label(r3, text="Company Size : ", bg='#FFFFFF', fg="#00B9ED",
                      font=('normal', 20, 'bold'))
    company_size_l.place(x=100, y=350)
    company_size = Entry(r3, placeholder='Company Size', width=20)
    company_size.place(x=290, y=350)

    industry_l = Label(r3, text="Industry : ", bg='#FFFFFF', fg="#00B9ED",
                  font=('normal', 20, 'bold'))
    industry_l.place(x=100, y=400)
    industry = Entry(r3, placeholder='Industry', width=20)
    industry.place(x=290, y=400)

    website_url_l = Label(r3, text="Website URL : ", bg='#FFFFFF', fg="#00B9ED",
                  font=('normal', 20, 'bold'))
    website_url_l.place(x=100, y=450)
    website_url = Entry(r3, placeholder='Website URL', width=20)
    website_url.place(x=290, y=450)

    r3.bn = PhotoImage(file="elements\\reg.png")
    btn = Button(r3, image=r3.bn, bg='#FFFFFF', bd=0, highlightthickness=0, highlightbackground="#333333",
                 activebackground="#ffffff", command=lambda: recruiter_submit(root))
    btn.place(x=320, y=500)


def recruiter_submit(root):
    global company1, loc1, company_size1, industry1, website_url1
    company1 = company.get()
    loc1 = loc.get()
    company_size1 = company_size.get()
    industry1 = industry.get()
    website_url1 = website_url.get()
    print(name1, email1, company1, loc1, company_size1, industry1, website_url1)
    if company1 and loc1 and company_size1 and industry1 and website_url1:
        exe = f'insert into User (Username, Email, Password,usertype) values("{name1}","{email1}","{pwd1}","Emp")'
        try:
            mycon = sql.connect(host='localhost', user='root',
                                passwd=user_pwd, database='jobmagnet')
            cur = mycon.cursor()
            cur.execute(exe)
            UserID = cur.lastrowid  # Get the last inserted UserID
            exe1 = f'INSERT INTO Employer (UserID, company_name,location, company_size, industry, website_url) VALUES ({UserID}, "{company1}","{loc1}", {company_size1}, "{industry1}", "{website_url1}")'
            cur.execute(exe1)
            name.delete(0, END)
            email.delete(0, END)
            pwd.delete(0, END)
            cpwd.delete(0, END)
            loc.delete(0, END)
            company.delete(0, END)
            company_size.delete(0, END)
            industry.delete(0, END)
            website_url.delete(0, END)
            mycon.commit()
            mycon.close()
            messagebox.showinfo('SUCCESS!', 'Registration Successful')
            logi(root)
        except Exception as e:
            print(e)
            pass
    else:
        messagebox.showinfo('ALERT!', 'ALL FIELDS ARE MUST BE FILLED')

def client_regis(root):
    global name, email, pwd, cpwd
    print("hello client")
    r1.destroy()
    r2 = Frame(root, height=700, width=1050)
    r2.place(x=0, y=0)
    r2.render = PhotoImage(file="elements/reg_bg.png")
    img = Label(r2, image=r2.render)
    img.place(x=0, y=0)

    name_l = Label(r2, text="Name : ", bg='#FFFFFF', fg="#00B9ED",
                   font=('normal', 20, 'bold'))
    name_l.place(x=100, y=250)
    name = Entry(r2, placeholder='Enter Your Full Name...', width=20)
    name.place(x=290, y=250)

    email_l = Label(r2, text="Email : ", bg='#FFFFFF', fg="#00B9ED",
                    font=('normal', 20, 'bold'))
    email_l.place(x=100, y=300)
    email = Entry(r2, placeholder='Email', width=20)
    email.place(x=290, y=300)

    pwd_l = Label(r2, text="Password : ", bg='#FFFFFF', fg="#00B9ED",
                  font=('normal', 20, 'bold'))
    pwd_l.place(x=100, y=350)
    pwd = Entry(r2, placeholder='Password', show="*", width=20)
    pwd.place(x=290, y=350)

    con_pwd_l = Label(r2, text="Confirm : ", bg='#FFFFFF', fg="#00B9ED",
                      font=('normal', 20, 'bold'))
    con_pwd_l.place(x=100, y=400)
    cpwd = Entry(r2, placeholder='Confirm Password', show="*", width=20)
    cpwd.place(x=290, y=400)

    r2.bn = PhotoImage(file="elements\\next1.png")
    btn = Button(r2, image=r2.bn, bg='#FFFFFF', bd=0, highlightthickness=0, highlightbackground="#333333",
                 activebackground="#ffffff", command=lambda: client_check(root))
    btn.place(x=320, y=500)

    r2.back = PhotoImage(file="elements\\back.png")
    btn2 = Button(r2, image=r2.back, bg='#FFFFFF', bd=0, highlightthickness=0, highlightbackground="#333333",
                  activebackground="#ffffff", command=lambda: mai(root))
    btn2.place(x=120, y=500)


def client_check(root):
    global name1, email1, pwd1, cpwd1
    name1 = name.get()
    email1 = email.get()
    pwd1 = pwd.get()
    cpwd1 = cpwd.get()
    print(name1, email1, pwd1, cpwd1)
    if name1 and email1 and pwd1 and cpwd1:
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='jobmagnet')
        cur = mycon.cursor()
        cur.execute('select Email from user')
        total = cur.fetchall()
        mycon.close()
        exist_email = []
        for i in total:
            exist_email.append(i[0])
        print("existing users:", exist_email)

        if email1 in exist_email:
            messagebox.showinfo('ALERT!', 'EMAIL ALREADY REGISTERED')
            email.delete(0, END)

        else:
            if pwd1 == cpwd1:
                client_complete(root)
            else:
                messagebox.showinfo('ALERT!', 'PASSWORDS DO NOT MATCH')

    else:
        messagebox.showinfo('ALERT!', 'ALL FIELDS ARE MUST BE FILLED')


def client_complete(root):
    print("hello ", name1, ", Let's complete your profile")
    r3 = Frame(root, height=700, width=1050)
    r3.place(x=0, y=0)
    r3.render = PhotoImage(file="elements/reg_bg.png")
    img = Label(r3, image=r3.render)
    img.place(x=0, y=0)

    global loc, resume_url, skills, education
    loc_l = Label(r3, text="Location : ", bg='#FFFFFF', fg="#00B9ED",
                  font=('normal', 20, 'bold'))
    loc_l.place(x=100, y=250)
    loc = Entry(r3, placeholder='Location', width=20)
    loc.place(x=290, y=250)

    resume_url_l = Label(r3, text="Resume URL : ", bg='#FFFFFF', fg="#00B9ED",
                         font=('normal', 20, 'bold'))
    resume_url_l.place(x=100, y=300)
    resume_url = Entry(r3, placeholder='Resume URL', width=20)
    resume_url.place(x=290, y=300)

    skills_l = Label(r3, text="Skills : ", bg='#FFFFFF',
                     fg="#00B9ED", font=('normal', 20, 'bold'))
    skills_l.place(x=100, y=350)
    skills = Entry(r3, placeholder='Skills', width=20)
    skills.place(x=290, y=350)

    education_l = Label(r3, text="Education : ",
                        bg='#FFFFFF', fg="#00B9ED", font=('normal', 20, 'bold'))
    education_l.place(x=100, y=400)
    education = Entry(r3, placeholder='Education', width=20)
    education.place(x=290, y=400)

    r3.bn = PhotoImage(file="elements\\reg.png")
    btn = Button(r3, image=r3.bn, bg='#FFFFFF', bd=0, highlightthickness=0, 
                 activebackground="#ffffff", command=lambda: client_submit(root))
    btn.place(x=320, y=500)


def client_submit(root):
    global loc1, resume_url1, skills1, education1
    loc1 = loc.get()
    resume_url1 = resume_url.get()
    skills1 = skills.get()
    education1 = education.get()
    print(name1, email1, loc1, resume_url1, skills1, education1)
    if loc1 and resume_url1 and skills1 and education1:
        exe = f'insert into user (Username, Email, Password,usertype) values("{name1}","{email1}","{pwd1}","Jbs")'
        try:
            mycon = sql.connect(host='localhost', user='root',
                                passwd=user_pwd, database='jobmagnet')
            cur = mycon.cursor()
            cur.execute(exe)
            UserID = cur.lastrowid  # Get the last inserted UserID
            exe1 = f'insert into Jobseeker (UserID, Location, Resume_url, Skills, Education) values({UserID}, "{loc1}","{resume_url1}","{skills1}","{education1}")'
            cur.execute(exe1)
            name.delete(0, END)
            email.delete(0, END)
            pwd.delete(0, END)
            cpwd.delete(0, END)
            loc.delete(0, END)
            resume_url.delete(0, END)
            skills.delete(0, END)
            education.delete(0, END)
            mycon.commit()
            mycon.close()
            messagebox.showinfo('SUCCESS!', 'Registration Successful')
            logi(root)
        except Exception as e:
            print(e)
            pass

    else:
        messagebox.showinfo('ALERT!', 'ALL FIELDS ARE MUST BE FILLED')

