from tkinter import *
from tkinter import ttk
from tkinter import messagebox, Label
from tkinter_uix.Entry import Entry
import mysql.connector as sql
import modules.login as l
from modules.creds import user_pwd
import tkinter as tk
from tkinter import simpledialog


def get_recruiter_details(email):
    global recruiter_id, name, company
    query = f'''
        SELECT emp.employer_id, emp.company_name, usr.Username 
        FROM jobmagnet.Employer AS emp
        JOIN jobmagnet.User AS usr ON emp.UserID = usr.UserID
        WHERE usr.Email = "{email}"
    '''
    mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
    cur = mycon.cursor()
    cur.execute(query)
    result = cur.fetchone()
    mycon.close()

    if result:
        recruiter_id = result[0]
        company = result[1]
        name = result[2]
        return True
    else:
        return False
def logi(root):
    try:
        bg.destroy()
    except:
        pass
    l.log(root)


def submit_job():
    global role1, loc1, desc1, req1, close_date1
    role1 = role.get()
    loc1 = loc.get()
    desc1 = desc.get()
    req1 = req.get()
    close_date1 = close_date.get()

    if role1 and loc1 and desc1 and req1 and close_date1:
        if recruiter_id:
            query = f'INSERT INTO jobmagnet.Job_Posting (title, location, description, requirements, closing_date, employer_id) VALUES ("{role1}", "{loc1}", "{desc1}", "{req1}", "{close_date1}", {recruiter_id})'
            try:
                mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
                cur = mycon.cursor()
                cur.execute(query)
                mycon.commit()
                mycon.close()
                messagebox.showinfo('SUCCESS!', 'You have successfully created a job posting.')
            except Exception as e:
                messagebox.showerror('Error', f'An error occurred: {str(e)}')
        else:
            messagebox.showerror('Error', 'Recruiter details not found.')
    else:
        messagebox.showerror('Error', 'All fields are mandatory.')

def sort_all(table):
    criteria = search_d.get()
    if(criteria == "Select"):
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
        cur = mycon.cursor()
        cur.execute(f'SELECT job_id, title, location, description, requirements, closing_date FROM jobmagnet.Job_Posting WHERE employer_id={recruiter_id} ORDER BY {criteria}')
        all_jobs = cur.fetchall()
        mycon.close()

        for r in all_jobs:
            table.insert('', 'end', values=r)

def sort_applicants(table):
    criteria = search_d.get()
    if(criteria == "Select"):
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
        cur = mycon.cursor()
        cur.execute(f'SELECT job.title AS JobRole, jobseeker.Username, jobseeker.Email, jobseeker.Age, jobseeker.Location, jobseeker.Experience, jobseeker.Skills, jobseeker.Education FROM jobmagnet.Application AS app JOIN jobmagnet.Jobseeker AS jobseeker ON app.jobseeker_id = jobseeker.jobseeker_id JOIN jobmagnet.Job_Posting AS job ON job.job_id = app.job_id WHERE job.employer_id = {recruiter_id} ORDER BY {criteria};')
        applicants = cur.fetchall()
        mycon.close()

        for x in applicants:
            table.insert('', 'end', values=x)

# ----------------------------------------------Posted jobs Query-----------------------------------------------


import datetime

def format_closing_date(closing_date):
    # Check if closing_date is already a string
    if isinstance(closing_date, str):
        try:
            formatted_date = datetime.datetime.strptime(closing_date, '%Y-%m-%d').strftime('%b %d, %Y')
            return formatted_date
        except ValueError:
            return closing_date  # Return as is if unable to parse
    elif isinstance(closing_date, datetime.date):
        # If closing_date is datetime.date, convert it to string and then format
        formatted_date = closing_date.strftime('%b %d, %Y')
        return formatted_date
    else:
        return str(closing_date)  # Return as is if not recognized

def show_all(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='jobmagnet')
    cur = mycon.cursor()
    cur.execute(
        f'SELECT job_id, title, location, description, requirements, closing_date FROM jobmagnet.Job_Posting WHERE employer_id={recruiter_id}')
    all_jobs = cur.fetchall()
    mycon.close()
    for r in all_jobs:
        # Format closing date before displaying
        r = list(r)
        r[-1] = format_closing_date(r[-1])
        table.insert('', 'end', values=r)

