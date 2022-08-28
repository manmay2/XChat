def signin(cursor):
    user_id = input("Enter your user name to login: ")
    paswd = input("Enter the password to login: ")
    cursor.execute("select * from signup")
    data = cursor.fetchall()
    for i in data:
        if(i[0] == user_id and i[1] == paswd):
            print("YOU ARE SUCCESSFULLY SIGNED IN")
            break
    else:
        print("USERNAME OR PASSWORD IS ENTERED WRONG...PLEASE TRY AGAIN")
