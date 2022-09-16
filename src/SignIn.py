def signin(cursor):
    user_id = input("Enter your user name to login: ").strip()
    paswd = input("Enter the password to login: ").strip()
    flag = 0
    inc = 0
    cursor.execute("select * from signup;")
    data = cursor.fetchall()
    for i in data:
        if(i[0] == user_id and i[1] == paswd):
            print("YOU ARE SUCCESSFULLY SIGNED IN")
            print("___________________________________________________")
            flag = 1
    if flag != 1:
        print("PLEASE CHECK YOUR USERNAME AND PASSWORD AND TRY AGAIN LATER!!!!")
    elif(flag == 1):
        data.remove((user_id, paswd))
        for j in data:
            if(j[0] == user_id and j[1] == paswd):
                continue
            else:
                inc += 1
                print(inc, ".", j[0])
        ch = int(input("WHOM DO YOU WANT TO CHAT--- : "))
        table_name=user_id+str(data[ch-1][0])
        query = f"create table if not exists {table_name}({user_id} LONGTEXT,{str(data[ch-1][0])} LONGTEXT);"
        cursor.execute(query)
        print(user_id,":")
        text=input()
        cursor.execute("insert into {} values('{}','{}')".format(table_name,text," "))
        
