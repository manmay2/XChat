import threading
STOP=False
MSG=[]
def multi(cursor,mycon,user_id,chat_user,table_name):
    global STOP
    try:
        push_thread=threading.Thread(target=push,args=(cursor,mycon,user_id,table_name))
        fetch_thread=threading.Thread(target=fetch,args=(cursor,mycon,table_name,chat_user,user_id))
        push_thread.start()
        fetch_thread.start()
        push_thread.join()
        fetch_thread.join()
    except:
        print("Logged Out")
        STOP=True
def push(cursor,mycon,user_id,table_name):
    global STOP
    from datetime import datetime
    print(f"{user_id}: ",end='')
    text=input()
    if text.strip()!='':
        try:
            cursor.execute("insert into {}({}) values('{}');".format(table_name,user_id,text+" "+str(datetime.now())))
            mycon.commit()
        except:
            STOP=True
            print("Error occured.. \nLogged Out")
    else:
        print("\x1b[1F",end='')
    if not STOP:
        push(cursor,mycon,user_id,table_name)
def fetch(cursor,mycon,table_name,chat_user,userid):
    global MSG,STOP
    import time
    try:
        cursor.execute("select {} from {};".format(chat_user,table_name))
        for i in cursor:
            if STOP:
                break
            if i == (None,):
                continue
            if i[0] not in MSG:
                print("\r\x1b[2k",end='')
                print(f"{chat_user}: {' '.join(i[0].split()[0:-2])}\n{userid}: ",end='')
                MSG.append(i[0])
        time.sleep(0.5)
        mycon.commit()
    except:
        print("Error in fetching data.\n Logged Out")
        STOP=True
    if not STOP:
        fetch(cursor,mycon,table_name,chat_user,userid)
def fetchall(cursor,user_id,chat_user,table_name):
    global MSG
    user_id_msg=[]
    chat_user_msg=[]    
    cursor.execute("select {},{} from {};".format(user_id,chat_user,table_name))
    for i in cursor:
        if i==(None,None):
            continue
        user_id_msg.append(i[0])
        chat_user_msg.append(i[1])
    if user_id_msg!=[] or chat_user_msg!=[]:
        for i in range(len(user_id_msg)):
            if user_id_msg==[]:
                break
            if user_id_msg[i]==None:
                print(f"{chat_user}:",' '.join(chat_user_msg[i].split()[0:-2]))
            if chat_user_msg[i]==None:
                print(f"{user_id}:",' '.join(user_id_msg[i].split()[0:-2]))
    MSG=chat_user_msg
    