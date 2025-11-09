import tkinter as tk
import pyodbc
from tkinter import messagebox
import re

#connect to sql server
conn=pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-2VKUOAN\\SQL2008R2;'
    'DATABASE=Userdb;'
    'Trusted_Connection=yes;'
)
cursor=conn.cursor()
print("Connected to SQL Server Successfully!")

#data validation function
def validate_data(password, contact, email):
    #password validation
    if (len(password) < 8 or 
        not password.isalnum() or 
        not any(char.isdigit() for char in password) or 
        not any(char.isalpha() for char in password)):
        messagebox.showwarning("Input Error", 
            "Password must be at least 8 characters long, contain letters and numbers, and be alphanumeric.")
        return False

    #contact number validation
    if not (contact.isdigit() and len(contact) == 10):
        messagebox.showwarning("Input Error", "Contact number must be exactly 10 digits.")
        return False

    #email validation(using regex pattern)
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        messagebox.showwarning("Input Error", "Invalid email address format.")
        return False
    return True

#search for user
def search_user():
    global search_entry,user_info
    name = search_entry.get().strip()
    print(name)
    user_info.delete("1.0", tk.END)
    if not name:
            messagebox.showwarning("Input Error", "Please enter a user name to search.")
            return
    try:
            cursor.execute("SELECT * FROM Info WHERE username=?", (name,))
            result = cursor.fetchone()
            if result:
                info_text = f"Name:\t\t{result[0]}\n\nPassword:\t\t{result[1]}\n\nGender:\t\t{result[2]}\n\nContact:\t\t{result[3]}\n\nEmail:\t\t{result[4]}\n\nQualification:\t\t{result[5]}"
                user_info.configure(font=("Times New Roman", 11, "bold"))
                user_info.insert(tk.END, info_text)
            else:
                messagebox.showinfo("Not Found", "No user found with that name.")
                return
    except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return
    
#update function           
def update_user():
    name = search_entry.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a username to update.")
        return

    #check if user exists in database
    cursor.execute("SELECT * FROM Info WHERE username=?", (name,))
    user = cursor.fetchone()
    if not user:
        messagebox.showinfo("Not Found", f"No user found with name '{name}'.")
        return

    update_window = tk.Toplevel(root)
    update_window.title(f"Update User - {name}")
    update_window.geometry("500x400")
    update_window.configure(bg="#f0f0f0")

    tk.Label(update_window, text=f"Update Details for {name}", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=15)

    #take new values from user to update
    tk.Label(update_window, text="Password:", bg="#f0f0f0").pack()
    password_entry = tk.Entry(update_window)
    password_entry.insert(0, user[1])
    password_entry.pack()

    tk.Label(update_window, text="Gender:", bg="#f0f0f0").pack()
    gender_var = tk.StringVar(value=user[2])
    tk.Radiobutton(update_window, text="Male", variable=gender_var, value="Male", bg="#f0f0f0").pack()
    tk.Radiobutton(update_window, text="Female", variable=gender_var, value="Female", bg="#f0f0f0").pack()

    tk.Label(update_window, text="Contact:", bg="#f0f0f0").pack()
    contact_entry = tk.Entry(update_window)
    contact_entry.insert(0, user[3])
    contact_entry.pack()

    tk.Label(update_window, text="Email:", bg="#f0f0f0").pack()
    email_entry = tk.Entry(update_window)
    email_entry.insert(0, user[4])
    email_entry.pack()

    tk.Label(update_window, text="Qualification:", bg="#f0f0f0").pack()
    qualification_var = tk.StringVar(value=user[5])
    tk.OptionMenu(update_window, qualification_var, "High School", "Intermediate", "Undergraduate", "Postgraduate", "PhD").pack()
    
    #save updated details of user
    def save_updated_details():
        new_password = password_entry.get().strip()
        new_gender = gender_var.get()
        new_contact = contact_entry.get().strip()
        new_email = email_entry.get().strip()
        new_qualification = qualification_var.get()

        if not validate_data(new_password, new_contact, new_email):
            messagebox.showwarning("Input Error", "Please fill valid values in password, contact, and email fields before updating.")
            return
        
        if not all([new_password, new_contact, new_email]) or new_qualification == "Select":
            messagebox.showwarning("Input Error", "Please fill all fields properly before updating.")
            return

        try:
            cursor.execute("UPDATE Info SET password=?, gender=?, phone=?, email=?, qualification=? WHERE username=?",
                           (new_password, new_gender, new_contact, new_email, new_qualification, name))
            conn.commit()

            messagebox.showinfo("Success", f"User '{name}' updated successfully.")
            #update_window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
    tk.Button(update_window, text="Save Changes", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), command=save_updated_details).pack(pady=20)

