def signup(mycon, cursor):
    user_name = input("Enter a user name: ").strip()
    pas = input("Set a strong password for your account: ").strip()
    cursor.execute(
        "insert into signup values('{0}','{1}')".format(user_name, pas))
    mycon.commit()
