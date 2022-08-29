def signin(cursor):
    user_id = input("Enter your user name to login: ")
    f = 0
    inc = 0
    paswd = input("Enter the password to login: ")
    cursor.execute("select * from signup;")
    data = cursor.fetchall()
    for i in data:
        if(i[0] == user_id and i[1] == paswd):
            print("YOU ARE SUCCESSFULLY SIGNED IN")
            print("___________________________________________________")
            f = 1
    if f != 1:
        print("PLEASE CHECK YOUR USERNAME AND PASSWORD AND TRY AGAIN LATER!!!!")
    elif(f == 1):
        data.remove((user_id, paswd))
        for j in data:
            if(j[0] == user_id and j[1] == paswd):
                continue
            else:
                inc += 1
                print(inc, ".", j[0])
        ch = int(input("-----WHOM DO YOU WANT TO CHAT-"))
        try:
            query = f"create table if not exists {user_id+str(data[ch-1][0])}({user_id} varchar(65535),{str(data[ch-1][0])} varchar(65535))"
            cursor.execute(query)
        except:
            print("Error occured....Try again later....")
