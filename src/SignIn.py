def signin(cursor):
    user_id = input("Enter your user name to login: ")
    f=0
    inc=0
    paswd = input("Enter the password to login: ")
    cursor.execute("select * from signup;")
    data = cursor.fetchall()
    for i in data:
        if(i[0] == user_id and i[1] == paswd):
            print("YOU ARE SUCCESSFULLY SIGNED IN")
            print("___________________________________________________")
            f=1
    if f!=1:
        print("PLEASE CHECK YOUR USERNAME AND PASSWORD AND TRY AGAIN LATER!!!!")
    elif(f==1):
        cursor.execute("select * from signup;")
        for j in cursor.fetchall():
            if(j[0]==user_id and j[1]==paswd):
                continue
            else:
                inc+=1
                print(inc,".",j[0])
        ch=int(input("-----WHOM DO YOU WANT TO CHAT-----"))
        
        cursor.execute("create table if not exists {0}({1} varchar(10000000000)),{2} varchar(10000000000)".format(user_id+paswd))
s        
     
