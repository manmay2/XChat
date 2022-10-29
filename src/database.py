import mysql.connector as s
from SignIn import *
from SignUp import *
from tkinter import Frame, Label, PhotoImage, Radiobutton, IntVar, Toplevel, Tk, messagebox as m
import os
# print("........WELCOME TO THE WORLD OF XCHAT APP.........")

try:
    def event(tex):
        title.configure(text=tex)
        choice = sButton.get()
        messageBox.destroy()
        if (choice == 1):
            signup(title, root, but, cursor, mycon, s)
        elif (choice == 2):
            signin(title, root, but, cursor, mycon, s)

    mycon = s.connect(host=os.environ.get("DB_SERVER"), user=os.environ.get("DB_USER"),
                      password=os.environ.get("DB_PASS"), database=os.environ.get("DB_NAME"))
    if mycon.is_connected():
        cursor = mycon.cursor()

        cursor.execute(
            "create table if not exists signup(username varchar(200) primary key,password LONGTEXT,status varchar(7) default 'Offline')")

        def disable_event():
            pass
        root = Tk()
        # root.wm_overrideredirect(True)
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", disable_event)
        width = 400
        height = 700

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        root.geometry('%dx%d+%d+%d' % (width, height, x, y))

        frame1 = Frame(root, bd=0, bg="#323232", width=width,
                       height=50).place(x=0, y=0)
        powerOff = PhotoImage(file="images/power-button.png")
        but = Button(frame1, image=powerOff, bd=0, bg="#323232",
                     fg="#323232")
        but.place(x=width-60, y=5)
        root.configure(background="#323232")
        root.title("XChat")
        choice = 0
        sButton = IntVar()

        messageBox = Toplevel(root)
        messageBox.wm_overrideredirect(True)
        messageBox.focus_force()
        messageBox.lift()
        messageBox.attributes("-topmost", True)
        messageBox.geometry(
            '%dx%d+%d+%d' % (width, height-width, x, (screen_height/2) - (height/2) + 250))
        messageBox.configure(background="#323232")
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

        title = Label(root, bg="#323232", fg="white",
                      font=("Times New Roman", 40))
        title.pack(pady=40)

        root.mainloop()
    else:
        print("Connected Failed....")
except Exception as e:
    # print("\nSomething error occured...Try after sometime", e)
    m.showerror("Error", f"Program Exited with error code: {e.args[0]}")