def show_applicants(table):
    mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
    cur = mycon.cursor()
    cur.execute(f'''SELECT job.title, user.Username, user.Email, jobseeker.Location, jobseeker.Education, jobseeker.Skills, app.resume_file, app.application_status, job.closing_date
                    FROM jobmagnet.Application AS app
                    JOIN jobmagnet.Jobseeker AS jobseeker ON app.jobseeker_id = jobseeker.jobseeker_id
                    JOIN jobmagnet.Job_Posting AS job ON job.job_id = app.job_id
                    JOIN jobmagnet.User AS user ON jobseeker.UserID = user.UserID
                    WHERE job.employer_id = {recruiter_id};
                ''')
    applicants = cur.fetchall()
    mycon.close()
    for x in applicants:
        # Format closing date before displaying
        x = list(x)
        x[-1] = format_closing_date(x[-1])
        table.insert('', 'end', values=x)

def change_application_status(table):
    # Get the selected item
    selected_index = table.focus()
    selected_values = table.item(selected_index, 'values')
    
    # Check if an item is selected
    if selected_values:
        application_id = selected_values[0] 
        current_status = selected_values[-2]
        if current_status != "Pending":
            messagebox.showinfo("Cannot Change Status", "The application status can only be changed if it's currently pending.")
            return
        
        new_status = askstatus()
        if new_status not in ["Accepted", "Rejected"]:
            messagebox.showinfo("Invalid Status", "Please enter a valid status (Accepted/Rejected).")
            return
        
        if new_status:
            update_application_status(application_id, new_status)
            # Refresh the table
            show_applicants(table)
    else:
        messagebox.showinfo("No Selection", "Please select an application to change its status.")

