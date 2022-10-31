import os
from tkinter import BOTH, CENTER, E, LEFT, RIGHT, W, X, Y, YES, Label, messagebox
from encryption import encrypt, decrypt, generate_key
MSG = []
STOP = False
REQUEST_PUSH = False
REQUEST_FETCH = False
HEIGHT = 5
# BUTTON_CLICKED = False
KEY = ""


def textCutter(text: str) -> str:
    group = []
    for i in range(0, len(text), 32):
        group.append(text[i:i+32])
    return '\n'.join(group)


def Service(cursor, msg, sendButton, frame, stat, mycon,
            user_id, chat_user, table_name, s):
    import time

    def send(e, cursor, msg, frame, stat, mycon, user_id, table_name, s, text=""):
        from datetime import datetime

        if text.strip() != '':
            try:
                text = str(text+" "+str(datetime.now()))
                # while True:
                # if REQUEST_FETCH == False:
                #     REQUEST_PUSH = True
                cursor.execute(
                    f'insert into {table_name}({user_id}) values("{text}");')
                mycon.commit()
                msg.delete("1.0", "end")
                Label(frame, text=text, bg="green", fg="white", font=(
                    "Aerial", 13), justify=LEFT, anchor=W, bd=0, padx=5).pack(pady=5, padx=120,  ipady=5)
                text = ""
                # REQUEST_PUSH = False
                # break
                # else:
                #     continue
            except:
                if not mycon.is_connected():
                    try:
                        mycon = s.connect(host=os.environ.get("DB_SERVER"), user=os.environ.get("DB_USER"),
                                          passwd=os.environ.get("DB_PASS"), database=os.environ.get("DB_NAME"))
                        cursor = mycon.cursor()
                        # while True:
                        # if REQUEST_FETCH == False:
                        #     REQUEST_PUSH = True
                        cursor.execute(
                            f'insert into {table_name}({user_id}) values("{text}");')
                        mycon.commit()
                        msg.delete("1.0", "end")
                        Label(frame, text=text, bg="green", fg="white", font=(
                            "Aerial", 13), justify=LEFT, anchor=W, bd=0, padx=5).pack(pady=5, padx=120,  ipady=5)
                        text = ""
                        #     REQUEST_PUSH = False
                        #     break
                        # else:
                        #     continue
                    except:
                        STOP = True
                        cursor.execute(
                            f"update signup set status='Offline' where username='{user_id}';")
                        mycon.commit()
                        # print(
                        #     "Error occured........Try again later...\nLogged Out")
                        # quit()
                        raise Exception
                else:
                    try:
                        send(e, cursor, msg, frame, stat,
                             mycon, user_id, table_name, s, text)
                    except:
                        STOP = True
                        # print("Error occured........Try again later...\nLogged Out")
                        # quit()
                        cursor.execute(
                            f"update signup set status='Offline' where username='{user_id}';")
                        mycon.commit()
                        raise Exception
        # else:
            # print("\x1B[1F", end='')

    sendButton.bind("<Button-1>", lambda e: send(e, cursor, msg,
                    frame, stat, mycon, user_id, table_name, s))

    while True:
        try:
            cursor.execute(
                f"select status from signup where username='{chat_user}';")
            status = cursor.fetchone()[0]
            if stat.get() != status:
                stat.configure(text=f'{status}')
            # if REQUEST_PUSH == False:
            #     REQUEST_FETCH = True
                cursor.execute(f"select {chat_user} from {table_name};")
                # REQUEST_FETCH = False
                # break
            else:
                continue
            for i in cursor:
                # if STOP:
                #     break
                if i == (None,):
                    continue
                if i[0] not in MSG:
                    # print("\r\x1b[2K", end='')
                    # print(
                    #     f"{chat_user}: {' '.join(i[0].split()[0:-2])}\n{user_id}: ", end='')
                    text_ = textCutter(i[0])
                    Label(frame, text=text_, font=("Aerial", 13), bg="#595959", fg="white",
                          justify=LEFT, anchor=W, bd=0, padx=5).pack(fill=Y, pady=5, padx=0, ipady=5)
                    MSG.append(i[0])
            time.sleep(1)
            mycon.commit()
        except:
            if not mycon.is_connected():
                try:
                    mycon = s.connect(host=os.environ.get("DB_FOREIGN_SERVER"), user=os.environ.get("DB_FOREIGN_USER"),
                                      passwd=os.environ.get("DB_FOREIGN_PASS"), database=os.environ.get("DB_FOREIGN_USER"))
                    cursor = mycon.cursor()
                    mycon.commit()
                except:
                    STOP = True
                    # print("Error occured in Connection ..\nLogged Out")
                    cursor.execute(
                        f"update signup set status='Offline' where username='{user_id}';")
                    mycon.commit()
                    raise Exception
                    # quit()
            else:
                try:
                    # fetch(cursor, mycon, table_name, user_id, chat_user, s)
                    pass
                except:
                    STOP = True
                    # print("Error occured in Fetching Data..\nLogged Out")
                    # quit()
                    cursor.execute(
                        f"update signup set status='Offline' where username='{user_id}';")
                    mycon.commit()


