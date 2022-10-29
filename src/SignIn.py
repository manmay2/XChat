from client import *
from encryption import encrypt
from tkinter import Entry, Button, Frame, Label, messagebox, Listbox, Text, Button


def signin(title, root, button, cursor, mycon, s):
    def destroy(_, user_id):
        ans = messagebox.askyesno("Xchat", "Are You Sure??")
        if ans:
            cursor.execute(
                f"update signup set status='Offline' where username='{user_id}'")
            mycon.commit()
            root.destroy()

    def itemSelect(user_id, data, listBox, label, button):
        value = str(listBox.get("anchor"))
        ch = int(value[0])
        listBox.destroy()
        label.destroy()
        button.destroy()
        status = data[ch-1][2]
        name = value[4:]
        user_id = ''.join(user_id.split())
        chat_user = ''.join(str(data[ch-1][0]).split())
        cond1 = user_id+str(chat_user)
        cond2 = str(chat_user)+user_id
        cursor.execute("show tables;")
        # tables = cursor.fetchall()
        for temp in cursor:
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
        label_frame = Frame(root, height=50, width=400, bg='green')
        label_frame.place(x=0, y=50)
        Label(label_frame, text=f"{name}", fg="white", bg="green", font=(
            "Times New Roman", 25)).place(x=10, y=0)
        stat = Label(label_frame, text=f"{status}", fg="white", bg="green", font=(
            "Times New Roman", 15))
        stat.place(x=10, y=28)
        frame = Frame(root, height=560, width=400)
        frame.place(x=0, y=100)
        frame.pack_propagate(0)
        msg = Text(root, bd=8, height=1, width=27, bg="#c7c9bd",
                   fg="black", font=("Aerial", 15))
        msg.place(x=20, y=650)
        sendButton = Button(root, text='SEND', height=2, width=4,
                            bg='green', fg='black')
        sendButton.place(x=320, y=650)
        fetchall(frame, mycon, cursor, user_id, chat_user, table_name)
        # button.unbind("<Button-1>", bind)
        multi(root, cursor, msg, sendButton, button, frame, stat,
              mycon, user_id, chat_user, table_name, s)

        # user_id = input("Enter your user name to login: ").strip()
        # paswd = input("Enter the password to login: ").strip()

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
                if (i[0] == user_id and i[1] == paswd):
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
            elif (flag == 1):
                delete()
                label = Label(root, text="Select the User with whom you wanna continue chat...", font=(
                    'Aerial', 15), bg="#323232", fg="white")
                label.place(x=10, y=50)
                listBox = Listbox(
                    root, width=30, name="list", bg="#323232", selectbackground="#3F3737", font=("Times 20"))
                listBox.pack()
                listBox.place(x=33, y=80)
                data.remove((user_id, paswd, status))
                for j in data:
                    if (j[0] == user_id and j[1] == paswd):
                        continue
                    else:
                        inc += 1
                        # print(inc, ".", j[0])
                        listBox.insert("end", f"{inc} . {j[0]}")
                if len(data) == 0:
                    # print("No Other user available...\n\n")
                    listBox.insert("end", "No Other user available...")
                else:
                    # ch = int(input("WHOM DO YOU WANT TO CHAT--- : "))
                    button = Button(root, text="Start Chat..",
                                    command=lambda: itemSelect(user_id, data, listBox, label, button), bd=0)
                    button.place(x=150, y=420)

    def onClick(event):
        if str(event.widget) == ".!entry" and user_name.get() == "Enter User Name...":
            user_name.delete(0, len("Enter User Name..."))
            user_name.focus_force()
        elif str(event.widget) == ".!entry2" and pas.get() == "Enter Password...":
            pas.delete(0, len("Enter Password..."))
            pas.focus_force()

    user_name = Entry(root, width=23, font=("Arial", 20))
    user_name.bind("<1>", onClick)
    user_name.insert(0, "Enter User Name...")
    user_name.place(x=50, y=130)
    pas = Entry(root, width=23, font=("Arial", 20))
    pas.insert(0, "Enter Password...")
    pas.bind("<1>", onClick)
    pas.place(x=50, y=260)

    bind = button.bind(
        "<Button-1>", lambda _:  destroy(_, str(user_name.get())))

    signInButton = Button(root, text="Sign In...",
                          command=insert)
    signInButton.place(x=150, y=500)
