import os
from tkinter import CENTER, E, LEFT, W, Label, messagebox
from encryption import encrypt, decrypt, generate_key
MSG = []
STOP = False
REQUEST_PUSH = False
REQUEST_FETCH = False
# BUTTON_CLICKED = False
KEY = ""
DAYS_ADDED = []


def calc(inp: str) -> str:
    """Determines relative date.."""
    from datetime import date
    inp = inp.split('-')

    def leap(year: int) -> bool:
        if (year % 100 == 0 and year % 400 == 0):
            return True
        elif (year % 100 == 0 and year % 400 != 0):
            return False
        elif (year % 4 == 0):
            return True
        else:
            return False

    t = str(date.today()).split('-')
    li_months = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
    if t[0] == inp[0] and t[1] == inp[1] and t[2] == inp[2]:
        return "Today"
    elif (t[0] == inp[0]) and leap(int(inp[0])) and t[1] == '03' and inp[1] == '02' and t[2] == '01' and inp[2] == '29':
        return ("Yesterday")
    elif (t[0] == inp[0]) and not leap(int(inp[0])) and t[1] == '03' and inp[1] == '02' and t[2] == '01' and inp[2] == '28':
        return "Yesterday"
    elif (((t[2] == '01' and inp[2] == '31') or (t[2] == '01' and inp[2] == '30')) and t[0] == inp[0] and int(t[1])-1 == int(inp[1])):
        return ("Yesterday")
    elif (int(t[2])-1 == int(inp[2]) and t[0] == inp[0] and t[1] == inp[1]):
        return ("Yesterday")
    else:
        return inp[2]+" "+li_months[int(inp[1])-1]+" "+inp[0]


def textCutter(text: str) -> str:
    group = []
    for i in range(0, len(text), 32):
        group.append(text[i:i+32])
    return '\n'.join(group)


def multi(cursor, msg, sendButton, frame, stat, mycon,
          user_id, chat_user, table_name, s):

    global KEY
    KEY = generate_key(table_name)
    sendButton.bind("<Button-1>", lambda _: push(_, cursor, msg,
                    frame, mycon, user_id, table_name, s))
    fetch(cursor, frame, stat, mycon, table_name, user_id, chat_user, s)


def push(_, cursor, msg, frame, mycon, user_id, table_name, s, text=""):
    global STOP, REQUEST_FETCH, REQUEST_PUSH, KEY, DAYS_ADDED
    from datetime import datetime
    if text == "":
        text = msg.get(1.0, "end")
    if text.strip() != '':
        try:
            text = encrypt(text, KEY)
            text_ = textCutter(decrypt(text, KEY))
            text = str(text+" "+str(datetime.now()))
            day = calc(str(datetime.now()).split()[0])
            while True:
                if REQUEST_FETCH == False:
                    REQUEST_PUSH = True
                    cursor.execute(
                        f'insert into {table_name}({user_id}) values("{text}");')
                    mycon.commit()
                    msg.delete("1.0", "end")
                    if day not in DAYS_ADDED:
                        Label(frame, text=day, font=("Aerial 16"), bg='#595959', fg='#d9d9d9', bd=0, padx=3).pack(
                            pady=3, ipadx=3, ipady=1, anchor=CENTER)
                        DAYS_ADDED.append(day)
                    Label(frame, text=text_, bg="green", fg="white", font=(
                        "Aerial", 18), justify=LEFT, anchor=W, bd=0, padx=5).pack(pady=5, padx=10, ipady=2, anchor=E)
                    text = ""
                    REQUEST_PUSH = False
                    break
                else:
                    continue
        except Exception as e:
            if not mycon.is_connected():
                try:
                    mycon = s.connect(host=os.environ.get("DB_FOREIGN_SERVER"), user=os.environ.get("DB_FOREIGN_USER"),
                                      passwd=os.environ.get("DB_FOREIGN_PASS"), database=os.environ.get("DB_FOREIGN_USER"))
                    cursor = mycon.cursor()
                    while True:
                        if REQUEST_FETCH == False:
                            REQUEST_PUSH = True
                            cursor.execute(
                                f'insert into {table_name}({user_id}) values("{text}");')
                            mycon.commit()
                            msg.delete("1.0", "end")
                            if day not in DAYS_ADDED:
                                Label(frame, text=day, font=("Aerial 16"), bg='#595959', fg='#d9d9d9', bd=0, padx=3).pack(
                                    pady=3, ipadx=3, ipady=1, anchor=CENTER)
                                DAYS_ADDED.append(day)
                            Label(frame, text=text, bg="green", fg="white", font=(
                                "Aerial", 13), justify=LEFT, anchor=W, bd=0, padx=5).pack(pady=5, padx=120,  ipady=5)
                            text = ""
                            REQUEST_PUSH = False
                            break
                        else:
                            continue
                except:
                    STOP = True
                    cursor.execute(
                        f"update signup set status='Offline' where username='{user_id}';")
                    mycon.commit()
            else:
                # try:
                #     push(e, cursor, msg, frame, stat, mycon,
                #          user_id, table_name, s, text)
                # except:
                STOP = True
                cursor.execute(
                    f"update signup set status='Offline' where username='{user_id}';")
                mycon.commit()
                messagebox.showerror("Error", f"Network Error..{e.args[0]}")


