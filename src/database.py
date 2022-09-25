import mysql.connector as s
from SignIn import *
from SignUp import *
import os
print("........WELCOME TO THE WORLD OF XCHAT APP.........")
try:
    mycon = s.connect(host="localhost", user=os.environ.get("DB_USER"),
                      passwd=os.environ.get("DB_PASS"), database="xchat")
    cursor = mycon.cursor()

    cursor.execute(
        "create table if not exists signup(username varchar(200) primary key,password varchar(8))")

    print("1. NEW TO THE APP!! PRESS 1 TO SIGN UP")
    print("2. ALREADY HAVE AN ACCOUNT !! PRESS 2 TO SIGN IN")

    choice = int(input("ENTER YOUR CHOICE: "))
    if(choice == 1):
        signup(mycon, cursor)
    elif(choice == 2):
        signin(cursor, mycon)
except:
    print("Something error occured...Try after sometime")
