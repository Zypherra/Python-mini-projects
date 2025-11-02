import pyodbc
from datetime import date
from datetime import datetime

conn=pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-2VKUOAN\\SQL2008R2;'
    'DATABASE=DailyTaskdb;'
    'Trusted_Connection=yes;'
)
cursor=conn.cursor()
print("Connected to SQL Server successfully!")

def add_task():
    name=input("Enter Name:")
    date=input("Enter Date(DD-MM-YYYY):")
    time=input("Enter Time(HH-MM-SS):")
    desc=input("Enter Description:")
    priority=input('Enter Priority(High/Medium/Low):')
    try:
        task_date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
        task_time = datetime.strptime(time, "%H-%M-%S").strftime("%H:%M:%S")
    except ValueError:
        print("Invalid date or time format. Please use DD-MM-YYYY and HH-MM-SS.")
        return
    status='Pending'
    cursor.execute(
        "INSERT INTO Task(taskname,taskdate,tasktime,description,priority,status) VALUES(?,?,?,?,?,?)",
        (name,task_date,task_time,desc,priority,status)
    )
    conn.commit()
    print("Task added successfully!")
    print()

def view_tasks():
    cursor.execute("SELECT * FROM Task ORDER BY taskdate,tasktime")
    rows=cursor.fetchall()
    if not rows:
        print("No Data Available!")
    else:
        print("ALL TASKS:")
        print('-'*50)
        for row in rows:
            print(f"{row.taskid:<10}|{row.taskname:<10}|{row.taskdate:<10}|{row.tasktime:<10}|{row.description:<30}|{row.priority:<10}|{row.status:<10}")
        print("-"*50)
    print()

def view_today_tasks():
    today = date.today().strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM Task WHERE taskdate=?",(today,))
    rows=cursor.fetchall()
    print(f"\nTasks scheduled for {today}")
    if not rows:
        print("No tasks scheduled for Today!")
    else:
        for row in rows:
            print(f"{row.taskid:<10}|{row.taskname:<10}|{row.taskdate:<10}|{row.tasktime:<10}|{row.description:<30}|{row.priority:<10}|{row.status:<10}")
    print("-"*50)
    print()

def mark_task_completed():
    tid=int(input("Enter Task ID to mark task as 'Completed':"))
    cursor.execute("UPDATE Task SET status='Completed' WHERE taskid=?",(tid,))
    conn.commit()
    print("Task Updated Successfully!")
    print()

def delete_task():
    tid=int(input("Enter Task ID to delete task:"))
    cursor.execute("SELECT taskid FROM Task WHERE taskid=?",(tid,))
    found=cursor.fetchone()
    if not found:
        print("Data not available for id =",tid,'!')
    else:
        ch=input("Are You Sure want to delete the task:Press 'Y' for Yes, 'N' for No:")
        if ch=='Y':
            cursor.execute("DELETE FROM Task WHERE taskid=?",(tid,))
            conn.commit()
            print("Task Deleted Successfully!")
    print()

def main_menu():
    while True:
        print("\n--------------DAILY PLANNER MENU----------------")
        print("1 - Add a Task")
        print("2 - View All Tasks")
        print("3 - View Today's Tasks")
        print("4 - Mark Task as Completed")
        print("5 - Delete a Task")
        print("0 - Exit")
        choice = int(input("Enter your choice:"))
        if choice==1:
            add_task()
        elif choice==2:
            view_tasks()
        elif choice==3:
            view_today_tasks()
        elif choice==4:
            mark_task_completed()
        elif choice==5:
            delete_task()
        elif choice==0:
            print('Thank You For Using Our Services!')
            break
        else:
            print("Invalid Choice! Try Again!")

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
        print("Welcome to Daily Task Manager")
        main_menu()
    else:
        print("ACCESS DENIED!")

login()
conn.close()