def multi(cursor, msg, sendButton, frame, stat, mycon,
          user_id, chat_user, table_name, s):

    global KEY
    KEY = generate_key(table_name)
    sendButton.bind("<Button-1>", lambda _: push(_, cursor, msg,
                    frame, mycon, user_id, table_name, s))
    fetch(cursor, frame, stat, mycon, table_name, user_id, chat_user, s)


def push(_, cursor, msg, frame, mycon, user_id, table_name, s, text=""):
    global STOP, REQUEST_FETCH, REQUEST_PUSH, KEY
    from datetime import datetime
    if text == "":
        text = msg.get(1.0, "end")
    if text.strip() != '':
        try:
            text = encrypt(text, KEY)
            text_ = textCutter(decrypt(text, KEY))
            text = str(text+" "+str(datetime.now()))
            while True:
                if REQUEST_FETCH == False:
                    REQUEST_PUSH = True
                    cursor.execute(
                        f'insert into {table_name}({user_id}) values("{text}");')
                    mycon.commit()
                    msg.delete("1.0", "end")
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
                        f"update signup set status='Offlineline' where username='{user_id}';")
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
    global MSG, STOP, REQUEST_PUSH, REQUEST_FETCH, KEY
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
                msg = ' '.join(i[0].split()[0:-2])
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
    global MSG, HEIGHT
    KEY_ = generate_key(table_name)
    user_id_msg = []
    chat_user_msg = []

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
                if user_id_msg == []:
                    break
                if user_id_msg[i] == None:
                    text_ = ' '.join(
                        chat_user_msg[i].split()[0:-2])
                    text_ = decrypt(text_, KEY_)
                    text_ = textCutter(text_)
                    Label(frame, text=text_, font=("Aerial", 18), bg="#595959", fg="white",
                          justify=LEFT, anchor=W, bd=0, padx=5).pack(pady=5, padx=10, ipady=5, anchor=W)
                if chat_user_msg[i] == None:
                    text_ = ' '.join(user_id_msg[i].split()[
                        0:-2])
                    text_ = decrypt(text_, KEY_)
                    text_ = textCutter(text_)
                    Label(frame, text=text_, bg="green", fg="white", font=(
                        "Aerial", 18), justify=LEFT, anchor=W, bd=0, padx=5).pack(pady=5, padx=10, ipady=2, anchor=E)
        MSG = chat_user_msg
    except Exception as e:
        cursor.execute(
            f"update signup set status='Offline' where username='{user_id}';")
        mycon.commit()
        messagebox.showerror(
            "Error", f"Network Error...\nError Code: {e.args[0]}")
