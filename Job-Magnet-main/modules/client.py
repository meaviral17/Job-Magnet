from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector as sql
import modules.login as l
from modules.creds import user_pwd
from tkinter import filedialog 
name = None
location = None
clicid = None

def get_details(email):
    global name, location, clicid
    q = f'SELECT User.Username, Jobseeker.Location, Jobseeker.jobseeker_id FROM User JOIN Jobseeker ON User.UserID=Jobseeker.UserID WHERE User.Email="{email}"'
    mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
    cur = mycon.cursor()
    cur.execute(q)
    d = cur.fetchone()
    mycon.close()
    name = d[0]
    location = d[1]
    clicid = d[2]

def logi(root):
    try:
        bg.destroy()
    except:
        pass
    l.log(root)

def apply(table):
    def upload_resume():
        resume_file_path = filedialog.askopenfilename()
        resume_file_entry.insert(END, resume_file_path)

    def submit_application():
        # Retrieve input values
        cover_letter_text = cover_letter_entry.get("1.0", "end-1c")
        # Get the selected row from the table
        selected_item = table.focus()
        # Retrieve the job ID (ajid) from the selected row's data
        ajid = table.item(selected_item, 'values')[0]  # Assuming the job ID is in the first column
        # Assuming you have a resume file input widget, retrieve its value
        resume_file_path = resume_file_entry.get()

        # Check if cover letter and resume are provided
        if cover_letter_text.strip() == "":
            messagebox.showwarning("Missing Information", "Please provide a cover letter.")
            return
        if resume_file_path == "":
            messagebox.showwarning("Missing Information", "Please upload your resume.")
            return

        # Insert the application into the database
        queryapplyjob = f'INSERT INTO Application (jobseeker_id, job_id, cover_letter, resume_file) ' \
                        f'VALUES ({clicid}, {ajid}, "{cover_letter_text}", "{resume_file_path}")'
        mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
        cur = mycon.cursor()
        cur.execute(queryapplyjob)
        mycon.commit()
        mycon.close()
        messagebox.showinfo('Thanks', 'Your application has been submitted')
        # Close the application window
        app_window.destroy()

    # Create a new window for the application form
    app_window = Toplevel()
    app_window.title("Apply for Job")

    # Cover letter entry
    cover_letter_label = Label(app_window, text="Cover Letter:", font=('normal', 12))
    cover_letter_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    cover_letter_entry = Text(app_window, height=10, width=50)
    cover_letter_entry.grid(row=0, column=1, padx=10, pady=5)

    # Resume file upload
    resume_file_label = Label(app_window, text="Resume:", font=('normal', 12))
    resume_file_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    resume_file_entry = Entry(app_window, width=50)
    resume_file_entry.grid(row=1, column=1, padx=10, pady=5)
    upload_resume_button = Button(app_window, text="Upload Resume", command=upload_resume)
    upload_resume_button.grid(row=1, column=2, padx=5, pady=5)

    # Submit button
    submit_button = Button(app_window, text="Submit", font=('normal', 12, 'bold'), bg="black", fg="#ffffff", command=submit_application)
    submit_button.grid(row=2, column=1, padx=10, pady=10)

    # Ensure that the application window is closed properly
    app_window.protocol("WM_DELETE_WINDOW", lambda: app_window.destroy())
def delet(table):
    selectedindex = table.focus()
    selectedvalues = table.item(selectedindex, 'values')
    aaid = selectedvalues[0]
    mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
    cur = mycon.cursor()
    cur.execute(f'DELETE FROM Application WHERE application_id={aaid}')
    mycon.commit()
    mycon.close()
    messagebox.showinfo('Thanks', 'Your application has been Deleted')
    myapp()

def sort_alljobs(table):
    criteria = search_d.get()
    if criteria == "Select":
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
        cur = mycon.cursor()
        query = f'SELECT jp.job_id, jp.title, jp.description, e.company_name, jp.requirements, jp.closing_date, jp.employer_id \
FROM jobmagnet.Job_Posting jp \
JOIN jobmagnet.Employer e ON jp.employer_id = e.employer_id \
ORDER BY {criteria}'
        cur.execute(query)
        jobs = cur.fetchall()
        mycon.close()
        for i, r in enumerate(jobs):
            table.insert('', i, values=r)

def sort_myapplications(table):
    criteria = search_d.get()
    if criteria == "Select":
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
        cur = mycon.cursor()
        cur.execute(f'SELECT Application.application_id, Job_Posting.title, Job_Posting.description, Employer.company_name, Job_Posting.requirements, Job_Posting.closing_date, Job_Posting.employer_id FROM Application JOIN Job_Posting ON Application.job_id=Job_Posting.job_id JOIN Employer ON Job_Posting.employer_id=Employer.employer_id WHERE Application.jobseeker_id={clicid} ORDER BY {criteria}')
        jobs = cur.fetchall()
        mycon.close()
        for i, r in enumerate(jobs):
            table.insert('', i, values=r)

def showalljobs(table):
    mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
    cur = mycon.cursor()
    cur.execute(f'SELECT Job_Posting.job_id, Job_Posting.title, Job_Posting.description, Employer.company_name, Job_Posting.requirements, Job_Posting.closing_date, Job_Posting.employer_id FROM Job_Posting JOIN Employer ON Job_Posting.employer_id=Employer.employer_id')
    jobs = cur.fetchall()
    mycon.close()
    for i, r in enumerate(jobs):
        table.insert('', i, values=r)