def create():
    global role, loc, desc, req, close_date
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    # Create Form
    f1 = Frame(rt, width=520)
    f1.load = PhotoImage(file="elements\\create.png")
    img = Label(rt, image=f1.load, bg="#FFFFFF")
    img.grid(row=0, column=1, padx=150, pady=10)

    # Form
    # Labels
    role_l = Label(tab, text="Role :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    role_l.grid(row=0, column=0, pady=10, padx=10, sticky="e")
    loc_l = Label(tab, text="Location :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    loc_l.grid(row=1, column=0, pady=10, padx=10, sticky="e")
    desc_l = Label(tab, text="Description :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    desc_l.grid(row=2, column=0, pady=10, padx=10, sticky="e")
    req_l = Label(tab, text="Requirements :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    req_l.grid(row=3, column=0, pady=10, padx=10, sticky="e")
    close_date_l = Label(tab, text="Closing Date:", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    close_date_l.grid(row=4, column=0, pady=10, padx=10, sticky="e")

    # Entries
    role = Entry(tab, placeholder="Enter Job Role")
    role.grid(row=0, column=1, pady=10, padx=10)
    loc = Entry(tab, placeholder="Enter Job Location")
    loc.grid(row=1, column=1, pady=10, padx=10)
    desc = Entry(tab, placeholder="Enter Job Description")
    desc.grid(row=2, column=1, pady=10, padx=10)
    req = Entry(tab, placeholder="Enter Job Requirements")
    req.grid(row=3, column=1, pady=10, padx=10)
    close_date = Entry(tab, placeholder="Enter Closing Date(YYYY-MM-DD)")
    close_date.grid(row=4, column=1, pady=10, padx=10)

    btn = Button(tab, text="Submit", font=(20), bg="#45CE30",
                fg="#FFFFFF", command=submit_job)
    btn.grid(row=5, column=1, pady=15, sticky="w")

def deletjob(table):
    selectedindex = table.focus()
    selectedvalues = table.item(selectedindex, 'values')
    ajid = selectedvalues[0]
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='jobmagnet')
    cur = mycon.cursor()
    cur.execute(f'delete from jobmagnet.Application where jid={ajid}')
    cur.execute(f'delete from jobmagnet.Job_Posting where job_id={ajid}')
    mycon.commit()
    mycon.close()
    messagebox.showinfo('Thanks', 'Your Job has been Deleted')
    posted()

def posted():
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    search_l = Label(rt, text="Order By : ", font=(
        'normal', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(rt, width=12, font=(
        'normal', 18), state='readonly')
    search_d['values'] = ('Select', 'title', 'location')
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=0, pady=10)
    search = Button(rt, text="Sort", font=('normal', 12, 'bold'),
                    bg="#00b9ed", fg="#ffffff", command=lambda: sort_all(table))
    search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)
    dlt = Button(rt, text="Delete", font=('normal', 12, 'bold'),
                 bg="#00b9ed", fg="#ffffff", command=lambda: deletjob(table))
    dlt.grid(row=0, column=4, padx=10, pady=10, ipadx=5)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('JobID', 'Title', 'Location', 'Description', 'Requirements', 'Closing Date'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("JobID", text="JobID")
    table.heading("Title", text="Title")
    table.heading("Location", text='Location')
    table.heading("Description", text='Description')
    table.heading("Requirements", text='Requirements')
    table.heading("Closing Date", text='Closing Date')

    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("JobID", width=100)
    table.column("Title", width=150)
    table.column("Location", width=150)
    table.column("Description", width=200)
    table.column("Requirements", width=200)
    table.column("Closing Date", width=150)
    show_all(table)
    table.pack(fill="both", expand=1)

def app():
    # Clear existing widgets
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    # Create widgets for sorting
    search_l = Label(rt, text="Order By : ", font=('normal', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    
    search_d = ttk.Combobox(rt, width=12, font=('normal', 18), state='readonly')
    search_d['values'] = ('Select', 'JobRole', 'CName', 'CLocation')
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=10, pady=10)
    
    search = Button(rt, text="Sort", font=('normal', 12, 'bold'), bg="#00b9ed", fg="#ffffff", command=lambda: sort_applicants(table))
    search.grid(row=0, column=3, padx=45, pady=10, ipadx=30)

    # Create widgets for the table
    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")
    
    table = ttk.Treeview(tab, columns=('JobRole', 'CName', 'CEmail', 'Location', 'CExp', 'CSkills', 'CQualification', 'Resume File'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")

    table.heading("JobRole", text="Job Role")
    table.heading("CName", text='Applicants Name')
    table.heading("CEmail", text='Email')
    table.heading("Location", text='Location')
    table.heading("CExp", text='Experience')
    table.heading("CSkills", text='Skills')
    table.heading("CQualification", text='Qualification')
    table.heading("Resume File", text='Resume File')
    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("JobRole", width=150)
    table.column("CName", width=200)
    table.column("CEmail", width=100)
    table.column("Location", width=150)
    table.column("CExp", width=100)
    table.column("CSkills", width=200)
    table.column("CQualification", width=150)
    table.column("Resume File", width=150)

    # Create a Change Status button
    change_status_btn = Button(rt, text="Change Status", font=('normal', 12, 'bold'), bg="#00b9ed", fg="#ffffff", command=lambda: change_application_status(table))
    change_status_btn.grid(row=0, column=4, padx=10, pady=10, ipadx=30)

    show_applicants(table)
    table.pack(fill="both", expand=1)
def askstatus():
    root = tk.Tk()
    root.withdraw()  
    new_status = simpledialog.askstring("Update Application Status", "Enter the new status (Accepted/Rejected/Pending): ")
    return new_status
def update_application_status(application_id, new_status):
    try:
        mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
        cur = mycon.cursor()
        
        # Use parameterized query to prevent SQL injection
        query = 'UPDATE jobmagnet.Application SET application_status=%s WHERE application_id=%s'
        cur.execute(query, (new_status, application_id))
        
        mycon.commit()
        mycon.close()
        
        messagebox.showinfo('Success', f'Application status updated to {new_status}')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {str(e)}')



def emp(root, email1):
    global email
    email = email1
    bg = Frame(root, width=1050, height=700, bg="#333333")
    bg.place(x=0, y=0)

    get_recruiter_details(email)

    # Navbar
    nm = Label(root, text=f'{name}', font=('normal', 36, 'bold'), bg="#333333", fg="#FFFFFF")
    nm.place(x=300, y=50)
    cp = Label(root, text=f'{company}',font=('normal', 36, 'bold'), bg="#333333", fg="#FFFFFF")
    cp.place(x=300, y=120)
    bn = Button(root, text="LOGOUT", font=('normal', 20), bg="#b32e2e", fg="#ffffff", command=lambda: logi(root))
    bn.place(x=800, y=75)

    # Left
    lf = Frame(root, width=330, height=440, bg="#333333")  # Set background color to grey
    lf.place(x=60, y=220)
    cj = Button(lf, text="Post a Job", font=('normal', 20), bg="#b32e2e", fg="#ffffff", command=create)
    cj.grid(row=0, column=0, padx=20, pady=20)  # Adjust padding
    pj = Button(lf, text="Posted Jobs", font=('normal', 20), bg="#b32e2e", fg="#ffffff", command=posted)
    pj.grid(row=1, column=0, padx=20, pady=20)  # Adjust padding
    ap = Button(lf, text="Applications", font=('normal', 20), bg="#b32e2e", fg="#ffffff", command=app)
    ap.grid(row=2, column=0, padx=20, pady=20)  # Adjust padding

    # Right
    global rt, tab, bgr
    rt = Frame(root, width=540, height=420, bg="#333333")  # Set background color to grey
    rt.place(x=450, y=220)
    tab = Frame(root, bg="#333333")  # Set background color to grey
    tab.place(x=460, y=300, width=520, height=350)
     
    bgrf = Frame(root, width=540, height=420)
    bgrf.load = PhotoImage(file="elements\\bgr.png")
    bgr = Label(root, image=bgrf.load, bg="#00b9ed")
    bgr.place(x=440, y=210)