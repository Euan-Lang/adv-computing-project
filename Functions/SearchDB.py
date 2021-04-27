from Functions.MsgBox import createMsgBox
from datetime import date, timedelta
import mysql.connector
def searchRegClass(queryValue,PupilRecord):
    resultsOut = []
    try:
        cnx = mysql.connector.connect(host="localhost",user="root", password="",database="schooldetention") # connects to sql database to check if username and password are correct
    except mysql.connector.Error as err:
        createMsgBox(f"{err}","connection error")
    else:
        query = cnx.cursor()
        query.execute(f"SELECT * FROM pupil WHERE RegClass = \"{queryValue}\";")
        results = query.fetchall()
        results = [list(y) for y in results] # converts list of tuples to list of lists
        for x in results:
            pupilrow = PupilRecord(x[0],x[1]+" "+x[2],x[3])
            resultsOut.append(pupilrow)
    return resultsOut

def returnAllDetentions(DetentionRecord):
    resultsOut = []
    currentDate = date.today()
    maxDate = date.today() + timedelta(7) # this limits the returned detention so staff can only add upto 1 week ahead
    try:
        cnx = mysql.connector.connect(host="localhost",user="root", password="",database="schooldetention") # connects to sql database to check if username and password are correct
    except mysql.connector.Error as err:
        createMsgBox(f"{err}","connection error")
    else:
        query = cnx.cursor()
        query.execute(f"SELECT * FROM Detention WHERE DetentionDate >=\"{currentDate}\" AND DetentionDate <= \"{maxDate}\" """)
        results = query.fetchall()
        results = [list(y) for y in results]# converts list of tuples to list of lists
        for x in results:
            formatedDate =str(x[1])
            datarow = DetentionRecord(x[0],formatedDate,x[2],x[3],x[4])
            resultsOut.append(datarow)
    return(resultsOut)
        
