import os
import threading
MSG = []
STOP = False


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
        STOP = True


def push(cursor, mycon, user_id, table_name, s):
    global STOP
    from datetime import datetime
    print(f"{user_id}: ", end='')
    text = input()
    if text.strip() != '':
        try:
            text = str(text+" "+str(datetime.now()))
            cursor.execute(
                f'insert into {table_name}({user_id}) values("{text}");')
            mycon.commit()
        except:
            if not mycon.is_connected():
                try:
                    mycon = s.connect(host=os.environ.get("DB_FOREIGN_SERVER"), user=os.environ.get("DB_FOREIGN_USER"),
                                      passwd=os.environ.get("DB_FOREIGN_PASS"), database=os.environ.get("DB_FOREIGN_USER"))
                    cursor = mycon.cursor()
                    cursor.execute(
                        f'insert into {table_name}({user_id}) values("{text}");')
                    mycon.commit()
                except:
                    STOP = True
                    print("Error occured........Try again later...\nLogged Out")
            else:
                print("Error occured........Try again later...\nLogged Out")
                STOP = True
    else:
        print("\x1B[1F", end='')
    if not STOP:
        push(cursor, mycon, user_id, table_name, s)


def fetch(cursor, mycon, table_name, user_id, chat_user, s):
    import time
    global MSG, STOP
    try:
        cursor.execute(f"select {chat_user} from {table_name};")
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
        time.sleep(0.5)
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
                print("Error occured in Fetching Data..\nLogged Out")
        else:
            print("Error occured in Fetching Data..\nLogged Out")
            STOP = True
    if not STOP:
        fetch(cursor, mycon, table_name, user_id, chat_user, s)


def fetchall(cursor, user_id, chat_user, table_name):
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
        print("Some error occured...Try again later\nLogged Out")
