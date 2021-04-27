from enum import Enum
import hashlib
import mysql.connector
from Functions.passwordValidator import validatePassword
from Functions.MsgBox import createMsgBox
from Functions.InputBox import createInputBox
def login():
    username= createInputBox("Enter Username","Username:")
    passwordString=createInputBox("Enter Password","Password:")
    userOut = [] # used to pass basic user details back to the main program
    class Valid(Enum): 
        notChecked =1
        notValid =2
        valid =3
    passStatus = Valid.notChecked
    userStatus = Valid.notChecked
    if not username:
        userStatus = Valid.notValid
    else:
        userStatus = Valid.valid
    if not passwordString:
        passStatus = Valid.notValid
    if passStatus == Valid.notChecked:
        pState = validatePassword(passwordString) #call Validation module for password
        if pState == True:
            passStatus = Valid.valid
        else:
            passStatus = Valid.notValid
    if not passStatus == Valid.valid or not userStatus == Valid.valid:
        createMsgBox("Please re-enter password or username in correct format","Invalid Format")
    else:
        PassToHash = hashlib.md5(passwordString.encode()) # hashes password
        PassHash = PassToHash.hexdigest()
        try:
            cnx = mysql.connector.connect(host="localhost",user="root", password="",database="schooldetention") # connects to sql database to check if username and password are correct
        except mysql.connector.Error as err:
            createMsgBox(f"{err}","connection error")
        else:
            query = cnx.cursor()
            query.execute(f"SELECT StaffID, FirstName, Surname, DepartmentName, DepartmentCode, Username, Slt FROM STAFF WHERE Username = \"{username}\" AND Passwrd = \"{PassHash}\"")
            results = query.fetchall()
            results = [list(y) for y in results]   #used to convert query results from tuple to list
            if len(results)> 1:
                createMsgBox("Error:multiple results. Username and password conflict error","Error")
            elif len(results)==0:
                createMsgBox("Incorect usernme or password","Invalid submition")
            else: 
                    userOut = results[0]
            cnx.close()
    return userOut
