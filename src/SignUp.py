from encryption import encrypt
from tkinter import Entry, Button, messagebox


def signup(root, button, mycon, cursor):

    def destroy(_, user_id):
        ans = messagebox.askyesno("Xchat", "Are You Sure??")
        if ans:
            cursor.execute(
                f"update signup set status='Offline' where username='{user_id}'")
            mycon.commit()
            root.destroy()

    def insert():
        user = str(user_name.get()).strip()
        pasWord = pas.get().strip()
        if (user == "" or pasWord == "") or (user == "Enter User Name..." or pasWord == "Enter Password..."):
            messagebox.showwarning("XChat", "Please provide valid input....")
        else:
            pasWord = encrypt(str(pasWord))
            try:
                cursor.execute("select username from signup;")
                userNameSet = cursor.fetchall()
                if (user,) in userNameSet:
                    messagebox.showwarning("XChat",
                                           f"Username {user} already exists..Try Different name...")
                    return
            except:
                pass
            cursor.execute(
                "insert into signup(username,password) values('{0}','{1}')".format(user, pasWord))
            mycon.commit()
            messagebox.showinfo("XChat", "Successfully Signed Up....")
    # user_name = input("Enter a user name: ").strip()
    # pas = input("Set a strong password for your account: ").strip()

    def onClick(event):
        if str(event.widget) == ".!entry" and user_name.get() == "Enter User Name...":
            user_name.delete(0, len("Enter User Name..."))
        elif str(event.widget) == ".!entry2" and pas.get() == "Enter Password...":
            pas.delete(0, len("Enter Password..."))

    user_name = Entry(root, width=23,
                      font=("Arial", 20))
    user_name.bind("<1>", onClick)
    user_name.insert(0, "Enter User Name...")
    user_name.place(x=50, y=130)
    pas = Entry(root, width=23, font=("Arial", 20))
    pas.insert(0, "Enter Password...")
    pas.bind("<1>", onClick)
    pas.place(x=50, y=260)
    button.bind("<Button-1>", lambda _:  destroy(_, str(user_name.get())))

    Button(root, text="Sign Up...", command=insert, bd=0).place(x=150, y=500)