def show_myapplications(table):
    mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
    cur = mycon.cursor()
    cur.execute(f'SELECT Application.application_id, Job_Posting.title, Job_Posting.description, Employer.company_name, Job_Posting.requirements, Job_Posting.closing_date, Job_Posting.employer_id FROM Application JOIN Job_Posting ON Application.job_id=Job_Posting.job_id JOIN Employer ON Job_Posting.employer_id=Employer.employer_id WHERE Application.jobseeker_id={clicid}')
    applications = cur.fetchall()
    mycon.close()
    for i, r in enumerate(applications):
        table.insert('', i, values=r)

def available():
    global rt, tab, bgr
    mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    search_l = Label(rt, text="Order By : ", font=('normal', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(rt, width=12, font=('normal', 18), state='readonly')
    search_d['values'] = ('Select', 'title', 'description', 'Location')
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=0, pady=10)
    search = Button(rt, text="Sort", font=('normal', 12, 'bold'), bg="black", fg="#ffffff", command=lambda: sort_alljobs(table))
    search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)

    apl = Button(rt, text="Apply", font=('normal', 12, 'bold'), bg="black", fg="#ffffff", command=lambda: apply(table))
    apl.grid(row=0, column=4, padx=10, pady=10, ipadx=5)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('job_id', 'title', 'description', 'company_name', 'Location', 'requirements', 'closing_date', 'employer_id'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("job_id", text="Job ID")
    table.heading("title", text="Title")
    table.heading("description", text="Description")
    table.heading("company_name", text='Company Name')
    table.heading("Location", text="Location")
    table.heading("requirements", text='Requirements')
    table.heading("closing_date", text='Closing Date')
    table.heading("employer_id", text="Employer ID")
    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("job_id", width=100)
    table.column("title", width=150)
    table.column("description", width=150)
    table.column("company_name", width=150)
    table.column("Location", width=150)
    table.column("requirements", width=100)
    table.column("closing_date", width=100)
    table.column("employer_id", width=150)
    showalljobs(table)
    table.pack(fill="both", expand=1)

def myapp():
    global rt, tab, bgr
    mycon = sql.connect(host='localhost', user='root', passwd=user_pwd, database='jobmagnet')
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    search_l = Label(rt, text="Order By : ", font=('normal', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(rt, width=12, font=('normal', 18), state='readonly')
    search_d['values'] = ('Select', 'title', 'description', 'Location')
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=0, pady=10)
    search = Button(rt, text="Sort", font=('normal', 12, 'bold'), bg="black", fg="#ffffff", command=lambda: sort_myapplications(table))
    search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)

    dlt = Button(rt, text="Delete", font=('normal', 12, 'bold'), bg="black", fg="#ffffff", command=lambda: delet(table))
    dlt.grid(row=0, column=4, padx=10, pady=10, ipadx=5)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('application_id', 'title', 'description', 'company_name', 'Location', 'requirements', 'closing_date', 'employer_id'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("application_id", text="Application ID")
    table.heading("title", text="Title")
    table.heading("description", text="Description")
    table.heading("company_name", text='Company Name')
    table.heading("Location", text="Location")
    table.heading("requirements", text='Requirements')
    table.heading("closing_date", text='Closing Date')
    table.heading("employer_id", text="Employer ID")
    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("application_id", width=50)
    table.column("title", width=150)
    table.column("description", width=150)
    table.column("company_name", width=150)
    table.column("Location", width=150)
    table.column("requirements", width=100)
    table.column("closing_date", width=100)
    table.column("employer_id", width=150)
    show_myapplications(table)
    table.pack(fill="both", expand=1)

def jobseeker(root, email1):
    global email, rt, tab, bgr
    email = email1
    bg = Frame(root, width=1050, height=700, bg="black")
    bg.place(x=0, y=0)

    get_details(email)

    bg.load = PhotoImage(file='elements\\bgM.png')
    img = Label(root, image=bg.load)
    img.place(x=0, y=0)

    nm = Label(root, text=f'{name}', font=('normal', 36, 'bold'), bg="#ffffff", fg="#0A3D62")
    nm.place(x=300, y=50)
    cp = Label(root, text=f'{location}', font=('normal', 24), bg="#ffffff", fg="#0A3D62")
    cp.place(x=300, y=120)
    bn = Button(root, text="LOGOUT", font=('normal', 20), bg="#b32e2e", fg="#ffffff", command=lambda: logi(root))
    bn.place(x=800, y=75)

    lf = Frame(root, width=330, height=440, bg="#B0B0B0")
    lf.place(x=60, y=240)
    pj = Button(lf, text="Available Jobs", font=('normal', 20), bg="#b32e2e", fg="#ffffff", command=available)
    pj.grid(row=0, column=0, padx=60, pady=70)
    ap = Button(lf, text="My Applications", font=('normal', 20), bg="#b32e2e", fg="#ffffff", command=myapp)
    ap.grid(row=1, column=0, padx=60, pady=70)

    rt = Frame(root, width=540, height=420, bg="black")
    rt.place(x=450, y=220)
    tab = Frame(root, bg="black")
    tab.place(x=460, y=300, width=520, height=350)
    bgrf = Frame(root, width=540, height=420)
    bgrf.load = PhotoImage(file="elements\\bgr.png")
    bgr = Label(root, image=bgrf.load, bg="black") 
    bgr.place(x=440, y=210)
