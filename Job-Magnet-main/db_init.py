import mysql.connector as sql
from modules.creds import user_pwd
from cv_schema_init import *

mycon = sql.connect(host='localhost', user='root', passwd=user_pwd)
cur = mycon.cursor()
cur.execute(CREATE_SCHEMA)
cur.execute(Create_User_Table)
cur.execute(Create_Employer_Table)
cur.execute(Create_Jobseeker_Table)
cur.execute(Create_Job_Posting_Table)
cur.execute(Create_Application_Table)
mycon.close()