#function to delete user from database
def delete_user():
    name = search_entry.get()
    print(name)
    cursor.execute("DELETE FROM Info WHERE username=?", (name,))
    conn.commit()
    if cursor.rowcount == 0:
        messagebox.showinfo("Info", f"No user found with name '{name}'.")
    else:
        messagebox.showinfo("Success", f"User '{name}' deleted successfully.")

#function to reset search and user info fields
def reset_user():
    search_entry.delete(0, tk.END)
    user_info.delete("1.0", tk.END)

#function to save user data from registration form in database
def save_user():
    name=name_entry.get()
    password=password_entry.get()
    gender=gender_var.get()
    contact=contact_entry.get()   
    email=email_entry.get()
    qualification=qualification_var.get()
    try:
        if not all([name, password, contact, email]) or qualification == "Select" or not validate_data(password, contact, email):
            messagebox.showwarning("Input Error", "Please fill all fields properly.")
            return
        cursor.execute("INSERT INTO Info (username, password, gender, phone, email, qualification) VALUES (?, ?, ?, ?, ?, ?)",(name,password,gender,contact,email,qualification))
        conn.commit()
        messagebox.showinfo("Success!","User information saved successfully.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

#function to open registration form window
def open_registration():
    global name_entry, password_entry, gender_var, contact_entry, email_entry, qualification_var
    reg_window = tk.Toplevel(root)
    reg_window.title("Registration Form")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    reg_window.configure(padx=550,bg="#64adf7")
    #set window to full screen height and width
    reg_window.geometry(f"{screen_width}x{screen_height}")
    
    tk.Label(reg_window, text="Registration Form", font=("Times New Roman", 20,"bold"),background="#64adf7").grid(padx=20,pady=50)

    frame2 = tk.Frame(reg_window)
    frame2.grid(padx=30,pady=50)

    tk.Label(frame2, text="User Name", font=("Times New Roman", 16,"bold")).grid(row=3,column=0,padx=20,pady=20)
    name_entry = tk.Entry(frame2)
    name_entry.grid(row=3,column=1)

    tk.Label(frame2, text="Password", font=("Times New Roman", 16,"bold")).grid(row=4,column=0,padx=20,pady=20)
    password_entry = tk.Entry(frame2, show="*")
    password_entry.grid(row=4,column=1,padx=20,pady=20)

    tk.Label(frame2, text="Gender", font=("Times New Roman", 16,"bold")).grid(row=5,column=0,padx=20,pady=20)
    gender_var = tk.StringVar(value="Male")
    tk.Radiobutton(frame2, text="Male", variable=gender_var, value="Male", font=("Times New Roman", 14)).grid(row=5,column=1)
    tk.Radiobutton(frame2, text="Female", variable=gender_var, value="Female", font=("Times New Roman", 14)).grid(row=5,column=2)

    tk.Label(frame2, text="Phone Number", font=("Times New Roman", 16,"bold")).grid(row=6,column=0,padx=20,pady=20)
    contact_entry = tk.Entry(frame2)
    contact_entry.grid(row=6,column=1,padx=20,pady=20)

    tk.Label(frame2, text="Email Address", font=("Times New Roman", 16,"bold")).grid(row=7,column=0,padx=20,pady=20)
    email_entry = tk.Entry(frame2)
    email_entry.grid(row=7,column=1,padx=20,pady=20)

    tk.Label(frame2, text="Qualification", font=("Times New Roman", 16,"bold")).grid(row=8,column=0,padx=20,pady=20)
    qualification_var = tk.StringVar(value="Select")
    qualification_entry = tk.OptionMenu(frame2, qualification_var, "High School","Intermediate","Undergraduate", "Postgraduate", "PhD")
    qualification_entry.grid(row=8,column=1,padx=20,pady=20)

    save_btn = tk.Button(frame2, text="Save", height=1, width=5, bg="#f1492b", fg="white",font=("Times New Roman", 16,"bold"),command=save_user)
    save_btn.grid(row=9,column=0,padx=50,pady=20)

    reset_btn = tk.Button(frame2, text="Reset", height=1, width=5, bg="#37d158", fg="white",font=("Times New Roman", 16,"bold"),command=lambda: [name_entry.delete(0, tk.END), email_entry.delete(0, tk.END), password_entry.delete(0, tk.END), contact_entry.delete(0, tk.END), qualification_var.set("Select")])
    reset_btn.grid(row=9,column=1,padx=50,pady=20)

#function to open CRUD operations window
def open_crud():
    crud_window = tk.Toplevel(root)
    crud_window.title("CRUD Operations")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    crud_window.configure(padx=475,bg="#64adf7")

    #set window to full screen height and width
    crud_window.geometry(f"{screen_width}x{screen_height}")

    tk.Label(crud_window, text="CRUD Operation Page", font=("Times New Roman", 20,"bold"),background="#64adf7").grid(pady=10)

    frame3 = tk.Frame(crud_window)
    frame3.grid(padx=20, pady=20)
    global search_entry, user_info
    tk.Label(frame3, text="User Name", font=("Times New Roman", 16,"bold")).grid(row=0, column=0, padx=10, pady=10)
    search_entry = tk.Entry(frame3)
    search_entry.grid(row=0, column=1, padx=10, pady=10)
    search_btn = tk.Button(frame3, text="Search", font=("Times New Roman", 14,"bold"), command=search_user, background="#de14f0", fg="white")
    search_btn.grid(row=0, column=2, padx=10, pady=10)

    tk.Label(frame3, text="--- User Details ---", font=("Times New Roman", 14,"bold")).grid(row=1, columnspan=3, pady=10)

    user_info = tk.Text(frame3, font=("Arial", 10),background="#eeeeee", fg="black")
    user_info.grid(row=2,column=0,rowspan=4, columnspan=3, pady=10, padx=10)

    update_btn = tk.Button(frame3, text="Update", command=update_user,font=("Times New Roman", 14,"bold"),background="#4caf50", fg="white")
    update_btn.grid(row=7, column=0, padx=10, pady=10)

    delete_btn = tk.Button(frame3, text="Delete", command=delete_user,font=("Times New Roman", 14,"bold"),background="#f44336", fg="white")
    delete_btn.grid(row=7, column=1, padx=10, pady=10)

    reset_btn = tk.Button(frame3, text="Reset", command=reset_user,font=("Times New Roman", 14,"bold"),background="#f0ad4e", fg="white")
    reset_btn.grid(row=7, column=2, padx=10, pady=10)

root = tk.Tk()
root.title("Main Page")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#set window to full screen height and width
root.geometry(f"{screen_width}x{screen_height}")
root.configure(bg="#d9f9d9")

frame = tk.Frame(root)
frame.pack(expand=True)

frame.configure(bg="#68a4fd")
tk.Label(frame, text="Main Page", font=("Times New Roman", 30, "bold"), bg="#68a4fd").pack(pady=20)

button1 = tk.Button(frame, text="Open CRUD", font=("Times New Roman", 20, "bold"), width=15, padx=20, pady=20, command=open_crud, bg="#27deeb")
button1.pack(side=tk.LEFT, padx=10, pady=10)

button2 = tk.Button(frame, text="Open Registration", font=("Times New Roman", 20, "bold"), width=15, padx=20, pady=20, command=open_registration, bg="#27deeb")
button2.pack(side=tk.LEFT, padx=10, pady=10)

root.mainloop()