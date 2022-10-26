import os
import threading
MSG = []
STOP = False
REQUEST_PUSH = False
REQUEST_FETCH = False


def multi(cursor, mycon, user_id, chat_user, table_name, s):
    global STOP
    try:
        push_thread = threading.Thread(
            target=push, args=(cursor, mycon, user_id, table_name, s))
        fetch_thread = threading.Thread(
            target=fetch, args=(cursor, mycon, table_name, user_id, chat_user, s))
        push_thread.start()
        fetch_thread.start()
        push_thread.join()
        fetch_thread.join()
    except:
        print("Logged Out")
        cursor.execute(
            f"update signup set status='Offline' where username='{user_id}';")
        mycon.commit()
        STOP = True


def push(cursor, mycon, user_id, table_name, s, text=""):
    global STOP, REQUEST_FETCH, REQUEST_PUSH
    from datetime import datetime
    while not STOP:
        print(f"{user_id}: ", end='')
        text = input()
        if text.strip() != '':
            try:
                text = str(text+" "+str(datetime.now()))
                while True:
                    if REQUEST_FETCH == False:
                        REQUEST_PUSH = True
                        cursor.execute(
                            f'insert into {table_name}({user_id}) values("{text}");')
                        mycon.commit()
                        text = ""
                        REQUEST_PUSH = False
                        break
                    else:
                        continue
            except:
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
                        # print(
                        #     "Error occured........Try again later...\nLogged Out")
                        # quit()
                        raise Exception
                else:
                    try:
                        push(cursor, mycon, user_id, table_name, s, text)
                    except:
                        STOP = True
                        # print("Error occured........Try again later...\nLogged Out")
                        # quit()
                        cursor.execute(
                            f"update signup set status='Offline' where username='{user_id}';")
                        mycon.commit()
                        raise Exception
        else:
            print("\x1B[1F", end='')


def fetch(cursor, mycon, table_name, user_id, chat_user, s):
    import time
    global MSG, STOP, REQUEST_PUSH, REQUEST_FETCH
    while not STOP:
        try:
            while True:
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
                    print("\r\x1b[2K", end='')
                    print(
                        f"{chat_user}: {' '.join(i[0].split()[0:-2])}\n{user_id}: ", end='')
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
                    fetch(cursor, mycon, table_name, user_id, chat_user, s)
                except:
                    STOP = True
                    # print("Error occured in Fetching Data..\nLogged Out")
                    # quit()
                    cursor.execute(
                        f"update signup set status='Offline' where username='{user_id}';")
                    mycon.commit()
                    raise Exception


def fetchall(mycon, cursor, user_id, chat_user, table_name):
    global MSG
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
                    print(f"{chat_user}:", ' '.join(
                        chat_user_msg[i].split()[0:-2]))
                if chat_user_msg[i] == None:
                    print(f"{user_id}:", ' '.join(
                        user_id_msg[i].split()[0:-2]))
        MSG = chat_user_msg
    except:
        # print("Some error occured...Try again later\nLogged Out")
        cursor.execute(
            f"update signup set status='Offline' where username='{user_id}';")
        mycon.commit()
        raise Exception
