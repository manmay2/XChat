from glob import glob
from client import *
from encryption import encrypt
from tkinter import Entry, Button, messagebox, Listbox


def signin(title, root, cursor, mycon, s):
    def itemSelect(event, user_id, data):
        w = event.widget
        index = int(w.curselection()[0])
        ch = int(str(w.get(index))[0])
        w.destroy()
        user_id = ''.join(user_id.split())
        chat_user = ''.join(str(data[ch-1][0]).split())
        cond1 = user_id+str(chat_user)
        cond2 = str(chat_user)+user_id
        cursor.execute("show tables;")
        tables = cursor.fetchall()
        for temp in tables:
            if temp[0] == cond1 or temp[0] == cond2:
                table_name = temp[0]
                break
        else:
            table_name = cond1
        try:
            query = f"create table if not exists {table_name}({user_id} LONGTEXT,{str(chat_user)} LONGTEXT);"
            cursor.execute(query)
            cursor.execute(
                f"update signup set status='Online' where username='{user_id}';")
            mycon.commit()
        except:
            raise Exception
        fetchall(mycon, cursor, user_id, chat_user, table_name)
        multi(cursor, mycon, user_id, chat_user, table_name, s)

        user_id = input("Enter your user name to login: ").strip()
        paswd = input("Enter the password to login: ").strip()

    def delete():
        user_name.destroy()
        pas.destroy()
        signInButton.destroy()
        title.destroy()

    def insert():
        user_id = user_name.get()
        paswd = pas.get()
        if (user_id == "" or paswd == "") or (user_id == "Enter User Name..." or paswd == "Enter Password..."):
            messagebox.showwarning("XChat", "Please provide valid input....")
        else:
            paswd = encrypt(paswd)
            flag = 0
            inc = 0
            cursor.execute("select * from signup;")
            data = cursor.fetchall()
            status = ""
            for i in data:
                if(i[0] == user_id and i[1] == paswd):
                    messagebox.showinfo(
                        "XChat", "YOU ARE SUCCESSFULLY SIGNED IN")
                    # print("YOU ARE SUCCESSFULLY SIGNED IN")
                    status = i[2]
                    # print("___________________________________________________\n")
                    flag = 1
                    break
            if flag != 1:
                messagebox.showerror(
                    "XChat", "PLEASE CHECK YOUR USERNAME AND PASSWORD AND TRY AGAIN LATER!!!!")
            elif(flag == 1):
                delete()
                listBox = Listbox(
                    root, width=30, name="list", bg="#323232", selectbackground="#3F3737", font=("Times 20"))
                listBox.pack()
                listBox.place(x=33, y=30)
                listBox.bind("<<ListboxSelect>>",
                             lambda event: itemSelect(event, user_id, data))
                data.remove((user_id, paswd, status))

                for j in data:
                    if(j[0] == user_id and j[1] == paswd):
                        continue
                    else:
                        inc += 1
                        # print(inc, ".", j[0])
                        listBox.insert(inc-1, f"{inc} . {j[0]}")
                if len(data) == 0:
                    # print("No Other user available...\n\n")
                    listBox.insert(0, "No Other user available...")
                # else:
                #     pass
                #     ch = int(input("WHOM DO YOU WANT TO CHAT--- : "))

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

    signInButton = Button(root, text="Sign In...", command=insert)
    signInButton.place(x=150, y=500)