def fetch(cursor, frame, stat, mycon, table_name, user_id, chat_user, s):
    global MSG, STOP, REQUEST_PUSH, REQUEST_FETCH, KEY, DAYS_ADDED
    initial = 0
    try:
        while True:
            cursor = mycon.cursor(buffered=True)
            cursor.execute(
                f"select status from signup where username='{chat_user}';")
            status = cursor.fetchone()[0]
            if stat['text'] != status:
                stat.configure(text=f'{status}')
            if REQUEST_PUSH == False:
                REQUEST_FETCH = True
                cursor.execute(f"select {chat_user} from {table_name};")
                REQUEST_FETCH = False
                break
            else:
                continue
        for i in cursor:
            if STOP:
                break
            if i == (None,):
                continue
            if i[0] not in MSG:
                day = calc(i[0].split()[-2])
                msg = ' '.join(i[0].split()[0:-2])
                # if initial == 0:
                #     Label(frame, text=day, font=("Aerial 16"), bg='#595959', fg='#d9d9d9', bd=0, padx=3).pack(
                #         pady=3, ipadx=3, ipady=1, anchor=CENTER)
                #     Label(frame, text=msg, font=("Times 15"), bg='#323232', fg='white', bd=0, padx=3).pack(
                #         pady=3, ipadx=3, ipady=1, anchor=W)
                #     DAYS_ADDED.append(day)
                #     MSG.append(i[0])
                #     initial += 1
                #     continue
                if day not in DAYS_ADDED:
                    Label(frame, text=day, font=("Aerial 16"), bg='#595959', fg='#d9d9d9', bd=0, padx=3).pack(
                        pady=3, ipadx=3, ipady=1, anchor=CENTER)
                    DAYS_ADDED.append(day)
                text_ = textCutter(decrypt(msg, KEY))
                Label(frame, text=text_, font=("Aerial", 18), bg="#595959", fg="white",
                      justify=LEFT, anchor=W, bd=0, padx=5).pack(pady=5, padx=10, ipady=5, anchor=W)
                MSG.append(i[0])
        mycon.commit()
    except:
        if not mycon.is_connected():
            try:
                mycon = s.connect(host=os.environ.get("DB_SERVER"), user=os.environ.get("DB_USER"),
                                  passwd=os.environ.get("DB_PASS"), database=os.environ.get("DB_NAME"))
                cursor = mycon.cursor()
                mycon.commit()
            except:
                STOP = True
                cursor.execute(
                    f"update signup set status='Offline' where username='{user_id}';")
                mycon.commit()

        else:
            try:
                fetch(cursor, frame, stat, mycon,
                      table_name, user_id, chat_user, s)
            except Exception as e:
                STOP = True
                cursor.execute(
                    f"update signup set status='Offline' where username='{user_id}';")
                mycon.commit()
                messagebox.showerror(
                    "Error", f"Network Error...\nError Code: {e.args[0]}")
    frame.after(1000, lambda: fetch(cursor, frame, stat,
                mycon, table_name, user_id, chat_user, s))


def fetchall(frame, mycon, cursor, user_id, chat_user, table_name):
    global MSG, DAYS_ADDED
    KEY_ = generate_key(table_name)
    user_id_msg = []
    chat_user_msg = []
    Label(frame, text="The only fast, reliable,  and highly trusted and \n end-to-end encypted source of communication. -XChat",
          font=("Times 15"), bg='#323232', fg='white', bd=0, padx=3).pack(pady=3, ipadx=3, ipady=1, anchor=CENTER)
    try:
        cursor.execute("select {},{} from {};".format(
            user_id, chat_user, table_name))
        for i in cursor:
            if i == (None, None):
                continue
            user_id_msg.append(i[0])
            chat_user_msg.append(i[1])

        if user_id_msg != [] or chat_user_msg != []:
            for i in range(len(user_id_msg)):
                if user_id_msg[i] == None:
                    day = calc(chat_user_msg[i].split()[-2])
                    text_ = ' '.join(
                        chat_user_msg[i].split()[0:-2])
                    text_ = decrypt(text_, KEY_)
                    text_ = textCutter(text_)
                    if day not in DAYS_ADDED:
                        Label(frame, text=day, font=("Aerial 16"), bg='#595959', fg='#d9d9d9', bd=0, padx=3).pack(
                            pady=3, ipadx=3, ipady=1, anchor=CENTER)
                        DAYS_ADDED.append(day)
                    Label(frame, text=text_, font=("Aerial", 18), bg="#595959", fg="white",
                          justify=LEFT, anchor=W, bd=0, padx=5).pack(pady=5, padx=10, ipady=5, anchor=W)
                elif chat_user_msg[i] == None:
                    day = calc(user_id_msg[i].split()[-2])
                    text_ = ' '.join(user_id_msg[i].split()[
                        0:-2])
                    text_ = decrypt(text_, KEY_)
                    text_ = textCutter(text_)
                    if day not in DAYS_ADDED:
                        Label(frame, text=day, font=("Aerial 16"), bg='#595959', fg='#d9d9d9', bd=0, padx=3).pack(
                            pady=3, ipadx=3, ipady=1, anchor=CENTER)
                        DAYS_ADDED.append(day)
                    Label(frame, text=text_, bg="green", fg="white", font=(
                        "Aerial", 18), justify=LEFT, anchor=W, bd=0, padx=5).pack(pady=5, padx=10, ipady=2, anchor=E)
        else:
            # try:
            #     tex = "Welcome to the fast, reliable,  and highly trusted and \n end-to-end encypted source of communication. -XChat"
            #     cursor = mycon.cursor(buffered=True)
            #     cursor.execute(
            #         f"insert into {table_name}({chat_user},{user_id}) values('{tex} {str(datetime.now())}',NULL)")
            #     mycon.commit()
            # except:
            pass
        MSG = chat_user_msg
    except Exception as e:
        cursor.execute(
            f"update signup set status='Offline' where username='{user_id}';")
        mycon.commit()
        messagebox.showerror(
            "Error", f"Network Error...\nError Code: {e.args[0]}")
