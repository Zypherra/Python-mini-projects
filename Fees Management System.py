import pyodbc

conn=pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-2VKUOAN\\SQL2008R2;'
    'DATABASE=FeesManagement;'
    'Trusted_Connection=yes;'
)
cursor=conn.cursor()
print("Connected to SQL Server Successfully!")

def add_student():
    sid=int(input("Enter student id:"))
    name=input("Enter student name:")
    cid=int(input("Enter course id:"))
    paid=int(input("Enter Amount Paid:"))
    cursor.execute('SELECT totalfees FROM dbo.Course WHERE courseid=?',(cid))
    data=cursor.fetchone()

    if data:
        total=data[0]
        balance=total-paid
    
    cursor.execute('INSERT INTO Student VALUES (?,?,?,?,?)',(sid,name,cid,paid,balance))
    conn.commit()
    print("Student added Successfully!")

def add_course():
    cid=int(input("Enter Course id:"))
    cname=input("Enter Course Name:")
    totalfees=int(input("Enter total fees of the Course:"))
    cursor.execute("INSERT INTO Course VALUES(?,?,?)",(cid,cname,totalfees))
    conn.commit()
    print("Course added Successfully!")

def rem_student():
    sid=int(input("Enter ID of Student you want to remove:"))
    cursor.execute("DELETE FROM Student WHERE studentid=?",(sid,))
    conn.commit()
    print("Student deleted from database Successfully!")

def rem_course():
    cid=int(input("Enter ID of Course you want to delete:"))
    cursor.execute("DELETE FROM Student WHERE courseid=?",(cid,))
    conn.commit()
    cursor.execute("DELETE FROM Course WHERE courseid=?",(cid,))
    conn.commit()
    print("Course and Students pursuing that Course are deleted from database Successfully!")

def display_all():
    cursor.execute("SELECT * FROM Student inner join Course ON Student.courseid=Course.courseid ORDER BY Student.courseid")
    rows=cursor.fetchall()
    if not rows:
        print("No Data Available!")
    else:
        print(f"{'Student ID':<10}|{'Student Name':<20}|{'Course ID':<10}|{'Course Name':<20}|{'Total Fees':<10}|{'Fees Paid':<10}|{'Balance':<10}")
        print('-'*85)
        for row in rows:
            print(f"{row.studentid:<10}|{row.sname:<20}|{row.courseid:<10}|{row.coursename:<20}|{row.totalfees:<10}|{row.feespaid:<10}|{row.balance:<10}")
    print()

def display_defaulters():
    cursor.execute("SELECT * FROM Student inner join Course ON (Student.courseid=Course.courseid AND Student.balance>0) ORDER BY Student.courseid")
    rows=cursor.fetchall()
    if not rows:
        print("No Data Available!")
    else:
        print(f"{'Student ID':<10}|{'Student Name':<20}|{'Course ID':<10}|{'Course Name':<20}|{'Total Fees':<10}|{'Fees Paid':<10}|{'Balance':<10}")
        print('-'*85)
        for row in rows:
            print(f"{row.studentid:<10}|{row.sname:<20}|{row.courseid:<10}|{row.coursename:<20}|{row.totalfees:<10}|{row.feespaid:<10}|{row.balance:<10}")
    print()

def display_courses():
    cursor.execute("SELECT * FROM Course")
    rows=cursor.fetchall()
    if not rows:
        print("No Course Data Available!")
    else:
        print(f"{'Course ID':<10}|{'Course Name':<20}|{'Total Fees':<10}")
        print('-'*40)
        for row in rows:
            print(f"{row.courseid:<10}|{row.coursename:<20}|{row.totalfees:<10}")
    print()

def main_menu():
    while True:
        print("--------FEE MANAGEMENT SYSTEM--------")
        print("1 - Add a new student")
        print("2 - Add a new course")
        print("3 - Remove an existing student")
        print("4 - Remove an existing course")
        print("5 - Display all Students information")
        print("6 - Display Fee Defaulter Students information")
        print("7 - Display All Available Courses")
        print("0 - Exit")
        choice=int(input("Enter your choice:"))
        if choice==1:
            add_student()
        elif choice==2:
            add_course()
        elif choice==3:
            rem_student()
        elif choice==4:
            rem_course()
        elif choice==5:
            display_all()
        elif choice==6:
            display_defaulters()
        elif choice==7:
            display_courses()
        elif choice==0:
            print("Thank you for using our services!")
            break
        else:
            print("Invalid Choice!")

def login():
    print("User, Please Login:")
    user_name='Parth Nag'
    user_age=20
    user_password='147258'
    name=input("Enter your name:")
    age=int(input("Enter your age:"))
    password=input("Enter Your Password:")
    if name==user_name and age==user_age and password==user_password:
        print()
        print("Welcome to Fees Management System")
        print()
        main_menu()
    else:
        print("ACCESS DENIED!")

login()
conn.close()