import mysql.connector as s
from SignIn import *
from SignUp import *
from tkinter import Label, Radiobutton, IntVar, Toplevel, Tk
import os
# print("........WELCOME TO THE WORLD OF XCHAT APP.........")

try:
    def event(tex):
        title.configure(text=tex)
        choice = sButton.get()
        messageBox.destroy()
        if(choice == 1):
            signup(root, mycon, cursor)
        elif(choice == 2):
            signin(title, root, cursor, mycon, s)

    mycon = s.connect(host=os.environ.get("DB_SERVER"), user=os.environ.get("DB_USER"),
                      password=os.environ.get("DB_PASS"), database=os.environ.get("DB_NAME"))
    if mycon.is_connected():
        cursor = mycon.cursor()

        cursor.execute(
            "create table if not exists signup(username varchar(200) primary key,password LONGTEXT,status varchar(7) default 'Offline')")

        root = Tk()
        root.minsize(400, 700)
        root.maxsize(400, 700)
        root.configure(background="#323232")
        root.eval('tk::PlaceWindow . center')
        root.title("XChat")
        choice = 0
        sButton = IntVar()

        messageBox = Toplevel(root)
        messageBox.minsize(400, 300)
        messageBox.maxsize(400, 300)
        messageBox.configure(background="#323232")
        messageBox.focus_force()
        root.eval(f'tk::PlaceWindow {str(messageBox)} center')
        Label(messageBox, text="Select the option", width=30, bg="#323232", fg="white",
              pady=15, font=("Times New Roman", 20)).pack()

        Radiobutton(messageBox, text="Sign Up", variable=sButton, font=("Aerial", 15),
                    value=1, bg="#323232", command=lambda: event("Sign Up"), fg="white").place(x=150, y=50)
        Radiobutton(messageBox, text="Sign In", variable=sButton, font=("Aerial", 15),
                    value=2, bg="#323232", command=lambda: event("Sign In"), fg="white").place(x=150, y=80)
        Radiobutton(messageBox, text="Exit", font=("Aerial", 15),
                    value="Exit", command=lambda: root.destroy(), bg="#323232", fg="white").place(x=150, y=110)
        # print("1. NEW TO THE APP!! PRESS 1 TO SIGN UP")
        # print("2. ALREADY HAVE AN ACCOUNT !! PRESS 2 TO SIGN IN")
        # print("3. Exit")

        # choice = int(input("ENTER YOUR CHOICE: "))

        title = Label(root, text="", bg="#323232", fg="white",
                      font=("Times New Roman", 40))
        title.pack(pady=40)

        root.mainloop()
    else:
        print("Connected Failed....")
except:
    print("\nSomething error occured...Try after sometime")
