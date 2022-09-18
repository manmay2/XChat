def push(cursor):
    text=input(user_id,":")
    cursor.execute("insert into {} {} values('{}')".format(table_name,user_id,text))