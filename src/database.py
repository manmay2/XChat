import mysql.connector as s
from SignIn import *
from SignUp import *
def details():
    print("3. Press 3 to see who are there in the list of sign in")
mycon=s.connect(host="localhost",user="root", passwd="2%0*2)0$Happy",database="xchat")
print("........WELCOME TO THE WORLD OF XCHAT APP.........")
cursor=mycon.cursor()
f=0
if f==0:
    cursor.execute("create table if not exists signup(username varchar(200) primary key,password varchar(8))")
    f=1
print("1. NEW TO THE APP!! PRESS 1 TO SIGN UP")
print("2. ALREADY HAVE AN ACCOUNT !! PRESS 2 TO SIGN IN")
choice=int(input("ENTER YOUR CHOICE: "))
if(choice==1):
    signup(mycon,cursor)
elif(choice==2):
    signin(cursor)
    details()
    
    
