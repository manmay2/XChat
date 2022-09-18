
def push(cursor,mycon,user_id,table_name):
    text=input(f"{user_id} :")
    cursor.execute("insert into {}({}) values('{}');".format(table_name,user_id,text))
    mycon.commit()  
def fetch(cursor,table_name,chat_user):
    cursor.execute("select {} from {};".format(chat_user,table_name))
    for i in cursor:
        if i == (None,):
            continue
        print(f"{chat_user}: ",i[0])
def fetchall(cursor,user_id,chat_user,table_name):
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
                print(f"{chat_user}:",chat_user_msg[i])
            if chat_user_msg[i]==None:
                print(f"{user_id}:",user_id_msg[i])
    
